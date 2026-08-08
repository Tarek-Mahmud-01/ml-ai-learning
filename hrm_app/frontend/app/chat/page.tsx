"use client";

import { useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";

type Msg = { role: "user" | "bot"; text: string; kind?: string | null; changed?: boolean };

const CHIPS: { group: string; items: string[] }[] = [
  { group: "Real data", items: ["import real data", "train", "check E100017 last two months"] },
  { group: "Learn", items: ["how does training work?", "supervised vs unsupervised"] },
  { group: "Employees", items: ["list employees", "add employee Rakib rate 22", "set E100017 base rate to 25"] },
  { group: "Attendance", items: ["add attendance E100 2024-06-20 present 09:00 18:00 pay 160", "set E100 2024-06-20 checkout to 19:00"] },
  { group: "Payroll", items: ["set E100 2024-06-20 pay to 190"] },
  { group: "Check", items: ["check E100 june", "show E100 2024-06-20"] },
  { group: "Training", items: ["E100 2024-06-20 is wrong", "retrain from my labels"] },
];

const GREETING: Msg = {
  role: "bot",
  text:
    "Hi! I'm your HRM assistant. Type naturally — e.g. 'check employee 100 for " +
    "the last two months and tell me if anything looks bad', or 'raise E102's pay " +
    "rate to 30'. I can manage employees, attendance, payroll, and the model. " +
    "Tap a command below, or just ask.",
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Msg[]>([GREETING]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const logRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  async function send(text: string) {
    const msg = text.trim();
    if (!msg || busy) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", text: msg }]);
    setBusy(true);
    try {
      const r = await api.chat(msg);
      setMessages((m) => [...m, { role: "bot", text: r.reply, kind: r.kind, changed: r.changed }]);
    } catch {
      setMessages((m) => [
        ...m,
        { role: "bot", text: "⚠ Cannot reach the API. Is the backend running on port 8010?" },
      ]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <p className="eyebrow">Assistant</p>
      <h1>Chat</h1>
      <p className="sub">
        Run the whole system by chatting — manage data and train the model. Every
        change is validated and logged; deletes ask you to confirm.
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
              {m.text}
              {m.role === "bot" && m.kind ? (
                <div>
                  <span className="kind">active model: {m.kind}</span>
                </div>
              ) : null}
              {m.role === "bot" && m.changed ? <div className="changed">updated ✓</div> : null}
            </div>
          ))}
          {busy ? <div className="bubble bot dim">…</div> : null}
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
            placeholder="Ask naturally… e.g. 'check E100 for the last two months'"
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
