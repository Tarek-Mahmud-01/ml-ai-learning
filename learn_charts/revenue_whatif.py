r"""
=====================================================================
REVENUE "WHAT-IF" SIMULATOR
=====================================================================
Uses your trained model to answer:
  "If I change units / price / discount, what happens to revenue?"

Run with:
  python learn_charts/revenue_whatif.py
=====================================================================
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import joblib
import pandas as pd

model = joblib.load("models/linear_regression.joblib")
FEATURES = ["Units_Sold", "Unit_Price", "Discount", "Cost_Price"]


def revenue(units, price, discount, cost):
    """Ask the model to predict revenue for one sale."""
    row = pd.DataFrame([[units, price, discount, cost]], columns=FEATURES)
    return model.predict(row)[0]


# -------------------------------------------------------------
# A "normal" average sale from your data
# -------------------------------------------------------------
base = dict(units=26, price=256, discount=0.10, cost=151)
base_rev = revenue(**base)

print("=" * 58)
print("REVENUE WHAT-IF SIMULATOR")
print("=" * 58)
print(f"Starting sale: {base['units']} units, ${base['price']} price, "
      f"{base['discount']*100:.0f}% discount, ${base['cost']} cost")
print(f"Predicted revenue = ${base_rev:,.2f}")
print()

# -------------------------------------------------------------
# Test different ideas and compare
# -------------------------------------------------------------
ideas = [
    ("Sell 5 MORE units",           dict(base, units=31)),
    ("Raise price by $20",          dict(base, price=276)),
    ("Cut discount 10% -> 5%",      dict(base, discount=0.05)),
    ("Remove discount (0%)",        dict(base, discount=0.00)),
    ("BEST: +5 units & no discount", dict(base, units=31, discount=0.00)),
]

print(f"{'IDEA':<32}{'REVENUE':>12}{'CHANGE':>12}")
print("-" * 58)
for name, params in ideas:
    r = revenue(**params)
    diff = r - base_rev
    sign = "+" if diff >= 0 else ""
    print(f"{name:<32}${r:>10,.0f}{sign}{diff:>10,.0f}")

print("-" * 58)
print("Try it yourself: open this file and change the numbers in")
print("`base` or add your own idea to the `ideas` list, then re-run.")
print("=" * 58)
