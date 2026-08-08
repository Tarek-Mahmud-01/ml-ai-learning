"""
=====================================================================
DAY 2 EXAMPLE — Linear Regression (the EASY way)
=====================================================================
Big idea: Linear Regression draws the BEST straight line through data,
then uses that line to PREDICT new answers.

The line has a simple formula:   y = m * x + b
   x = input (the clue)          e.g. hours studied
   y = output (the answer)       e.g. exam score
   m = slope (how steep)         "each hour adds this many points"
   b = intercept (start value)   "score if you studied 0 hours"

Run with:
  python learn_charts/day2_regression_example.py
=====================================================================
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

print("=" * 58)
print("DAY 2 — LINEAR REGRESSION (study hours -> exam score)")
print("=" * 58)

# -------------------------------------------------------------
# STEP 1 — Tiny, easy data
# Each student: how many HOURS they studied, and their SCORE.
# -------------------------------------------------------------
hours  = np.array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(-1, 1)  # X (the clue)
scores = np.array([52, 56, 61, 66, 70, 75, 79, 84])          # y (the answer)

print("Data (hours -> score):")
for h, s in zip(hours.ravel(), scores):
    print(f"   studied {h}h  ->  scored {s}")
print()

# -------------------------------------------------------------
# STEP 2 — TRAIN: let the model find the best line
# .fit() = "learn the pattern" (find best m and b)
# -------------------------------------------------------------
model = LinearRegression()
model.fit(hours, scores)

m = model.coef_[0]        # slope
b = model.intercept_      # intercept
print("STEP 2 — The model learned this line:")
print(f"   score = {m:.2f} * hours + {b:.2f}")
print(f"   -> meaning: each extra hour adds about {m:.1f} points.")
print(f"   -> with 0 hours, expected score is about {b:.1f}.")
print()

# -------------------------------------------------------------
# STEP 3 — PREDICT: use the line for NEW inputs
# -------------------------------------------------------------
print("STEP 3 — Predict scores for NEW study hours:")
for h in [4.5, 9, 10]:
    pred = model.predict([[h]])[0]
    print(f"   study {h}h  ->  predicted score = {pred:.1f}")
print()

# -------------------------------------------------------------
# STEP 4 — HOW GOOD is the line? (R2 score, 1.0 = perfect)
# -------------------------------------------------------------
r2 = r2_score(scores, model.predict(hours))
print("STEP 4 — Accuracy check:")
print(f"   R2 score = {r2:.4f}   (1.0 = perfect line, 0 = useless)")
print(f"   -> {r2*100:.1f}% of the pattern is explained by the line. Great!")
print()

print("=" * 58)
print("WHAT YOU LEARNED")
print("=" * 58)
print("1. Regression = find best straight line:  y = m*x + b")
print("2. .fit()  = learn the line from data (training)")
print("3. .predict() = use the line to guess new answers")
print("4. R2 score  = how well the line fits (closer to 1 = better)")
print("Your day2_linear_regression.py does the SAME thing, but with")
print("4 clues (Units_Sold, Unit_Price, Discount, Cost_Price) to")
print("predict Revenue instead of just 1 clue.")
print("=" * 58)
