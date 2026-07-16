# 🏢 HRM Payslip Anomaly Detector Plan

### 🎯 Goal
Detect errors or fraud in employee payslips based on company rules using Machine Learning.

### ⚙️ Global Settings (The "Law")
*   **Total Shift:** 9 Hours (8 Work + 1 Lunch).
*   **Overtime:** Kick-in after 9 hours.
*   **Weekends:** 2 Days (No work expected).

---

### 🛠️ Step 1: Data Preparation (The Wrangling)
We need a dataset with these columns:
1. `Employee_ID`
2. `Date`
3. `Check_In`
4. `Check_Out`
5. `Reported_Pay`
6. `Is_Weekend` (Boolean)

### 🧪 Step 2: Logic Engineering
The AI doesn't know about "Lunch breaks" automatically. We have to teach it:
*   `Total_Presence` = `Check_Out` - `Check_In`
*   `Expected_Pay` = (Base_Rate * 8) + (OT_Rate * (Total_Presence - 9))

### 🤖 Step 3: The Model (The Detective)
We will use an **Anomaly Detection** model (like Isolation Forest).
*   **Normal:** Payslip follows the `Expected_Pay` formula.
*   **Anomaly:** Payslip deviates significantly (e.g., worked 12 hours but paid for 5).

### 📝 Step 4: Output
The model will output:
*   **0 (Normal):** Everything looks good.
*   **1 (Anomaly):** **"ERROR DETECTED!"** Please check Employee X on Date Y.

---

### 🚀 Implementation Strategy
1. **Day 1:** Generate synthetic HRM data following your rules.
2. **Day 2:** Train the AI to recognize "Normal" behavior.
3. **Day 3:** Intentionally insert "Wrong" payslips to see if the AI catches them.
