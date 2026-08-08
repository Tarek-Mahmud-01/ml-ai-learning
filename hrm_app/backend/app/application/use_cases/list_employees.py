"""Use case: list all employees."""
from __future__ import annotations

from ...domain.entities import Employee
from ...domain.repositories import EmployeeRepository


class ListEmployees:
    def __init__(self, employees: EmployeeRepository) -> None:
        self._employees = employees

    def execute(self) -> list[Employee]:
        return self._employees.list_all()
