"""
End-to-end API test via FastAPI TestClient: seed → train → report.
Requires the Postgres 'hrm' database to be reachable.
Run from backend folder:  python -m pytest tests/test_api_e2e.py -q
"""
from fastapi.testclient import TestClient

from app.presentation.main import app


def test_seed_train_and_report():
    # `with` triggers the lifespan startup (creates tables).
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}

        # seed a month
        seed = client.post("/admin/seed", json={"month": "2024-06"}).json()
        assert seed["employees"] == 12
        assert seed["attendance_days"] > 0

        # train the detector
        trained = client.post("/admin/train").json()
        assert trained["samples_trained"] > 0

        # list employees
        emps = client.get("/employees").json()
        assert len(emps) == 12
        first = emps[0]["id"]

        # monthly report for the first employee
        rep = client.get(f"/employees/{first}/report", params={"month": "2024-06"}).json()
        assert rep["employee_id"] == first
        assert rep["total_days"] > 0
        # KPI cross-check: total paid equals sum of day rows
        day_sum = round(sum(d["reported_pay"] for d in rep["days"]), 2)
        assert abs(day_sum - rep["total_paid"]) < 0.01

        # unknown employee → 404
        assert client.get(
            "/employees/NOPE/report", params={"month": "2024-06"}).status_code == 404
