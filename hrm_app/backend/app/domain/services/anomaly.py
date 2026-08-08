"""
AnomalyDetector — the ML BRAIN's PORT (interface only).

The domain declares WHAT it needs ("tell me if this day looks unusual") without
knowing HOW. The concrete scikit-learn implementation lives in infrastructure.
This keeps sklearn out of the domain and makes the model swappable.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from ..entities import STATUS_BOTH, STATUS_ML, STATUS_OK, STATUS_RULE
from ..value_objects import DayFeatures


class AnomalyDetector(ABC):
    """Port: given one day's features, is it anomalous (likely wrong)?"""

    @abstractmethod
    def is_wrong(self, features: DayFeatures) -> bool:
        ...


class NullDetector(AnomalyDetector):
    """Safe fallback when no model is trained yet — flags nothing."""

    def is_wrong(self, features: DayFeatures) -> bool:  # noqa: ARG002
        return False


class DetectorTrainer(ABC):
    """Port: learn an anomaly detector from worked-day features (unsupervised)."""

    @abstractmethod
    def train(self, samples: list[DayFeatures]) -> AnomalyDetector:
        ...


class SupervisedTrainer(ABC):
    """Port: learn a detector from the user's labeled examples (supervised)."""

    @abstractmethod
    def train(self, samples: list[tuple[DayFeatures, bool]]) -> AnomalyDetector:
        ...


def build_status(rule_flag: bool, ml_flag: bool) -> str:
    """Combine the two brains into one status for the UI."""
    if rule_flag and ml_flag:
        return STATUS_BOTH
    if rule_flag:
        return STATUS_RULE
    if ml_flag:
        return STATUS_ML
    return STATUS_OK
