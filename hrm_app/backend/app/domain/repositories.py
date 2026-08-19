"""
Repository PORTS (interfaces) — the domain says what persistence it needs, not
how. Concrete SQLAlchemy/Postgres implementations live in infrastructure and
depend on these; the domain depends on nothing.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from .entities import AttendanceDay, AuditEntry, Employee, Label


class EmployeeRepository(ABC):
    @abstractmethod
    def add(self, employee: Employee) -> None: ...

    @abstractmethod
    def get(self, employee_id: str) -> Employee | None: ...

    @abstractmethod
    def list_all(self) -> list[Employee]: ...

    @abstractmethod
    def delete(self, employee_id: str) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...


class AttendanceRepository(ABC):
    @abstractmethod
    def add_many(self, days: list[AttendanceDay]) -> None: ...

    @abstractmethod
    def upsert_day(self, day: AttendanceDay) -> None: ...

    @abstractmethod
    def get_day(self, employee_id: str, day: date) -> AttendanceDay | None: ...

    @abstractmethod
    def delete_day(self, employee_id: str, day: date) -> bool: ...

    @abstractmethod
    def list_for_month(
        self, employee_id: str, year: int, month: int
    ) -> list[AttendanceDay]: ...

    @abstractmethod
    def list_months(self, employee_id: str) -> list[tuple[int, int]]: ...

    @abstractmethod
    def list_all(self) -> list[AttendanceDay]: ...

    @abstractmethod
    def clear(self) -> None: ...


class LabelRepository(ABC):
    @abstractmethod
    def upsert(self, label: Label) -> None: ...

    @abstractmethod
    def list_all(self) -> list[Label]: ...

    @abstractmethod
    def clear(self) -> None: ...


class AuditRepository(ABC):
    @abstractmethod
    def add(self, entry: AuditEntry) -> None: ...

    @abstractmethod
    def list_recent(self, limit: int = 20) -> list[AuditEntry]: ...


class ConfigRepository(ABC):
    """Chat-editable key/value settings (e.g. punch-merge window)."""

    @abstractmethod
    def get(self, key: str) -> str | None: ...

    @abstractmethod
    def set(self, key: str, value: str) -> None: ...

    @abstractmethod
    def all(self) -> dict[str, str]: ...
