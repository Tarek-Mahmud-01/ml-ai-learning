"""SQLAlchemy ORM tables. Infrastructure detail — never imported by the domain."""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class EmployeeModel(Base):
    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    # per-employee rules (the "careful" requirement)
    base_rate: Mapped[float] = mapped_column(Float, default=20.0)
    ot_rate: Mapped[float] = mapped_column(Float, default=30.0)
    shift_hours: Mapped[float] = mapped_column(Float, default=9.0)
    work_goal: Mapped[float] = mapped_column(Float, default=8.0)
    lunch: Mapped[float] = mapped_column(Float, default=1.0)
    tolerance: Mapped[float] = mapped_column(Float, default=0.01)
    shift_start: Mapped[str] = mapped_column(String(8), default="09:00")
    late_after: Mapped[str] = mapped_column(String(8), default="09:15")
    weekend_days: Mapped[str] = mapped_column(String(16), default="5,6")


class AttendanceModel(Base):
    __tablename__ = "attendance_days"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(16), index=True)
    day: Mapped[date] = mapped_column(Date, index=True)
    day_type: Mapped[str] = mapped_column(String(20))
    check_in: Mapped[str | None] = mapped_column(String(8), nullable=True)
    check_out: Mapped[str | None] = mapped_column(String(8), nullable=True)
    reported_pay: Mapped[float] = mapped_column(Float, default=0.0)
    __table_args__ = (
        UniqueConstraint("employee_id", "day", name="uq_att_emp_day"),
    )


class LabelModel(Base):
    __tablename__ = "labels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(16), index=True)
    day: Mapped[date] = mapped_column(Date)
    is_wrong: Mapped[bool] = mapped_column(Boolean)
    __table_args__ = (
        UniqueConstraint("employee_id", "day", name="uq_label_emp_day"),
    )


class AuditModel(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    action: Mapped[str] = mapped_column(String(40))
    target: Mapped[str] = mapped_column(String(80))
    detail: Mapped[str] = mapped_column(String(400))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
