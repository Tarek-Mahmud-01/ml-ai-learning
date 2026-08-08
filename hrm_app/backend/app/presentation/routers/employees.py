"""Employee endpoints — thin: call use case, map to schema."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ...application.use_cases.list_employees import ListEmployees
from ..deps import employee_repo, list_employees_uc
from ..schemas import EmployeeOut, employee_out

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_model=list[EmployeeOut])
def list_all(uc: ListEmployees = Depends(list_employees_uc)) -> list[EmployeeOut]:
    return [employee_out(e) for e in uc.execute()]


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_one(employee_id: str, repo=Depends(employee_repo)) -> EmployeeOut:
    emp = repo.get(employee_id)
    if emp is None:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
    return employee_out(emp)
