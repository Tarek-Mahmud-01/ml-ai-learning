"""Ports the agent depends on — implemented in infrastructure."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class ToolCall:
    name: str
    args: dict = field(default_factory=dict)


@dataclass
class LlmTurn:
    """One model turn: either tool calls to run, or a final text answer."""
    tool_calls: list[ToolCall] = field(default_factory=list)
    content: str = ""


class LlmAgentClient(Protocol):
    def chat(self, messages: list[dict], tools: list[dict]) -> LlmTurn:
        """One tool-calling turn against the model."""
        ...


class ConversationStore(Protocol):
    def load(self, session_id: str, limit: int = 20) -> list[dict]:
        """Return recent {role, content} messages for a session, oldest first."""
        ...

    def append(self, session_id: str, role: str, content: str) -> None:
        ...
