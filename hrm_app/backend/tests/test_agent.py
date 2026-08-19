"""
Tests for the tool-calling agent: registry schemas, query_data, and the reason→
act→observe loop (with a fake LLM) incl. confirm-gating + max-steps. No live LLM/DB.
"""
from datetime import date

from app.application.agent.hrm_agent import HrmAgent
from app.application.agent.ports import LlmTurn, ToolCall
from app.application.agent.tools import default_registry
from app.application.use_cases.chat_assistant import ChatReply
from app.application.use_cases.query_data import QueryData
from app.domain.services.report import RosterReport, RosterRow

CLOCK = lambda: date(2026, 8, 17)  # noqa: E731


# ---- registry --------------------------------------------------------------
def test_registry_schemas_are_valid():
    r = default_registry()
    schemas = r.schemas()
    assert len(schemas) >= 20
    for s in schemas:
        assert s["type"] == "function"
        fn = s["function"]
        assert fn["name"] and fn["parameters"]["type"] == "object"
    assert r.get("delete_employee").destructive is True
    assert r.get("find_employee").writes is False
    assert r.get("train").writes is True


# ---- query_data ------------------------------------------------------------
def _row(eid, paid, present, ot, flagged):
    return RosterRow(eid, "N" + eid, present, 0, 0, paid, paid, flagged, 0.0,
                     "ISSUES" if flagged else "OK", paid > 0, ot_hours=ot, total_hours=180)


def test_query_data_sort_filter_limit():
    roster = RosterReport("2026-07", [
        _row("E1", 1000, 20, 40, 1),
        _row("E2", 2000, 26, 10, 0),
        _row("E3", 500, 5, 60, 3),
    ])
    top = QueryData().execute(roster, {"sort_by": "ot_hours", "descending": True, "limit": 2})
    assert "E3" in top and "E1" in top and "E2" not in top   # top-2 by overtime
    many = QueryData().execute(roster, {"filters": [{"field": "present_days", "op": ">", "value": "10"}]})
    assert "E1" in many and "E2" in many and "E3" not in many


# ---- agent loop ------------------------------------------------------------
class FakeLlm:
    def __init__(self, turns, final="**Done.**", loop=False):
        self._turns, self._final, self._loop = list(turns), final, loop
        self.tool_calls_seen = 0

    def chat(self, messages, tools):
        if not tools:                       # forced final answer
            return LlmTurn(content=self._final)
        if self._loop:
            return LlmTurn(tool_calls=[ToolCall("find_employee", {"query": "x"})])
        if self._turns:
            return self._turns.pop(0)
        return LlmTurn(content=self._final)


class FakeExecutor:
    def __init__(self):
        self.ran = []

    def run_tool(self, name, args, confirm, message, today, ctx):
        self.ran.append((name, dict(args), confirm))
        return ChatReply(f"ran {name}", changed=name.startswith(("delete", "generate")))

    def handle(self, message):
        return ChatReply("fallback answer")


class FakeMemory:
    def __init__(self):
        self.msgs = []

    def load(self, session_id, limit=20):
        return list(self.msgs)

    def append(self, session_id, role, content):
        self.msgs.append({"role": role, "content": content})


def _agent(llm, execu, mem):
    return HrmAgent(llm, default_registry(), execu, mem, CLOCK, max_steps=4)


def test_agent_runs_tool_then_answers():
    llm = FakeLlm([LlmTurn(tool_calls=[ToolCall("find_employee", {"query": "17"})])],
                  final="**Found** E100017.")
    execu, mem = FakeExecutor(), FakeMemory()
    events = list(_agent(llm, execu, mem).run("s1", "find employee 17"))

    kinds = [e["type"] for e in events]
    assert "status" in kinds and "tool" in kinds and kinds[-1] == "done"
    answer = next(e["text"] for e in events if e["type"] == "answer")
    assert "Found" in answer
    assert execu.ran[0][0] == "find_employee"
    assert [m["role"] for m in mem.msgs] == ["user", "assistant"]


def test_agent_confirm_gates_delete():
    script = [LlmTurn(tool_calls=[ToolCall("delete_employee", {"employee_id": "E100"})])]
    # not confirmed -> tool must NOT run
    execu = FakeExecutor()
    list(_agent(FakeLlm(script[:], final="Please confirm."), execu, FakeMemory())
         .run("s", "delete employee E100"))
    assert all(r[0] != "delete_employee" for r in execu.ran)

    # confirmed -> tool runs
    execu2 = FakeExecutor()
    list(_agent(FakeLlm([LlmTurn(tool_calls=[ToolCall("delete_employee", {"employee_id": "E100"})])],
                        final="Deleted."), execu2, FakeMemory())
         .run("s", "delete employee E100 confirm"))
    assert any(r[0] == "delete_employee" and r[2] is True for r in execu2.ran)


def test_agent_max_steps_terminates():
    events = list(_agent(FakeLlm([], final="**Wrapped up.**", loop=True),
                         FakeExecutor(), FakeMemory()).run("s", "loop forever"))
    answer = next(e["text"] for e in events if e["type"] == "answer")
    assert answer == "**Wrapped up.**"        # forced final after max_steps


def test_agent_falls_back_when_llm_dead():
    class DeadLlm:
        def chat(self, messages, tools):
            raise RuntimeError("ollama down")
    events = list(_agent(DeadLlm(), FakeExecutor(), FakeMemory()).run("s", "hi"))
    answer = next(e["text"] for e in events if e["type"] == "answer")
    assert answer == "fallback answer"


# ---- robustness: salvage text tool-calls + fuzzy employee search ----------
def test_salvage_tool_calls_written_as_text():
    from app.infrastructure.llm.ollama_agent_client import _tool_calls_from_text
    calls = _tool_calls_from_text(
        'First I will call {"name": "find_employee", "parameters": {"query": "17"}} okay')
    assert len(calls) == 1
    assert calls[0].name == "find_employee" and calls[0].args == {"query": "17"}
    assert _tool_calls_from_text("just a normal answer, no json here") == []


class _Emp:
    def __init__(self, i, n):
        self.id, self.name = i, n


class _EmpRepo:
    def __init__(self, emps):
        self._e = emps

    def list_all(self):
        return self._e


def test_find_employee_is_fuzzy_and_unique():
    from app.application.use_cases.find_employee import FindEmployee
    repo = _EmpRepo([_Emp("E100017", "MD JASHIM UDDIN"),
                     _Emp("E100055", "KABIR AHMED"),
                     _Emp("E100090", "LAIZU BAREK")])
    fe = FindEmployee(repo)
    assert [e.id for e in fe.execute("joshm uddin")] == ["E100017"]   # misspelled
    assert [e.id for e in fe.execute("id ends 17")] == ["E100017"]
    assert [e.id for e in fe.execute("kabir")] == ["E100055"]
    assert fe.execute("nobody-xyz") == []
