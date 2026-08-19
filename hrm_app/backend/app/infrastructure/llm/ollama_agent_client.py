"""
Ollama tool-calling client — one agent turn against a local model (free, offline).
Sends messages + tool schemas to /api/chat and returns either tool calls or a final
text answer. The reasoning loop lives in the application HrmAgent.
"""
from __future__ import annotations

import json

import httpx

from ...application.agent.ports import LlmTurn, ToolCall


def _json_objects(text: str) -> list[str]:
    """Extract top-level {...} substrings (brace-matched) from free text."""
    out, i, n = [], 0, len(text)
    while i < n:
        if text[i] == "{":
            depth, j = 0, i
            while j < n:
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                    if depth == 0:
                        out.append(text[i:j + 1])
                        break
                j += 1
            i = j + 1
        else:
            i += 1
    return out


def _tool_calls_from_text(content: str) -> list[ToolCall]:
    """
    Salvage tool calls a small model wrote as TEXT/JSON in `content` instead of
    the structured tool_calls field (a common llama3.1:8b behaviour).
    """
    calls: list[ToolCall] = []
    for blob in _json_objects(content):
        try:
            obj = json.loads(blob)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict) or "name" not in obj:
            continue
        if "parameters" not in obj and "arguments" not in obj:
            continue                     # require an args key → avoids false positives
        args = obj.get("parameters") or obj.get("arguments") or {}
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except json.JSONDecodeError:
                args = {}
        calls.append(ToolCall(str(obj["name"]).strip(),
                              args if isinstance(args, dict) else {}))
    return calls


class OllamaAgentClient:
    def __init__(self, host: str, model: str, timeout: float = 120.0) -> None:
        self._url = host.rstrip("/") + "/api/chat"
        self._model = model
        self._timeout = timeout

    def chat(self, messages: list[dict], tools: list[dict]) -> LlmTurn:
        payload: dict = {
            "model": self._model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0},
        }
        if tools:
            payload["tools"] = tools
        r = httpx.post(self._url, json=payload,
                       timeout=httpx.Timeout(self._timeout, connect=3.0))
        r.raise_for_status()
        msg = r.json().get("message", {}) or {}

        calls: list[ToolCall] = []
        for tc in msg.get("tool_calls") or []:
            fn = tc.get("function", {}) or {}
            name = str(fn.get("name", "")).strip()
            if not name:
                continue
            args = fn.get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}
            if not isinstance(args, dict):
                args = {}
            calls.append(ToolCall(name=name, args=args))

        content = str(msg.get("content", "") or "")
        if not calls:                    # model may have written the call as text
            calls = _tool_calls_from_text(content)
            if calls:
                content = ""
        return LlmTurn(tool_calls=calls, content=content)
