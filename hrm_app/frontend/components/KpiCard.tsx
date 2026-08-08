export function KpiCard({
  label,
  value,
  sub,
  alert,
}: {
  label: string;
  value: string | number;
  sub?: string;
  alert?: boolean;
}) {
  return (
    <div className={`kpi ${alert ? "alert" : ""}`}>
      <div className="k">{label}</div>
      <div className="v">
        {value}
        {sub ? <small> {sub}</small> : null}
      </div>
    </div>
  );
}
