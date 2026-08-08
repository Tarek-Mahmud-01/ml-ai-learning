"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { Employee } from "@/lib/types";

export default function Dashboard() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [month, setMonth] = useState("2024-06");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<string>("");
  const [error, setError] = useState<string>("");

  async function load() {
    setLoading(true);
    setError("");
    try {
      setEmployees(await api.listEmployees());
    } catch (e) {
      setError("Cannot reach the API. Is the backend running on port 8010?");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function onSeed() {
    setBusy(true);
    setMsg("");
    setError("");
    try {
      const r = await api.seed(month);
      setMsg(
        `Seeded ${r.employees} employees · ${r.attendance_days} days · ${r.injected_fraud} hidden problems.`
      );
      await load();
    } catch {
      setError("Seeding failed.");
    } finally {
      setBusy(false);
    }
  }

  async function onTrain() {
    setBusy(true);
    setMsg("");
    setError("");
    try {
      const r = await api.train();
      setMsg(`Detector trained on ${r.samples_trained} worked days.`);
    } catch {
      setError("Training failed.");
    } finally {
      setBusy(false);
    }
  }

  async function onImport() {
    setBusy(true);
    setMsg("");
    setError("");
    try {
      const r = await api.importReal();
      setMsg(
        `Imported ${r.employees} real employees · ${r.attendance_days} days ` +
          `(${r.date_from} → ${r.date_to}). Merged ${r.punches_merged_away} ` +
          `duplicate punches (${r.merge_seconds}s window); ` +
          `${r.missing_punch_days} missing-punch days. Now click Train detector.`
      );
      await load();
    } catch {
      setError("Import failed. Is the biometric SQL file at the configured path?");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <p className="eyebrow">Dashboard</p>
      <h1>Employees</h1>
      <p className="sub">
        Pick an employee to audit their month — the checker combines your pay
        rules with an AI anomaly model.
      </p>

      <div className="panel panel-pad">
        <h2>Set up demo data</h2>
        <div className="row">
          <div className="field">
            <label htmlFor="month">Month</label>
            <input
              id="month"
              className="input"
              value={month}
              onChange={(e) => setMonth(e.target.value)}
              placeholder="YYYY-MM"
              style={{ width: 130 }}
            />
          </div>
          <button className="btn btn-primary" onClick={onSeed} disabled={busy}>
            {busy ? "Working…" : "Generate data"}
          </button>
          <button className="btn" onClick={onTrain} disabled={busy}>
            Train detector
          </button>
          <div className="spacer" />
        </div>
        {msg ? (
          <p className="msg" style={{ marginTop: ".9rem" }}>
            {msg}
          </p>
        ) : null}
        {error ? (
          <p className="msg" style={{ marginTop: ".9rem", color: "#0a0a0a" }}>
            ⚠ {error}
          </p>
        ) : null}
      </div>

      <div className="panel panel-pad" style={{ marginTop: "1.25rem" }}>
        <h2>Use your real data</h2>
        <p className="sub" style={{ marginTop: 0 }}>
          Import the real biometric punches (ZKTeco BioTime). Duplicate punches
          within ~60&nbsp;seconds are merged to one, and each day becomes
          first-in / last-out. Pay starts at a baseline rate you can fine-tune
          per employee in <a className="link" href="/chat">Chat</a>. This
          replaces the demo data.
        </p>
        <div className="row">
          <button className="btn btn-primary" onClick={onImport} disabled={busy}>
            {busy ? "Working…" : "Import real data"}
          </button>
          <button className="btn" onClick={onTrain} disabled={busy}>
            Train detector
          </button>
          <div className="spacer" />
        </div>
      </div>

      <div className="panel" style={{ marginTop: "1.25rem" }}>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th className="num">Base rate</th>
                <th className="num">OT rate</th>
                <th className="num">Work goal</th>
                <th>Shift start</th>
                <th>Weekend</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={8} className="empty">
                    Loading…
                  </td>
                </tr>
              ) : employees.length === 0 ? (
                <tr>
                  <td colSpan={8} className="empty">
                    No employees yet. Click <b>Generate data</b> above to start.
                  </td>
                </tr>
              ) : (
                employees.map((e) => (
                  <tr key={e.id}>
                    <td className="mono">{e.id}</td>
                    <td>{e.name}</td>
                    <td className="num mono">${e.base_rate}</td>
                    <td className="num mono">${e.ot_rate}</td>
                    <td className="num mono">{e.work_goal}h</td>
                    <td className="mono">{e.shift_start}</td>
                    <td className="mono dim">{e.weekend_days}</td>
                    <td className="num">
                      <a className="link" href={`/employees/${e.id}?month=${month}`}>
                        View report →
                      </a>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
