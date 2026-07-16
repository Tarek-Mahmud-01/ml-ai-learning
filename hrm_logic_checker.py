import pandas as pd
import numpy as np

# --- GLOBAL SETTINGS (The Rules) ---
SHIFT_TOTAL_HOURS = 9.0  # 8 hours work + 1 hour lunch
WORK_HOURS_GOAL = 8.0
LUNCH_BREAK_HOURS = 1.0
BASE_RATE_PER_HOUR = 20.0
OT_RATE_PER_HOUR = 30.0  # Overtime is paid higher!

def calculate_payslip_logic(check_in, check_out, reported_pay):
    """
    This function follows your HR rules to calculate what the pay SHOULD be.
    """
    # 1. Calculate Total Presence (Hours)
    in_time = pd.to_datetime(check_in)
    out_time = pd.to_datetime(check_out)
    total_presence = (out_time - in_time).total_seconds() / 3600
    
    # 2. Calculate Overtime (Any time after 9 hours)
    overtime_hours = max(0, total_presence - SHIFT_TOTAL_HOURS)
    
    # 3. Regular Work Hours (Max 8 hours of base pay)
    # We subtract lunch if they stayed at least 1 hour
    actual_work_hours = min(WORK_HOURS_GOAL, max(0, total_presence - LUNCH_BREAK_HOURS))
    
    # 4. Math: Total Expected Pay
    expected_base_pay = actual_work_hours * BASE_RATE_PER_HOUR
    expected_ot_pay = overtime_hours * OT_RATE_PER_HOUR
    total_expected_pay = expected_base_pay + expected_ot_pay
    
    # 5. The Checker: Is there a discrepancy?
    difference = reported_pay - total_expected_pay
    is_wrong = abs(difference) > 0.01  # True if there is an error
    
    return {
        "Total_Hours": round(total_presence, 2),
        "OT_Hours": round(overtime_hours, 2),
        "Expected_Pay": round(total_expected_pay, 2),
        "Difference": round(difference, 2),
        "Status": "[WRONG]" if is_wrong else "[CORRECT]"
    }

# --- TEST DATA ---
# Let's check 3 different employees
test_data = [
    {"Name": "Emp_A", "In": "09:00", "Out": "18:00", "Paid": 160.0}, # Normal 9h (8h work)
    {"Name": "Emp_B", "In": "09:00", "Out": "20:00", "Paid": 220.0}, # 11h (9h shift + 2h OT) -> 160 + (2*30)=220
    {"Name": "Emp_C", "In": "09:00", "Out": "18:00", "Paid": 100.0}, # Error! (Should be 160)
]

print(f"{'Name':<10} | {'Hours':<6} | {'OT':<4} | {'Expected':<10} | {'Status':<10}")
print("-" * 55)

for emp in test_data:
    result = calculate_payslip_logic(emp["In"], emp["Out"], emp["Paid"])
    print(f"{emp['Name']:<10} | {result['Total_Hours']:<6} | {result['OT_Hours']:<4} | ${result['Expected_Pay']:<9} | {result['Status']}")
