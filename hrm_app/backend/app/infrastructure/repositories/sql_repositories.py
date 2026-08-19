"""
SQLAlchemy implementations of the domain repository PORTS.
These depend on the domain (implement its interfaces); the domain never sees them.
"""
from __future__ import annotations

from datetime import date

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from ...domain.entities import AttendanceDay, AuditEntry, Employee, Label
from ...domain.repositories import (
    AttendanceRepository,
    AuditRepository,
    ConfigRepository,
    EmployeeRepository,
    LabelRepository,
)
from ..db.models import (
    AppConfigModel,
    AttendanceModel,
    AuditModel,
    ConversationModel,
    EmployeeModel,
    LabelModel,
)
from .mappers import (
    attendance_to_domain,
    attendance_to_orm,
    employee_to_domain,
    employee_to_orm,
)


class SqlEmployeeRepository(EmployeeRepository):
    def __init__(self, session: Session) -> None:
        self._s = session

    def add(self, employee: Employee) -> None:
        self._s.merge(employee_to_orm(employee))
        self._s.commit()

    def get(self, employee_id: str) -> Employee | None:
        m = self._s.get(EmployeeModel, employee_id)
        return employee_to_domain(m) if m else None

    def list_all(self) -> list[Employee]:
        rows = self._s.scalars(select(EmployeeModel).order_by(EmployeeModel.id)).all()
        return [employee_to_domain(m) for m in rows]

    def delete(self, employee_id: str) -> None:
        self._s.execute(
            delete(EmployeeModel).where(EmployeeModel.id == employee_id))
        self._s.commit()

    def clear(self) -> None:
        self._s.execute(delete(EmployeeModel))
        self._s.commit()


class SqlAttendanceRepository(AttendanceRepository):
    def __init__(self, session: Session) -> None:
        self._s = session

    def add_many(self, days: list[AttendanceDay]) -> None:
        self._s.add_all([attendance_to_orm(d) for d in days])
        self._s.commit()

    def _find(self, employee_id: str, day: date) -> AttendanceModel | None:
        return self._s.scalars(
            select(AttendanceModel).where(
                AttendanceModel.employee_id == employee_id,
                AttendanceModel.day == day,
            )
        ).first()

    def upsert_day(self, day: AttendanceDay) -> None:
        existing = self._find(day.employee_id, day.day)
        if existing:
            existing.day_type = day.day_type.value
            existing.check_in = day.check_in
            existing.check_out = day.check_out
            existing.reported_pay = day.reported_pay
        else:
            self._s.add(attendance_to_orm(day))
        self._s.commit()

    def get_day(self, employee_id: str, day: date) -> AttendanceDay | None:
        m = self._find(employee_id, day)
        return attendance_to_domain(m) if m else None

    def delete_day(self, employee_id: str, day: date) -> bool:
        m = self._find(employee_id, day)
        if not m:
            return False
        self._s.delete(m)
        self._s.commit()
        return True

    def list_for_month(
        self, employee_id: str, year: int, month: int
    ) -> list[AttendanceDay]:
        stmt = (
            select(AttendanceModel)
            .where(AttendanceModel.employee_id == employee_id)
            .order_by(AttendanceModel.day)
        )
        rows = self._s.scalars(stmt).all()
        return [
            attendance_to_domain(m)
            for m in rows
            if m.day.year == year and m.day.month == month
        ]

    def list_months(self, employee_id: str) -> list[tuple[int, int]]:
        rows = self._s.scalars(
            select(AttendanceModel.day).where(
                AttendanceModel.employee_id == employee_id)).all()
        return sorted({(d.year, d.month) for d in rows})

    def list_all(self) -> list[AttendanceDay]:
        rows = self._s.scalars(select(AttendanceModel)).all()
        return [attendance_to_domain(m) for m in rows]

    def clear(self) -> None:
        self._s.execute(delete(AttendanceModel))
        self._s.commit()


class SqlLabelRepository(LabelRepository):
    def __init__(self, session: Session) -> None:
        self._s = session

    def upsert(self, label: Label) -> None:
        existing = self._s.scalars(
            select(LabelModel).where(
                LabelModel.employee_id == label.employee_id,
                LabelModel.day == label.day,
            )
        ).first()
        if existing:
            existing.is_wrong = label.is_wrong
        else:
            self._s.add(LabelModel(
                employee_id=label.employee_id, day=label.day,
                is_wrong=label.is_wrong))
        self._s.commit()

    def list_all(self) -> list[Label]:
        rows = self._s.scalars(select(LabelModel)).all()
        return [Label(m.employee_id, m.day, m.is_wrong) for m in rows]

    def clear(self) -> None:
        self._s.execute(delete(LabelModel))
        self._s.commit()


class SqlAuditRepository(AuditRepository):
    def __init__(self, session: Session) -> None:
        self._s = session

    def add(self, entry: AuditEntry) -> None:
        self._s.add(AuditModel(
            action=entry.action, target=entry.target, detail=entry.detail))
        self._s.commit()

    def list_recent(self, limit: int = 20) -> list[AuditEntry]:
        rows = self._s.scalars(
            select(AuditModel).order_by(AuditModel.id.desc()).limit(limit)).all()
        return [AuditEntry(m.action, m.target, m.detail) for m in rows]


class SqlConfigRepository(ConfigRepository):
    def __init__(self, session: Session) -> None:
        self._s = session

    def get(self, key: str) -> str | None:
        m = self._s.get(AppConfigModel, key)
        return m.value if m else None

    def set(self, key: str, value: str) -> None:
        self._s.merge(AppConfigModel(key=key, value=value))
        self._s.commit()

    def all(self) -> dict[str, str]:
        rows = self._s.scalars(select(AppConfigModel)).all()
        return {m.key: m.value for m in rows}


class SqlConversationStore:
    """Agent chat memory (user/assistant messages) keyed by session id."""

    def __init__(self, session: Session) -> None:
        self._s = session

    def load(self, session_id: str, limit: int = 20) -> list[dict]:
        rows = self._s.scalars(
            select(ConversationModel)
            .where(ConversationModel.session_id == session_id)
            .order_by(ConversationModel.id.desc())
            .limit(limit)
        ).all()
        return [{"role": m.role, "content": m.content} for m in reversed(rows)]

    def append(self, session_id: str, role: str, content: str) -> None:
        self._s.add(ConversationModel(
            session_id=session_id, role=role, content=content))
        self._s.commit()
