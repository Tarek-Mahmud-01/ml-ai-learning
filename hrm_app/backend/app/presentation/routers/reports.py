"""Monthly report endpoint — the core admin query."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from ...application.use_cases.check_employee_month import (
    CheckEmployeeMonth,
    EmployeeNotFound,
)
from ..deps import check_month_uc
from ..schemas import MonthReportOut, month_report_out

router = APIRouter(prefix="/employees", tags=["reports"])


@router.get("/{employee_id}/report", response_model=MonthReportOut)
def month_report(
    employee_id: str,
    month: str = Query(..., description="YYYY-MM", pattern=r"^\d{4}-\d{2}$"),
    uc: CheckEmployeeMonth = Depends(check_month_uc),
) -> MonthReportOut:
    year, mon = int(month[:4]), int(month[5:7])
    try:
        report = uc.execute(employee_id, year, mon)
    except EmployeeNotFound:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
    return month_report_out(report)
