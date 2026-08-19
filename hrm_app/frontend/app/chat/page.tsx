"use client";

import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { api } from "@/lib/api";
import type { AgentEvent, TraceStep } from "@/lib/types";

type Msg = {
  role: "user" | "bot";
  text: string;
  status?: string;          // live progress line while working
  trace?: TraceStep[];
  done?: boolean;
};

const CHIPS: { group: string; items: string[] }[] = [
  { group: "Ask anything", items: [
      "who worked the most overtime last month? top 3",
      "last month unpaid list",
      "find the employee whose id ends 17",
      "payslip E100017 last month",
      "make 5 employees salary last month and check payslips",
      "set merge window to 90 seconds",
  ] },
  { group: "Real data", items: ["import real data", "train", "check E100017 last two months"] },
  { group: "Learn", items: ["how does training work?", "supervised vs unsupervised"] },
];

const GREETING: Msg = {
  role: "bot",
  done: true,
  text:
    "Hi! I'm your **HRM agent** 🤖 — ask me anything about your people and payroll, " +
    "in one message, even messy. I'll use my tools, think it through, and answer.\n\n" +
    "Try _“who worked the most overtime last month?”_, _“last month unpaid list”_, " +
    "or _“find employee 17”_.",
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Msg[]>([GREETING]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const logRef = useRef<HTMLDivElement>(null);
  const sessionRef = useRef<string | null>(null);

  useEffect(() => {
    sessionRef.current = localStorage.getItem("hrm_session") || null;
  }, []);

  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  function patchBot(patch: Partial<Msg> | ((b: Msg) => Partial<Msg>)) {
    setMessages((ms) => {
      const copy = [...ms];
      for (let i = copy.length - 1; i >= 0; i--) {
        if (copy[i].role === "bot") {
          const p = typeof patch === "function" ? patch(copy[i]) : patch;
          copy[i] = { ...copy[i], ...p };
          break;
        }
      }
      return copy;
    });
  }

  function typeOut(full: string) {
    let i = 0;
    const step = () => {
      i = Math.min(full.length, i + 3);
      patchBot({ text: full.slice(0, i), status: "" });
      if (i < full.length) setTimeout(step, 10);
      else patchBot({ done: true });
    };
    step();
  }

  async function send(text: string) {
    const msg = text.trim();
    if (!msg || busy) return;
    setInput("");
    setMessages((m) => [
      ...m,
      { role: "user", text: msg },
      { role: "bot", text: "", status: "Thinking…", trace: [], done: false },
    ]);
    setBusy(true);
    try {
      await api.chatStream(msg, sessionRef.current, (ev: AgentEvent) => {
        if (ev.type === "status") {
          patchBot({ status: ev.text || "" });
        } else if (ev.type === "tool") {
          patchBot((b) => ({
            trace: [...(b.trace || []), { name: ev.name || "", result: ev.result || "" }],
          }));
        } else if (ev.type === "answer") {
          typeOut(ev.text || "");
        } else if (ev.type === "done") {
          if (ev.session_id) {
            sessionRef.current = ev.session_id;
            localStorage.setItem("hrm_session", ev.session_id);
          }
        }
      });
    } catch {
      patchBot({ text: "⚠ Cannot reach the agent. Is the backend running on port 8010?", status: "", done: true });
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <p className="eyebrow">Assistant</p>
      <h1>Agent</h1>
      <p className="sub">
        A real tool-using agent — it reasons, calls the right tools, remembers the
        conversation, and answers. Every change is logged; deletes ask you to confirm.
      </p>

      <div className="chips">
        {CHIPS.map((g) => (
          <div key={g.group} style={{ display: "contents" }}>
            <div className="chip-group">{g.group}</div>
            {g.items.map((c) => (
              <button key={c} className="chip" onClick={() => send(c)} disabled={busy}>
                {c}
              </button>
            ))}
          </div>
        ))}
      </div>

      <div className="panel panel-pad chat">
        <div className="chat-log" ref={logRef}>
          {messages.map((m, i) => (
            <div key={i} className={`bubble ${m.role}`}>
              {m.role === "bot" ? (
                <>
                  {m.text ? (
                    <div className="md">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.text}</ReactMarkdown>
                    </div>
                  ) : null}
                  {!m.done && m.status ? (
                    <div className="agent-status">
                      <span className="dot" /> {m.status}
                    </div>
                  ) : null}
                  {m.trace && m.trace.length > 0 ? (
                    <details className="trace">
                      <summary>how I did it · {m.trace.length} step{m.trace.length > 1 ? "s" : ""}</summary>
                      {m.trace.map((t, j) => (
                        <div className="trace-step" key={j}>
                          <b>{t.name}</b>
                          <pre>{t.result}</pre>
                        </div>
                      ))}
                    </details>
                  ) : null}
                </>
              ) : (
                m.text
              )}
            </div>
          ))}
        </div>

        <form
          className="chat-input"
          onSubmit={(e) => {
            e.preventDefault();
            send(input);
          }}
        >
          <input
            className="input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask anything… e.g. 'who worked the most overtime last month?'"
            autoFocus
          />
          <button className="btn btn-primary" type="submit" disabled={busy}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
