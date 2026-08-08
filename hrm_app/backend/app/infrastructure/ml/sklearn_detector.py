"""
scikit-learn implementations of the domain's detector/trainer ports. The ONLY
place sklearn/pandas appear for detection — the domain stays clean.

Two model kinds behind one interface (teaches supervised vs unsupervised):
  kind="iforest" — IsolationForest (unsupervised); predict == -1 => wrong
  kind="rf"      — RandomForest    (supervised);   predict ==  1 => wrong
The active artifact carries its `kind`; whichever was trained last is used.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier

from ...domain.services.anomaly import (
    AnomalyDetector,
    DetectorTrainer,
    NullDetector,
    SupervisedTrainer,
)
from ...domain.value_objects import DayFeatures
from . import model_store

FEATURES = ["presence_hours", "Reported_Pay", "pay_per_hour"]


def _row(f: DayFeatures) -> list[float]:
    return [f.presence_hours, f.reported_pay, f.pay_per_hour]


class SklearnDetector(AnomalyDetector):
    """Wraps a fitted model; interpretation of 'wrong' depends on the kind."""

    def __init__(self, model, features: list[str], kind: str) -> None:
        self._model = model
        self._features = features
        self._kind = kind

    def is_wrong(self, features: DayFeatures) -> bool:
        X = pd.DataFrame([_row(features)], columns=self._features)
        pred = self._model.predict(X)[0]
        if self._kind == "rf":
            return bool(pred == 1)
        return bool(pred == -1)   # iforest: outlier


class SklearnTrainer(DetectorTrainer):
    """Unsupervised — fits IsolationForest on worked-day features."""

    def __init__(self, artifact_path: str | Path, contamination: float = 0.06) -> None:
        self._path = artifact_path
        self._contamination = contamination

    def train(self, samples: list[DayFeatures]) -> AnomalyDetector:
        if len(samples) < 10:
            return NullDetector()
        X = pd.DataFrame([_row(s) for s in samples], columns=FEATURES)
        model = IsolationForest(
            contamination=self._contamination, random_state=42, n_estimators=100)
        model.fit(X)
        model_store.save(
            {"model": model, "features": FEATURES, "kind": "iforest"}, self._path)
        return SklearnDetector(model, FEATURES, "iforest")


class SklearnSupervisedTrainer(SupervisedTrainer):
    """Supervised — fits RandomForest on the user's labeled examples."""

    def __init__(self, artifact_path: str | Path) -> None:
        self._path = artifact_path

    def train(self, samples: list[tuple[DayFeatures, bool]]) -> AnomalyDetector:
        labels = {int(w) for _, w in samples}
        if len(samples) < 4 or len(labels) < 2:
            # need at least both classes to learn a boundary
            return NullDetector()
        X = pd.DataFrame([_row(f) for f, _ in samples], columns=FEATURES)
        y = [int(w) for _, w in samples]
        model = RandomForestClassifier(
            n_estimators=100, class_weight="balanced", random_state=42)
        model.fit(X, y)
        model_store.save(
            {"model": model, "features": FEATURES, "kind": "rf"}, self._path)
        return SklearnDetector(model, FEATURES, "rf")


def load_detector(artifact_path: str | Path) -> AnomalyDetector:
    """Load the active detector (any kind), or NullDetector if none trained."""
    obj = model_store.load(artifact_path)
    if not obj:
        return NullDetector()
    return SklearnDetector(obj["model"], obj["features"], obj.get("kind", "iforest"))
