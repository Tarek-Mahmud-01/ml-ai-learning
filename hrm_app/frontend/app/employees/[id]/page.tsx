"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { MonthReport } from "@/lib/types";
import { StatusBadge } from "@/components/StatusBadge";
import { KpiCard } from "@/components/KpiCard";

const money = (n: number) =>
  `$${n.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

export default function ReportPage({ params }: { params: { id: string } }) {
  const [month, setMonth] = useState("2024-06");
  const [report, setReport] = useState<MonthReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const m = new URLSearchParams(window.location.search).get("month");
    if (m) setMonth(m);
  }, []);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      setError("");
      try {
        const r = await api.getReport(params.id, month);
        if (alive) setReport(r);
      } catch {
        if (alive) setError("Could not load this report. Try generating data first.");
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, [params.id, month]);

  return (
    <div>
      <a className="back" href="/">
        ← All employees
      </a>

      {loading ? (
        <div className="empty">Loading report…</div>
      ) : error ? (
        <div className="empty">{error}</div>
      ) : report ? (
        <>
          <div style={{ marginTop: ".8rem" }}>
            <p className="eyebrow" style={{ marginBottom: ".3rem" }}>
              {report.employee_id} · {report.month}
            </p>
            <h1>{report.employee_name}</h1>
          </div>

          <div className="summary">
            {report.summary}
            <div className="rulesnote">Rules applied — {report.rules_note}</div>
          </div>

          <div className="row" style={{ marginBottom: "1.5rem" }}>
            <div className="field">
              <label htmlFor="m">Month</label>
              <input
                id="m"
                className="input"
                value={month}
                onChange={(e) => setMonth(e.target.value)}
                style={{ width: 130 }}
              />
            </div>
          </div>

          <div className="kpis" style={{ marginBottom: "1.5rem" }}>
            <KpiCard label="Present" value={report.present_days} sub="days" />
            <KpiCard label="Absent" value={report.absent_days} sub="days" />
            <KpiCard label="Late" value={report.late_days} sub="days" />
            <KpiCard label="Leave" value={report.leave_days} sub="days" />
            <KpiCard label="Total hours" value={report.total_hours} sub="h" />
            <KpiCard label="Overtime" value={report.ot_hours} sub="h" />
            <KpiCard label="Paid" value={money(report.total_paid)} />
            <KpiCard label="Expected" value={money(report.total_expected)} />
            <KpiCard
              label="Flagged"
              value={report.flagged_days}
              sub="days"
              alert={report.flagged_days > 0}
            />
            <KpiCard
              label="Money at risk"
              value={money(report.money_at_risk)}
              alert={report.money_at_risk > 0}
            />
          </div>

          <div className="panel">
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>In – Out</th>
                    <th className="num">Hrs</th>
                    <th className="num">OT</th>
                    <th className="num">Expected</th>
                    <th className="num">Paid</th>
                    <th className="num">Diff</th>
                    <th>Status</th>
                    <th>Reason &amp; rule applied</th>
                  </tr>
                </thead>
                <tbody>
                  {report.days.map((d) => {
                    const flagged = d.rule_flag || d.ml_flag;
                    return (
                      <tr key={d.day} className={flagged ? "flagged" : ""}>
                        <td className="mono">{d.day.slice(8)}</td>
                        <td className="dim">{d.day_type}</td>
                        <td className="mono dim">
                          {d.check_in && d.check_out
                            ? `${d.check_in}–${d.check_out}`
                            : "—"}
                        </td>
                        <td className="num mono">{d.presence_hours || "—"}</td>
                        <td className="num mono">{d.ot_hours || "—"}</td>
                        <td className="num mono">{money(d.expected_pay)}</td>
                        <td className="num mono">{money(d.reported_pay)}</td>
                        <td className="num mono">
                          {d.diff === 0 ? "—" : (d.diff > 0 ? "+" : "") + d.diff.toFixed(2)}
                        </td>
                        <td>
                          <StatusBadge status={d.status} />
                        </td>
                        <td>
                          {d.reason}
                          <div className="mono dim" style={{ fontSize: ".72rem" }}>
                            {d.rule_note}
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          <div className="pill-legend">
            <span>Legend:</span>
            <StatusBadge status="OK" /> <span>correct</span>
            <StatusBadge status="RULE-FLAG" /> <span>rules say wrong</span>
            <StatusBadge status="ML-FLAG" /> <span>AI says unusual</span>
            <StatusBadge status="BOTH" /> <span>both agree</span>
          </div>
        </>
      ) : null}
    </div>
  );
}
