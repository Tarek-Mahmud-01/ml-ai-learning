r"""
=====================================================================
SEE LINEAR REGRESSION LEARN — watch the error shrink
=====================================================================
This shows HOW the best line is found:
  - Try different lines (different slope m).
  - Measure the total squared error for each.
  - The line with the SMALLEST error is the best one.

Run with:
  python learn_charts/see_regression_learn.py
=====================================================================
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
from sklearn.linear_model import LinearRegression

# Simple data: hours studied -> exam score
x = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)
y = np.array([52, 56, 61, 66, 70, 75, 79, 84], dtype=float)


def total_squared_error(m, b):
    """Add up (real - predicted)^2 for every point."""
    predicted = m * x + b
    errors = y - predicted
    return np.sum(errors ** 2)


print("=" * 58)
print("STEP 1 — Try different slopes (m), keep b fixed at 47")
print("=" * 58)
print(f"{'slope m':>8}{'total squared error':>24}")
print("-" * 34)
b = 47
best_m, best_err = None, float("inf")
for m in [1, 2, 3, 4, 4.6, 5, 6, 7]:
    err = total_squared_error(m, b)
    mark = ""
    if err < best_err:
        best_err, best_m = err, m
    print(f"{m:>8.1f}{err:>24,.1f}")

print("-" * 34)
print(f"Smallest error was at slope m = {best_m}  (that's the best guess)")
print("Notice: error goes DOWN, hits a bottom, then goes UP again.")
print("The bottom = the best line. This is what the model searches for.")
print()

# -------------------------------------------------------------
# Now let the real model find the exact best line
# -------------------------------------------------------------
print("=" * 58)
print("STEP 2 — The real model finds the EXACT best line")
print("=" * 58)
model = LinearRegression()
model.fit(x.reshape(-1, 1), y)
m_exact = model.coef_[0]
b_exact = model.intercept_
err_exact = total_squared_error(m_exact, b_exact)
print(f"Best line found:  score = {m_exact:.3f} * hours + {b_exact:.3f}")
print(f"Its total squared error = {err_exact:,.2f}  (smallest possible)")
print()
print("So 'training' just means: search for the m and b with the")
print("least error. That's the whole secret of linear regression. 🎯")
print("=" * 58)
