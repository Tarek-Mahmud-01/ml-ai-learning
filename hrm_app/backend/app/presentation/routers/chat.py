"""Chat endpoint — thin: hand the message to the assistant, return its reply."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ...application.use_cases.chat_assistant import ChatAssistant
from ..deps import chat_assistant_uc
from ..schemas import ChatReplyOut, ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatReplyOut)
def chat(
    body: ChatRequest,
    uc: ChatAssistant = Depends(chat_assistant_uc),
) -> ChatReplyOut:
    r = uc.handle(body.message)
    return ChatReplyOut(reply=r.reply, kind=r.kind, changed=r.changed)
