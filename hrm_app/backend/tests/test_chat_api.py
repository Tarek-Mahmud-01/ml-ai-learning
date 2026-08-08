"""
End-to-end chat flow through POST /chat. Requires Postgres 'hrm'.
Exercises: tutor, employee CRUD, attendance/payroll, check, train, label, retrain, delete.
"""
from fastapi.testclient import TestClient

from app.infrastructure.config import settings
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.repositories.sql_repositories import (
    SqlAuditRepository,
    SqlLabelRepository,
)
from app.presentation.main import app

# Tests use the deterministic regex resolver (fast, no LLM dependency).
settings.use_llm = False


def _say(client, msg):
    return client.post("/chat", json={"message": msg}).json()


def test_chat_full_flow():
    with TestClient(app) as client:
        client.post("/admin/seed", json={"month": "2024-06"})

        # clear any labels from previous runs for a clean supervised test
        s = SessionLocal()
        SqlLabelRepository(s).clear()
        s.close()

        # tutor
        assert "TRAINING" in _say(client, "how does training work?")["reply"]

        # add + list + edit employee
        r = _say(client, "add employee Rakib rate 22 start 09:00")
        assert r["changed"] and "Added" in r["reply"]
        assert "Rakib" in _say(client, "list employees")["reply"]
        assert "Updated E100" in _say(client, "set E100 base rate to 30")["reply"]

        # attendance + payroll (pay)
        assert _say(client, "add attendance E100 2024-06-15 present 09:00 18:00 pay 160")["changed"]
        assert "pay" in _say(client, "set E100 2024-06-15 pay to 190")["reply"]

        # check month + multi-month range
        assert "E100" in _say(client, "check E100 june")["reply"]
        assert "E100" in _say(client, "check E100 last two months")["reply"]

        # train (unsupervised)
        assert _say(client, "train")["kind"] == "iforest"

        # teach: 4 labels, both classes, on existing inserted days
        for d, pay, verdict in [
            ("2024-06-15", 190, "wrong"),
            ("2024-06-16", 160, "correct"),
            ("2024-06-17", 160, "correct"),
            ("2024-06-18", 50, "wrong"),
        ]:
            _say(client, f"add attendance E100 {d} present 09:00 18:00 pay {pay}")
            _say(client, f"E100 {d} is {verdict}")
        assert _say(client, "retrain from my labels")["kind"] == "rf"

        # delete needs confirm
        r1 = _say(client, "delete attendance E100 2024-06-18")
        assert "confirm" in r1["reply"].lower() and not r1["changed"]
        r2 = _say(client, "delete attendance E100 2024-06-18 confirm")
        assert r2["changed"]

        # audit trail recorded the writes
        s = SessionLocal()
        assert len(SqlAuditRepository(s).list_recent(50)) > 0
        s.close()

        # unknown -> help (fails safe)
        assert "I can manage" in _say(client, "asdfqwer")["reply"]
