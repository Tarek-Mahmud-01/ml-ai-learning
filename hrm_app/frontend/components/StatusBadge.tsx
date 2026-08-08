export function StatusBadge({ status }: { status: string }) {
  const cls =
    status === "OK"
      ? "badge-ok"
      : status === "RULE-FLAG"
      ? "badge-rule"
      : status === "ML-FLAG"
      ? "badge-ml"
      : "badge-both";
  return <span className={`badge ${cls}`}>{status}</span>;
}
