"""
ChatAssistant — the composition point for the admin chat. Parses one message
into a safe intent and dispatches to the right use case. Holds NO business math
(that lives in the domain services it calls). Every write is audited; deletes
require an explicit confirm.
"""
from __future__ import annotations

from dataclasses import dataclass

from ...domain.entities import AuditEntry
from ...domain.repositories import (
    AttendanceRepository,
    AuditRepository,
    EmployeeRepository,
    LabelRepository,
)
from ...domain.services import tutor
from ...domain.services.anomaly import (
    AnomalyDetector,
    DetectorTrainer,
    SupervisedTrainer,
)
from ...domain.services.chat_intents import IntentResolver
from ...domain.services.payroll_rules import PayrollRulesService
from .attendance_crud import (
    DeleteAttendance,
    EditAttendance,
    InsertAttendance,
    ShowDay,
)
from .check_employee_month import CheckEmployeeMonth
from .check_employee_range import CheckEmployeeRange
from .employee_crud import AddEmployee, DeleteEmployee, EditEmployee, ShowEmployee
from .import_bio_time import ImportBioTime
from .label_feedback import SaveLabel, SupervisedTrain
from .list_employees import ListEmployees
from .train_model import TrainModel

_WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


@dataclass
class ChatReply:
    reply: str
    kind: str | None = None      # active model kind after train/retrain
    changed: bool = False        # did this modify data?


class ChatAssistant:
    def __init__(
        self,
        employees: EmployeeRepository,
        attendance: AttendanceRepository,
        labels: LabelRepository,
        audit: AuditRepository,
        rules: PayrollRulesService,
        detector: AnomalyDetector,
        unsup_trainer: DetectorTrainer,
        sup_trainer: SupervisedTrainer,
        resolver: IntentResolver,
        importer: ImportBioTime,
        import_path: str,
    ) -> None:
        self._emp = employees
        self._att = attendance
        self._lab = labels
        self._audit_repo = audit
        self._rules = rules
        self._detector = detector
        self._unsup = unsup_trainer
        self._sup = sup_trainer
        self._resolver = resolver
        self._importer = importer
        self._import_path = import_path

    def handle(self, message: str) -> ChatReply:
        intent = self._resolver.resolve(message)
        try:
            return self._dispatch(intent, message)
        except ValueError as e:
            return ChatReply(f"⚠ {e}")
        except Exception as e:  # noqa: BLE001 — surface any adapter error safely
            return ChatReply(f"⚠ Sorry, I couldn't do that: {e}")

    def _audit(self, action: str, target: str, detail: str) -> None:
        self._audit_repo.add(AuditEntry(action, target, detail))

    def _dispatch(self, intent, message: str) -> ChatReply:
        k, p = intent.kind, intent.params

        if k == "help":
            return ChatReply(tutor.help_text())
        if k == "tutor":
            return ChatReply(tutor.answer(p.get("message", message)))

        # ---- import real biometric data ----
        if k == "import_data":
            rep = self._importer.execute(
                self._import_path,
                replace=p.get("replace", True),
                merge_seconds=p.get("merge_seconds"))
            self._audit("import_data", "biometric",
                        f"{rep['employees']} employees, {rep['attendance_days']} days")
            scope = ("replaced the demo data" if rep["replaced_demo"]
                     else "added alongside the demo data")
            return ChatReply(
                f"Imported real biometric data ({scope}):\n"
                f"• {rep['employees']} employees, {rep['attendance_days']} attendance days "
                f"({rep['date_from']} → {rep['date_to']})\n"
                f"• Merged {rep['punches_merged_away']} duplicate punches "
                f"(window {rep['merge_seconds']}s) from {rep['punches_read']} reads\n"
                f"• {rep['missing_punch_days']} missing-punch days (checked in, never out)\n"
                f"Pay is a ${rep['default_base_rate']:.0f}/h baseline — tune per employee, "
                f"e.g. 'set E100017 base rate to 25'. Now say 'train' to fit the model.",
                changed=True)

        # ---- training ----
        if k == "train":
            rep = TrainModel(self._att, self._unsup).execute()
            self._audit("train", "model", f"IsolationForest on {rep.samples} days")
            return ChatReply(
                f"Trained on {rep.samples} worked days.\n"
                f"• Features: {', '.join(rep.features)}\n"
                f"• Algorithm: {rep.algorithm}\n"
                f"It learned the 'normal' pattern; unusual days get flagged. "
                f"Active model: unsupervised.",
                kind="iforest", changed=True)

        if k == "retrain":
            res = SupervisedTrain(self._att, self._lab, self._sup).execute()
            if not res["trained"]:
                return ChatReply(
                    f"You have {res['labels']} labelled day(s) "
                    f"({res['wrong']} wrong, {res['correct']} correct). I need at "
                    f"least 4 labels with BOTH classes. Label more, e.g. "
                    f"'E100 2024-06-11 is wrong'.")
            self._audit("retrain", "model", f"RandomForest on {res['labels']} labels")
            return ChatReply(
                f"Retrained a SUPERVISED model on your {res['labels']} labels "
                f"({res['wrong']} wrong, {res['correct']} correct). "
                f"The report now uses what YOU taught it. Active model: supervised.",
                kind="rf", changed=True)

        if k == "label":
            lab = SaveLabel(self._emp, self._att, self._lab).execute(
                p["employee_id"], p["day"], p["is_wrong"])
            self._audit("label", f"{lab.employee_id} {lab.day}",
                        "wrong" if lab.is_wrong else "correct")
            return ChatReply(
                f"Noted {lab.employee_id} on {lab.day} as "
                f"{'WRONG' if lab.is_wrong else 'CORRECT'}. "
                f"Say 'retrain from my labels' when ready.", changed=True)

        # ---- employees ----
        if k == "add_employee":
            e = AddEmployee(self._emp).execute(
                p.get("name"), p.get("base_rate"), p.get("ot_rate"),
                p.get("shift_start"), p.get("employee_id"))
            self._audit("add_employee", e.id, f"{e.name} ${e.rules.base_rate:.0f}/h")
            return ChatReply(
                f"Added {e.id} — {e.name}: ${e.rules.base_rate:.0f}/h base, "
                f"start {e.rules.shift_start}.", changed=True)

        if k == "edit_employee":
            e, desc = EditEmployee(self._emp).execute(
                p["employee_id"], p.get("field"), p.get("value"))
            self._audit("edit_employee", e.id, desc)
            return ChatReply(f"Updated {e.id} — {desc}.", changed=True)

        if k == "delete_employee":
            if not intent.confirm:
                return ChatReply(
                    f"This will DELETE employee {p['employee_id']}. "
                    f"Send: 'delete employee {p['employee_id']} confirm' to proceed.")
            e = DeleteEmployee(self._emp).execute(p["employee_id"])
            self._audit("delete_employee", e.id, e.name)
            return ChatReply(f"Deleted employee {e.id} ({e.name}).", changed=True)

        if k == "show_employee":
            e = ShowEmployee(self._emp).execute(p["employee_id"])
            wd = "/".join(_WD[d] for d in sorted(e.rules.weekend_days))
            return ChatReply(
                f"{e.id} {e.name}: ${e.rules.base_rate:.0f}/h base, "
                f"${e.rules.ot_rate:.0f}/h OT, work {e.rules.work_goal:.0f}h, "
                f"start {e.rules.shift_start}, weekend {wd}.")

        if k == "list_employees":
            emps = ListEmployees(self._emp).execute()
            if not emps:
                return ChatReply("No employees yet. Try 'add employee Rakib rate 22'.")
            return ChatReply("Employees: " + ", ".join(f"{e.id} {e.name}" for e in emps))

        # ---- attendance / payroll ----
        if k == "insert_attendance":
            r = InsertAttendance(self._emp, self._att).execute(
                p["employee_id"], p["day"], p.get("day_type"),
                p.get("check_in"), p.get("check_out"), p.get("reported_pay"))
            self._audit("insert_attendance", f"{r.employee_id} {r.day}",
                        f"{r.day_type.value} ${r.reported_pay:.2f}")
            return ChatReply(
                f"Added attendance for {r.employee_id} on {r.day}: "
                f"{r.day_type.value}, {r.check_in or '—'}–{r.check_out or '—'}, "
                f"pay ${r.reported_pay:.2f}.", changed=True)

        if k == "edit_attendance":
            r, desc = EditAttendance(self._att).execute(
                p["employee_id"], p["day"], p["field"], p["value"])
            self._audit("edit_attendance", f"{r.employee_id} {r.day}", desc)
            return ChatReply(f"Updated {r.employee_id} {r.day} — {desc}.", changed=True)

        if k == "delete_attendance":
            if not intent.confirm:
                return ChatReply(
                    f"This will DELETE attendance for {p['employee_id']} on "
                    f"{p['day']}. Send the same command with 'confirm'.")
            DeleteAttendance(self._att).execute(p["employee_id"], p["day"])
            self._audit("delete_attendance", f"{p['employee_id']} {p['day']}", "deleted")
            return ChatReply(
                f"Deleted attendance for {p['employee_id']} on {p['day']}.",
                changed=True)

        # ---- checks ----
        if k == "check_month":
            if self._emp.get(p["employee_id"]) is None:
                raise ValueError(f"{p['employee_id']} not found")
            rep = CheckEmployeeMonth(
                self._emp, self._att, self._rules, self._detector
            ).execute(p["employee_id"], p["year"], p["month"])
            return ChatReply(f"{rep.summary}\nRules: {rep.rules_note}")

        if k == "check_range":
            if self._emp.get(p["employee_id"]) is None:
                raise ValueError(f"{p['employee_id']} not found")
            rep = CheckEmployeeRange(
                self._emp, self._att, self._rules, self._detector
            ).execute(p["employee_id"], int(p.get("months", 2)))
            return ChatReply(rep.summary)

        if k == "show_day":
            r = ShowDay(self._att).execute(p["employee_id"], p["day"])
            return ChatReply(
                f"{r.employee_id} {r.day}: {r.day_type.value}, "
                f"{r.check_in or '—'}–{r.check_out or '—'}, pay ${r.reported_pay:.2f}.")

        return ChatReply(tutor.help_text())
