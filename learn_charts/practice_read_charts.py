r"""
=====================================================================
PRACTICE — Can you READ your charts?  (quiz)
=====================================================================
Open the charts in reports/ first, read README_charts_explained.md,
then answer below by replacing None with your answer.

Run with:
  python learn_charts/practice_read_charts.py
=====================================================================
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")  # so ✅ ❌ show on any terminal
except Exception:
    pass

score = []
def check(q, condition):
    print(f"  {q:<48} {'PASS ✅' if condition else 'TRY AGAIN ❌'}")
    score.append(condition)

print("=" * 58)
print("QUIZ — read the charts, then answer")
print("=" * 58)

# -------------------------------------------------------------
# Q1 — In the heatmap, Profit and Cost_Price had a number of -0.48.
#      Does higher Cost_Price make profit go UP or DOWN?
#      Answer with the word "UP" or "DOWN".
# -------------------------------------------------------------
q1 = None   # YOUR ANSWER  ("UP" or "DOWN")
check("Q1: higher Cost_Price -> profit goes...", q1 == "DOWN")

# -------------------------------------------------------------
# Q2 — In revenue_by_category, which category earns the MOST revenue?
#      Answer: "Food", "Electronics", "Apparel", or "Furniture".
# -------------------------------------------------------------
q2 = None   # YOUR ANSWER
check("Q2: highest revenue category", q2 == "Electronics")

# -------------------------------------------------------------
# Q3 — In feature importance, which column was MOST important to the AI?
#      Answer: "Unit_Price", "Discount", "Hour", ...
# -------------------------------------------------------------
q3 = None   # YOUR ANSWER
check("Q3: most important feature", q3 == "Unit_Price")

# -------------------------------------------------------------
# Q4 — In the Profit histogram, the hill is centered near which number?
#      (Most sales made a profit close to...) Answer with a number.
# -------------------------------------------------------------
q4 = None   # YOUR ANSWER (a number)
check("Q4: profit histogram center", q4 == 0)

# -------------------------------------------------------------
# Q5 — In the decision tree, the VERY FIRST question is about which column?
#      Answer: "Unit_Price" or "Cost_Price".
# -------------------------------------------------------------
q5 = None   # YOUR ANSWER
check("Q5: first question in the tree", q5 == "Unit_Price")

# -------------------------------------------------------------
print("-" * 58)
passed = sum(score)
print(f"  SCORE: {passed}/{len(score)}")
if passed == len(score):
    print("  🎉 You can READ charts now — a real data scientist skill!")
else:
    print("  Re-open the charts + README, then try the ❌ ones again.")
print("=" * 58)

# =====================================================================
# ANSWERS (peek only if stuck):
#   Q1 DOWN  |  Q2 Electronics  |  Q3 Unit_Price  |  Q4 0  |  Q5 Unit_Price
# =====================================================================
