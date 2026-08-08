"""Employee create / edit / delete / show use cases (orchestration only)."""
from __future__ import annotations

from dataclasses import replace

from ...domain.entities import Employee
from ...domain.repositories import EmployeeRepository
from ...domain.value_objects import EmployeeRules

_WD = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}
_EMP_FIELDS = {"base_rate", "ot_rate", "work_goal", "shift_start", "name", "weekend_days"}


def _next_id(existing: list[Employee]) -> str:
    nums = [int(e.id[1:]) for e in existing if e.id[1:].isdigit()]
    return f"E{(max(nums) + 1) if nums else 100:03d}"


def _parse_weekend(value: str) -> frozenset[int]:
    out = set()
    for token in str(value).replace("/", ",").split(","):
        key = token.strip()[:3].lower()
        if key in _WD:
            out.add(_WD[key])
    if not out:
        raise ValueError("weekend needs day names like 'fri,sat'")
    return frozenset(out)


class AddEmployee:
    def __init__(self, employees: EmployeeRepository) -> None:
        self._e = employees

    def execute(self, name: str | None, base_rate=None, ot_rate=None,
                shift_start=None, employee_id: str | None = None) -> Employee:
        if not name:
            raise ValueError("please give a name, e.g. 'add employee Rakib rate 22'")
        existing = self._e.list_all()
        if employee_id and self._e.get(employee_id):
            raise ValueError(f"{employee_id} already exists")
        emp = Employee(
            id=employee_id or _next_id(existing),
            name=name,
            rules=EmployeeRules(
                base_rate=float(base_rate) if base_rate is not None else 20.0,
                ot_rate=float(ot_rate) if ot_rate is not None else 30.0,
                shift_start=shift_start or "09:00",
            ),
        )
        self._e.add(emp)
        return emp


class EditEmployee:
    def __init__(self, employees: EmployeeRepository) -> None:
        self._e = employees

    def execute(self, employee_id: str, field: str | None, value) -> tuple[Employee, str]:
        if field not in _EMP_FIELDS:
            raise ValueError(
                "I can change: base_rate, ot_rate, work_goal, shift_start, name, weekend_days")
        if value in (None, ""):
            raise ValueError("please give a value, e.g. 'set E101 base rate to 30'")
        emp = self._e.get(employee_id)
        if emp is None:
            raise ValueError(f"{employee_id} not found")

        if field == "name":
            before = emp.name
            emp.name = str(value).strip()
            after = emp.name
        elif field == "weekend_days":
            before = "/".join(str(d) for d in sorted(emp.rules.weekend_days))
            emp.rules = replace(emp.rules, weekend_days=_parse_weekend(value))
            after = "/".join(str(d) for d in sorted(emp.rules.weekend_days))
        elif field == "shift_start":
            before = emp.rules.shift_start
            emp.rules = replace(emp.rules, shift_start=str(value).strip())
            after = emp.rules.shift_start
        else:  # numeric rule field
            before = getattr(emp.rules, field)
            emp.rules = replace(emp.rules, **{field: float(value)})
            after = getattr(emp.rules, field)

        self._e.add(emp)   # merge = upsert
        return emp, f"{field}: {before} -> {after}"


class DeleteEmployee:
    def __init__(self, employees: EmployeeRepository) -> None:
        self._e = employees

    def execute(self, employee_id: str) -> Employee:
        emp = self._e.get(employee_id)
        if emp is None:
            raise ValueError(f"{employee_id} not found")
        self._e.delete(employee_id)
        return emp


class ShowEmployee:
    def __init__(self, employees: EmployeeRepository) -> None:
        self._e = employees

    def execute(self, employee_id: str) -> Employee:
        emp = self._e.get(employee_id)
        if emp is None:
            raise ValueError(f"{employee_id} not found")
        return emp
