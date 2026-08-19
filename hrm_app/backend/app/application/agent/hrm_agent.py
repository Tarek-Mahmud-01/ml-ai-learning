"""
HrmAgent — a real tool-calling agent loop (reason → act → observe → repeat).

The LLM is offered the tool registry; each turn it either calls tools (which we
execute via the shared ChatAssistant executor and feed back as observations) or
writes the final answer. `run()` is a generator that STREAMS events so the UI can
show live progress and type the answer out. `handle()` drains it for non-stream
callers/tests. Conversation memory gives multi-turn context + confirm flows.
"""
from __future__ import annotations

import re
from datetime import date
from typing import Callable, Iterator

from .ports import ConversationStore, LlmAgentClient
from .tools import ToolRegistry

_STATUS = {
    "find_employee": "🔍 Searching employees…", "list_employees": "📋 Listing employees…",
    "show_employee": "👤 Loading employee…", "check_month": "📊 Checking the month…",
    "check_range": "📊 Checking recent months…", "check_all": "📊 Building the roster…",
    "list_unpaid": "💸 Finding unpaid…", "list_absent": "📅 Finding absences…",
    "list_issues": "⚠️ Finding issues…", "list_paid": "💰 Finding paid…",
    "payslip": "🧾 Building payslip…", "query_data": "🔎 Running your query…",
    "list_attendance": "📅 Loading attendance…",
    "add_employee": "➕ Adding employee…", "edit_employee": "✏️ Updating employee…",
    "delete_employee": "🗑️ Deleting employee…", "insert_attendance": "➕ Adding attendance…",
    "edit_attendance": "✏️ Updating attendance…", "delete_attendance": "🗑️ Deleting attendance…",
    "generate_employees": "🧑‍🤝‍🧑 Creating staff…", "generate_salary": "🧑‍🤝‍🧑 Generating salary…",
    "configure": "⚙️ Saving setting…", "label": "🏷️ Saving label…", "train": "🧠 Training…",
    "retrain": "🧠 Retraining…", "import_data": "📥 Importing real data…", "tutor": "📚 Explaining…",
}


def _system(today: date) -> str:
    return (
        f"You are the assistant for an HR payroll & attendance system. "
        f"Today is {today.isoformat()}.\n"
        "You have TOOLS to look up and change HR data. To answer a request, CALL the "
        "tools you need (you may call several, across turns), then write the final "
        "answer yourself.\n\n"
        "Rules:\n"
        "- Use tools for ANY real data — NEVER invent employees, pay, hours, counts, or a "
        "tool's output. Report ONLY what the tools actually returned; if a tool errors or "
        "returns nothing, say so plainly.\n"
        "- The user's spelling/grammar is often messy — INTERPRET it, don't refuse. ALWAYS "
        "try a relevant tool before answering; never say 'I can't help' without trying.\n"
        "- If the user names a PERSON (not an id), call find_employee first to get their id, "
        "then use that id in the next tool. 'attendance list for <name>' → find_employee then "
        "list_attendance.\n"
        "- Prefer the FEWEST tools; a simple lookup needs ONE tool.\n"
        "- Months: pass month_phrase ('last month', 'june', '2026-07'). For a follow-up like "
        "'the month before that', work out the ACTUAL month from the conversation + today's "
        "date and pass it concretely (e.g. if the last question was about July 2026, pass "
        "'2026-06'). Don't reuse 'last month' for a different month.\n"
        "- Employee ids look like E100 or E100017.\n"
        "- Destructive tools (delete_*) run ONLY if the user said 'confirm' or 'yes'; "
        "otherwise ask them to confirm.\n"
        "- Finish with a SHORT, friendly answer in Markdown: a one-line summary, then "
        "**bold** key numbers and small bullet lists or a table where useful. Be warm and "
        "clear like a helpful assistant — never a raw data dump."
    )


class HrmAgent:
    def __init__(self, llm: LlmAgentClient, registry: ToolRegistry, executor,
                 memory: ConversationStore, clock: Callable[[], date],
                 max_steps: int = 6) -> None:
        self._llm = llm
        self._registry = registry
        self._executor = executor          # ChatAssistant (has run_tool)
        self._memory = memory
        self._clock = clock
        self._max_steps = max_steps

    @staticmethod
    def _confirmed(message: str) -> bool:
        return bool(re.search(r"\b(confirm|yes|confirmed|do it)\b", message.lower()))

    def run(self, session_id: str, message: str) -> Iterator[dict]:
        today = self._clock()
        convo: list[dict] = [{"role": "system", "content": _system(today)}]
        convo += self._memory.load(session_id, limit=16)
        convo.append({"role": "user", "content": message})

        ctx: dict = {}
        changed = False
        trace: list[dict] = []
        confirmed = self._confirmed(message)
        final: str | None = None

        for step in range(self._max_steps):
            try:
                turn = self._llm.chat(convo, self._registry.schemas())
            except Exception as e:  # noqa: BLE001
                if step == 0:      # tool-calling unavailable → plan-and-execute fallback
                    rep = self._executor.handle(message)
                    final = rep.reply
                    changed = changed or rep.changed
                else:
                    final = f"⚠ The local model had trouble responding ({e})."
                break

            if not turn.tool_calls:
                final = (turn.content or "").strip() or "Done."
                break

            convo.append({"role": "assistant", "content": turn.content or "",
                          "tool_calls": [{"function": {"name": tc.name, "arguments": tc.args}}
                                         for tc in turn.tool_calls]})
            for tc in turn.tool_calls:
                tool = self._registry.get(tc.name)
                yield {"type": "status", "text": _STATUS.get(tc.name, f"Running {tc.name}…")}
                if tool is None:
                    obs = f"Unknown tool '{tc.name}'."
                elif tool.destructive and not confirmed:
                    obs = (f"NOT executed — '{tc.name}' is destructive. Ask the user to "
                           f"resend with the word 'confirm'.")
                else:
                    try:
                        reply = self._executor.run_tool(
                            tc.name, tc.args or {}, confirmed, message, today, ctx)
                        obs = reply.reply
                        changed = changed or reply.changed
                    except Exception as e:  # noqa: BLE001
                        obs = f"Tool error: {e}"
                trace.append({"name": tc.name, "result": obs})
                yield {"type": "tool", "name": tc.name, "result": obs[:600]}
                convo.append({"role": "tool", "name": tc.name, "content": obs})

        if final is None:                      # ran out of steps → force a text answer
            try:
                convo.append({"role": "user", "content":
                              "Now write the final answer in friendly Markdown using ONLY "
                              "the tool results above."})
                turn = self._llm.chat(convo, [])
                final = (turn.content or "").strip() or self._summary(trace)
            except Exception:  # noqa: BLE001
                final = self._summary(trace)

        self._memory.append(session_id, "user", message)
        self._memory.append(session_id, "assistant", final)
        yield {"type": "answer", "text": final}
        yield {"type": "done", "session_id": session_id, "changed": changed, "trace": trace}

    @staticmethod
    def _summary(trace: list[dict]) -> str:
        if not trace:
            return "I couldn't complete that — please try rephrasing."
        tail = "\n\n".join(f"**{t['name']}**\n{t['result']}" for t in trace[-3:])
        return "Here's what I found:\n\n" + tail

    def handle(self, session_id: str, message: str) -> dict:
        """Non-streaming: drain the event stream into a single result."""
        text, changed, trace, sid = "", False, [], session_id
        for ev in self.run(session_id, message):
            if ev["type"] == "answer":
                text = ev["text"]
            elif ev["type"] == "done":
                changed, trace, sid = ev["changed"], ev["trace"], ev["session_id"]
        return {"session_id": sid, "reply": text, "changed": changed, "trace": trace}
