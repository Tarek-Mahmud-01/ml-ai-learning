// TypeScript mirrors of the backend DTOs. Presentation-only.

export interface Employee {
  id: string;
  name: string;
  base_rate: number;
  ot_rate: number;
  work_goal: number;
  shift_start: string;
  weekend_days: string;
}

export interface DayVerdict {
  day: string;
  day_type: string;
  check_in: string | null;
  check_out: string | null;
  presence_hours: number;
  ot_hours: number;
  expected_pay: number;
  reported_pay: number;
  diff: number;
  rule_flag: boolean;
  ml_flag: boolean;
  status: string; // OK | RULE-FLAG | ML-FLAG | BOTH
  reason: string;
  rule_note: string;
}

export interface MonthReport {
  employee_id: string;
  employee_name: string;
  month: string;
  rules_note: string;
  total_days: number;
  present_days: number;
  absent_days: number;
  late_days: number;
  leave_days: number;
  total_hours: number;
  ot_hours: number;
  total_paid: number;
  total_expected: number;
  money_at_risk: number;
  flagged_days: number;
  summary: string;
  days: DayVerdict[];
}

export interface SeedResult {
  month: string;
  employees: number;
  attendance_days: number;
  injected_fraud: number;
}

export interface TrainResult {
  samples_trained: number;
}

export interface ImportResult {
  employees: number;
  attendance_days: number;
  missing_punch_days: number;
  punches_read: number;
  punches_kept: number;
  punches_merged_away: number;
  date_from: string | null;
  date_to: string | null;
  merge_seconds: number;
  default_base_rate: number;
  replaced_demo: boolean;
}

export interface ChatReply {
  reply: string;
  kind?: string | null;
  changed?: boolean;
}
