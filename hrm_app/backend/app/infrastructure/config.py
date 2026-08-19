"""
Infrastructure config — reads settings from environment / .env.
This is the only place that knows concrete connection strings and ports.
"""
from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]   # .../hrm_app/backend


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        extra="ignore",
        protected_namespaces=(),   # allow fields we name freely
    )

    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/hrm"
    )
    artifact_path: str = "var/hrm_model.joblib"   # relative to backend dir
    cors_origins: str = "http://localhost:3000"
    api_port: int = 8010

    # Local LLM (Ollama) — free natural-language understanding for the chat.
    # llama3.1:8b plans messy, multi-step requests better than 3b; set
    # OLLAMA_MODEL=llama3.2:3b in .env to fall back to the faster small model.
    use_llm: bool = True
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"

    # Real biometric import (ZKTeco BioTime SQL dump) + the punch-merge rule.
    punch_merge_seconds: int = 60          # punches within this window count as one
    import_default_base_rate: float = 20.0  # starting pay rate (tune per employee later)
    import_default_ot_rate: float = 30.0
    import_sql_path: str = r"C:\Users\tarek\Downloads\bio_time27-07-2026.sql"

    @property
    def artifact_abspath(self) -> Path:
        return BACKEND_DIR / self.artifact_path

    @property
    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
