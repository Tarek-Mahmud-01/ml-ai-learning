"""Load/save the ML artifact (joblib). Pure I/O detail."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import joblib


def load(path: str | Path) -> dict[str, Any] | None:
    path = Path(path)
    if not path.exists():
        return None
    return joblib.load(path)


def save(obj: dict[str, Any], path: str | Path) -> None:
    path = Path(path)
    os.makedirs(path.parent, exist_ok=True)
    joblib.dump(obj, path)
