r"""
=====================================================================
HRM DETECTIVE — REAL TRAINED AI MODEL (free, local, no API)
=====================================================================
This is REAL machine learning:
  - We give the model EXAMPLES of correct and wrong payslips.
  - The model LEARNS the pattern by itself (we do NOT hard-code rules).
  - Then it can judge NEW payslips it has never seen.

100% free. Runs on YOUR computer. No internet, no paid API.

Run with:
  python hrm_detective/train_model.py
=====================================================================
"""
import sys, os
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

HERE = os.path.dirname(__file__)
CSV = os.path.join(HERE, "payslips.csv")
MODEL_OUT = os.path.join(HERE, "hrm_model.joblib")


def hour_of(t):
    h, m = str(t).split(":")
    return int(h) + int(m) / 60.0


def main():
    if not os.path.exists(CSV):
        print("payslips.csv not found. Run generate_payslips.py first.")
        return

    df = pd.read_csv(CSV)

    # -------------------------------------------------------------
    # STEP 1 — FEATURE ENGINEERING
    # Turn each payslip into numbers the model can learn from.
    # We give RAW facts (hours, pay, pay-per-hour) and let the model
    # figure out what "wrong" looks like. We do NOT tell it the rule.
    # -------------------------------------------------------------
    df["presence_hours"] = df["Check_Out"].map(hour_of) - df["Check_In"].map(hour_of)
    df["pay_per_hour"] = df["Reported_Pay"] / df["presence_hours"].replace(0, np.nan)
    df["pay_per_hour"] = df["pay_per_hour"].fillna(0)

    features = ["presence_hours", "Reported_Pay", "pay_per_hour"]
    X = df[features]

    # -------------------------------------------------------------
    # STEP 2 — THE ANSWER (label): was this payslip actually wrong?
    # 1 = wrong (fraud/mistake), 0 = correct.
    # (In real life you would get these labels from an audit.)
    # -------------------------------------------------------------
    y = (df["_secret_label"] != "normal").astype(int)

    print("=" * 60)
    print("TRAINING A REAL AI MODEL ON YOUR HRM DATA")
    print("=" * 60)
    print(f"Total payslips: {len(df)}   (wrong: {y.sum()}, correct: {len(y)-y.sum()})")
    print(f"Features the model will learn from: {features}")
    print()

    # -------------------------------------------------------------
    # STEP 3 — SPLIT: learn on 70%, test on 30% it has NEVER seen
    # -------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y)

    # -------------------------------------------------------------
    # STEP 4 — TRAIN (this is the "learning"!)
    # class_weight="balanced" because wrong payslips are rare.
    # -------------------------------------------------------------
    print("Training... (the model is learning the pattern by itself)")
    model = RandomForestClassifier(
        n_estimators=100, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)

    # -------------------------------------------------------------
    # STEP 5 — TEST on unseen payslips
    # -------------------------------------------------------------
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    print(f"\nAccuracy on NEW unseen payslips: {acc*100:.1f}%")
    print("\nDetailed report (0=correct, 1=wrong):")
    print(classification_report(y_test, pred, zero_division=0))

    # -------------------------------------------------------------
    # STEP 6 — What did the model learn was important?
    # -------------------------------------------------------------
    print("What the model learned to look at:")
    for f, imp in sorted(zip(features, model.feature_importances_),
                         key=lambda t: -t[1]):
        bar = "#" * int(imp * 40)
        print(f"   {f:<16} {imp:.2f}  {bar}")

    # -------------------------------------------------------------
    # STEP 7 — Save the trained model (your "AI brain")
    # -------------------------------------------------------------
    joblib.dump({"model": model, "features": features}, MODEL_OUT)
    print(f"\nSaved trained model -> {MODEL_OUT}")

    # -------------------------------------------------------------
    # STEP 8 — Use it on 3 brand-new made-up payslips
    # -------------------------------------------------------------
    print("\n" + "=" * 60)
    print("TRY THE TRAINED MODEL ON NEW PAYSLIPS")
    print("=" * 60)
    tests = pd.DataFrame([
        {"presence_hours": 9,  "Reported_Pay": 160, "pay_per_hour": 160/9},   # normal
        {"presence_hours": 9,  "Reported_Pay": 60,  "pay_per_hour": 60/9},    # underpaid
        {"presence_hours": 20, "Reported_Pay": 490, "pay_per_hour": 490/20},  # impossible hours
    ])
    labels = ["normal 9h/$160", "suspicious 9h/$60", "impossible 20h/$490"]
    verdict = model.predict(tests[features])
    for name, v in zip(labels, verdict):
        print(f"   {name:<24} -> {'WRONG ❌' if v == 1 else 'OK ✅'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
