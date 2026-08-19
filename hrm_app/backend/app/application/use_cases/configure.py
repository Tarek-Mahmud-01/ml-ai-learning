"""
Use case: change a chat-editable setting (persisted via ConfigRepository). Only
a small whitelist of keys is allowed, each coerced to the right type. These are
read back by the import / generate use cases (config overrides the .env default).
"""
from __future__ import annotations

from ...domain.repositories import ConfigRepository

# key -> (type, human label)
ALLOWED = {
    "merge_seconds": ("int", "punch-merge window (seconds)"),
    "default_base_rate": ("float", "default base pay rate ($/h)"),
    "default_ot_rate": ("float", "default overtime rate ($/h)"),
}

_ALIASES = {
    "merge_window": "merge_seconds", "merge": "merge_seconds",
    "punch_merge_seconds": "merge_seconds",
    "base_rate": "default_base_rate", "rate": "default_base_rate",
    "default_rate": "default_base_rate",
    "ot_rate": "default_ot_rate", "overtime_rate": "default_ot_rate",
}


class Configure:
    def __init__(self, config: ConfigRepository) -> None:
        self._c = config

    def execute(self, key: str, value) -> tuple[str, str, str]:
        key = (key or "").strip().lower().replace(" ", "_")
        key = _ALIASES.get(key, key)
        if key not in ALLOWED:
            raise ValueError(
                "Unknown setting. You can set: " + ", ".join(ALLOWED))
        typ, label = ALLOWED[key]
        raw = str(value).strip()
        try:
            val = str(int(float(raw))) if typ == "int" else str(float(raw))
        except (TypeError, ValueError):
            raise ValueError(f"'{value}' is not a valid number for {label}.")
        self._c.set(key, val)
        return key, val, label
