// The ONLY file that talks to the backend. Components never fetch directly.
import type {
  AgentEvent,
  ChatReply,
  Employee,
  ImportResult,
  MonthReport,
  SeedResult,
  TrainResult,
} from "./types";

const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8010";

async function jget<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

async function jpost<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export const api = {
  listEmployees: () => jget<Employee[]>("/employees"),
  getEmployee: (id: string) => jget<Employee>(`/employees/${id}`),
  getReport: (id: string, month: string) =>
    jget<MonthReport>(`/employees/${id}/report?month=${month}`),
  seed: (month: string) => jpost<SeedResult>("/admin/seed", { month }),
  importReal: () => jpost<ImportResult>("/admin/import", { replace: true }),
  train: () => jpost<TrainResult>("/admin/train"),
  chat: (message: string) => jpost<ChatReply>("/chat", { message }),

  // Streaming agent: calls onEvent for each SSE event (status/tool/answer/done).
  async chatStream(
    message: string,
    sessionId: string | null,
    onEvent: (ev: AgentEvent) => void
  ): Promise<void> {
    const res = await fetch(`${BASE}/chat/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId }),
    });
    if (!res.body) throw new Error("No response stream");
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const chunks = buffer.split("\n\n");
      buffer = chunks.pop() || "";
      for (const chunk of chunks) {
        const line = chunk.split("\n").find((l) => l.startsWith("data: "));
        if (!line) continue;
        try {
          onEvent(JSON.parse(line.slice(6)) as AgentEvent);
        } catch {
          /* ignore malformed event */
        }
      }
    }
  },
};
