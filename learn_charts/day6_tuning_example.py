r"""
=====================================================================
DAY 6 EXAMPLE — Tuning (finding the best model settings)
=====================================================================
Big idea:
  "Hyperparameters" = SETTINGS you pick BEFORE training.
  Example: how deep can a tree go? (max_depth)

  Too deep  = the model MEMORIZES the training data (overfitting).
              Great on old data, BAD on new data.
  Too shallow = too simple, misses the pattern.
  Just right = best on NEW (unseen) data.

  GridSearchCV = try many settings automatically and pick the best.

Run with:
  python learn_charts/day6_tuning_example.py
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
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score

# -------------------------------------------------------------
# Data: 300 students. pass/fail from study + sleep (with noise).
# -------------------------------------------------------------
rng = np.random.default_rng(42)
n = 300
study = rng.uniform(0, 8, n)
sleep = rng.uniform(3, 9, n)
score = study + 0.5 * sleep + rng.normal(0, 1.0, n)
y = (score > 6).astype(int)
X = np.column_stack([study, sleep])
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

print("=" * 60)
print("DAY 6 — TUNING: what happens at different max_depth?")
print("=" * 60)
print(f"{'max_depth':>10}{'TRAIN acc':>12}{'TEST acc':>12}   note")
print("-" * 60)

for depth in [1, 2, 3, 5, 10, 20, None]:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=42)
    tree.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, tree.predict(X_train))
    test_acc = accuracy_score(y_test, tree.predict(X_test))

    note = ""
    if depth in (1,):
        note = "too simple"
    elif depth in (None, 20):
        note = "MEMORIZING! (overfit)"
    elif depth in (3, 5):
        note = "good balance ✅"
    label = "None" if depth is None else str(depth)
    print(f"{label:>10}{train_acc*100:>11.0f}%{test_acc*100:>11.0f}%   {note}")

print("-" * 60)
print("See it? Deep trees get ~100% on TRAIN but LOWER on TEST.")
print("That gap = overfitting (memorizing, not learning).")
print("The best TEST score is at a medium depth. That's the sweet spot.")
print()

# -------------------------------------------------------------
# GridSearchCV — let the computer find the best settings
# -------------------------------------------------------------
print("=" * 60)
print("GRID SEARCH — try many settings, pick the best automatically")
print("=" * 60)
param_grid = {
    "n_estimators": [50, 100],
    "max_depth": [3, 5, 10, None],
}
print("Settings to try:")
print(f"   n_estimators (trees): {param_grid['n_estimators']}")
print(f"   max_depth (depth):    {param_grid['max_depth']}")
print("Searching (with 3x cross-validation 'triple check')...")

grid = GridSearchCV(RandomForestClassifier(random_state=42),
                    param_grid, cv=3, scoring="accuracy", n_jobs=-1)
grid.fit(X_train, y_train)

print()
print(f"🏆 WINNING SETTINGS: {grid.best_params_}")
print(f"   Cross-validation score: {grid.best_score_*100:.1f}%")
final_test = accuracy_score(y_test, grid.best_estimator_.predict(X_test))
print(f"   Accuracy on NEW test data: {final_test*100:.1f}%")
print()

print("=" * 60)
print("WHAT YOU LEARNED")
print("=" * 60)
print("1. Hyperparameters = settings chosen BEFORE training.")
print("2. Too deep = overfit (memorize). Simpler is often better.")
print("3. GridSearchCV tries all combos + 'triple checks' to find best.")
print("Your day6_tuning.py does the SAME on your sales data, and found")
print("max_depth=5 works best -> simpler model wins on new data!")
print("=" * 60)
