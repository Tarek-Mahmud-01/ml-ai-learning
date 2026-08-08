"""Use case: retrain the unsupervised detector on the current attendance data."""
from __future__ import annotations

from dataclasses import dataclass

from ...domain.repositories import AttendanceRepository
from ...domain.services.anomaly import DetectorTrainer
from ...domain.value_objects import DayFeatures, parse_hour


@dataclass
class TrainingReport:
    samples: int
    features: list[str]
    algorithm: str
    kind: str


class TrainModel:
    def __init__(self, attendance: AttendanceRepository, trainer: DetectorTrainer) -> None:
        self._attendance = attendance
        self._trainer = trainer

    def execute(self) -> TrainingReport:
        """Train on worked days; returns a small report so callers can explain it."""
        samples: list[DayFeatures] = []
        for d in self._attendance.list_all():
            ci, co = parse_hour(d.check_in), parse_hour(d.check_out)
            if ci is None or co is None:
                continue
            presence = co - ci
            if presence <= 0:
                continue
            samples.append(DayFeatures(presence, d.reported_pay))
        self._trainer.train(samples)
        trained = len(samples) >= 10
        return TrainingReport(
            samples=len(samples),
            features=["presence_hours", "reported_pay", "pay_per_hour"],
            algorithm="IsolationForest (unsupervised)",
            kind="iforest" if trained else "none",
        )
