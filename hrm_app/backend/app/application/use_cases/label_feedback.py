"""Teaching the model: save user labels, then retrain a supervised detector."""
from __future__ import annotations

from datetime import date

from ...domain.entities import Label
from ...domain.repositories import (
    AttendanceRepository,
    EmployeeRepository,
    LabelRepository,
)
from ...domain.services.anomaly import SupervisedTrainer
from ...domain.value_objects import DayFeatures, parse_hour


class SaveLabel:
    def __init__(self, employees: EmployeeRepository,
                 attendance: AttendanceRepository, labels: LabelRepository) -> None:
        self._e = employees
        self._a = attendance
        self._l = labels

    def execute(self, employee_id, day, is_wrong: bool) -> Label:
        if self._e.get(employee_id) is None:
            raise ValueError(f"{employee_id} not found")
        try:
            d = date.fromisoformat(day)
        except (ValueError, TypeError):
            raise ValueError("please give a date like 2024-06-11")
        if self._a.get_day(employee_id, d) is None:
            raise ValueError(f"no attendance for {employee_id} on {day} to label")
        lab = Label(employee_id, d, bool(is_wrong))
        self._l.upsert(lab)
        return lab


class SupervisedTrain:
    def __init__(self, attendance: AttendanceRepository, labels: LabelRepository,
                 trainer: SupervisedTrainer) -> None:
        self._a = attendance
        self._l = labels
        self._trainer = trainer

    def execute(self) -> dict:
        samples: list[tuple[DayFeatures, bool]] = []
        for lab in self._l.list_all():
            day = self._a.get_day(lab.employee_id, lab.day)
            if day is None:
                continue
            ci, co = parse_hour(day.check_in), parse_hour(day.check_out)
            if ci is None or co is None:
                continue
            presence = co - ci
            if presence <= 0:
                continue
            samples.append((DayFeatures(presence, day.reported_pay), lab.is_wrong))

        self._trainer.train(samples)
        wrong = sum(1 for _, w in samples if w)
        classes = len({w for _, w in samples})
        trained = len(samples) >= 4 and classes >= 2
        return {
            "labels": len(samples),
            "wrong": wrong,
            "correct": len(samples) - wrong,
            "trained": trained,
        }
