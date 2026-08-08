r"""
=====================================================================
DAY 5 EXAMPLE — Random Forest (many trees voting)
=====================================================================
Big idea:
  - A DECISION TREE is one flowchart of yes/no questions.
  - One tree alone can be wrong (it "overthinks" / memorizes).
  - A RANDOM FOREST = many trees, each slightly different, and they
    VOTE. The majority answer is usually right. "Many heads > one."

We predict: will a student PASS (1) or FAIL (0) an exam,
using 2 clues: hours studied and hours slept.

Run with:
  python learn_charts/day5_forest_example.py
=====================================================================
"""
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# -------------------------------------------------------------
# STEP 1 — Data: [hours_studied, hours_slept] -> pass(1)/fail(0)
# We MAKE a bigger, realistic dataset (300 students) with a rule
# plus a little randomness/noise (real life is never perfect).
# Rule: pass if study + 0.5*sleep is high enough. Noise flips a few.
# -------------------------------------------------------------
rng = np.random.default_rng(42)
n = 300
study = rng.uniform(0, 8, n)       # 0 to 8 hours studied
sleep = rng.uniform(3, 9, n)       # 3 to 9 hours slept
score = study + 0.5 * sleep + rng.normal(0, 1.0, n)   # add noise
y = (score > 6).astype(int)        # pass if score above 6
X = np.column_stack([study, sleep])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

print("=" * 58)
print("DAY 5 — ONE TREE vs A FOREST (pass/fail prediction)")
print("=" * 58)

# -------------------------------------------------------------
# STEP 2 — One single decision tree
# -------------------------------------------------------------
tree = DecisionTreeClassifier(random_state=42)
tree.fit(X_train, y_train)
tree_acc = accuracy_score(y_test, tree.predict(X_test))
print(f"1 single tree      -> accuracy = {tree_acc*100:.0f}%")

# -------------------------------------------------------------
# STEP 3 — A forest of 100 trees voting
# -------------------------------------------------------------
forest = RandomForestClassifier(n_estimators=100, random_state=42)
forest.fit(X_train, y_train)
forest_acc = accuracy_score(y_test, forest.predict(X_test))
print(f"100 trees (forest) -> accuracy = {forest_acc*100:.0f}%")
print()

# -------------------------------------------------------------
# STEP 4 — Watch the forest VOTE on one new student
# -------------------------------------------------------------
new_student = [[4, 6]]   # studied 4h, slept 6h -> pass or fail?
print("STEP 4 — A new student: studied 4h, slept 6h. Will they pass?")

# ask each of the 100 trees separately
votes = [t.predict(new_student)[0] for t in forest.estimators_]
pass_votes = sum(votes)
fail_votes = len(votes) - pass_votes
final = forest.predict(new_student)[0]

print(f"   Trees voting PASS: {pass_votes}")
print(f"   Trees voting FAIL: {fail_votes}")
print(f"   FOREST DECISION (majority): {'PASS ✅' if final == 1 else 'FAIL ❌'}")
print()

# -------------------------------------------------------------
# STEP 5 — Feature importance: which clue mattered more?
# -------------------------------------------------------------
names = ["hours_studied", "hours_slept"]
print("STEP 5 — Which clue was more important?")
for n, imp in zip(names, forest.feature_importances_):
    bar = "#" * int(imp * 40)
    print(f"   {n:<14} {imp:.2f}  {bar}")
print()

print("=" * 58)
print("WHAT YOU LEARNED")
print("=" * 58)
print("1. One tree can make mistakes (it is 'sensitive').")
print("2. A forest = many trees VOTE -> more stable, fewer mistakes.")
print("3. feature_importances_ tells you which clue mattered most.")
print("Your day5_random_forest.py does the SAME, predicting HighProfit")
print("from 5 clues, and it found Unit_Price was the most important.")
print("=" * 58)
