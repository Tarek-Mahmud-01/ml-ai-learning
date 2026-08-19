"""
Chat endpoints:
- POST /chat         — non-stream, single-intent assistant (fallback + tests).
- POST /chat/stream  — the tool-calling AGENT, streamed as SSE (status/tool/answer/done).
"""
from __future__ import annotations

import json
from uuid import uuid4

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from ...application.agent.hrm_agent import HrmAgent
from ...application.use_cases.chat_assistant import ChatAssistant
from ..deps import chat_assistant_uc, hrm_agent_uc
from ..schemas import ChatReplyOut, ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatReplyOut)
def chat(
    body: ChatRequest,
    uc: ChatAssistant = Depends(chat_assistant_uc),
) -> ChatReplyOut:
    r = uc.handle(body.message)
    return ChatReplyOut(reply=r.reply, kind=r.kind, changed=r.changed)


@router.post("/stream")
def chat_stream(
    body: ChatRequest,
    agent: HrmAgent = Depends(hrm_agent_uc),
) -> StreamingResponse:
    session_id = body.session_id or uuid4().hex
    message = body.message

    def events():
        for ev in agent.run(session_id, message):
            yield f"data: {json.dumps(ev)}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache",
                                      "X-Accel-Buffering": "no"})
