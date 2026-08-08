// The ONLY file that talks to the backend. Components never fetch directly.
import type {
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
};
