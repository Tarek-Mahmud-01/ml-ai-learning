r"""
=====================================================================
DAY 1 EXAMPLE — dropna() + Feature Engineering (ice cream sales)
=====================================================================
Run with:
  python day1_wrangling_example.py

You will SEE:
  1. Raw messy data (with missing values = NaN).
  2. dropna() removing the broken rows.
  3. Feature engineering: creating NEW helpful columns
     (Is_Weekend, Is_Holiday) from raw data.
=====================================================================
"""
import pandas as pd
import numpy as np

pd.set_option("display.width", 100)

# -------------------------------------------------------------
# STEP 1 — Raw data (like it comes from the real world = messy)
# -------------------------------------------------------------
# Notice: some Temperature and Sales values are missing (NaN).
raw = pd.DataFrame({
    "Date":        ["2024-07-01", "2024-07-02", "2024-07-03", "2024-07-04",
                    "2024-07-05", "2024-07-06", "2024-07-07"],
    "Temperature": [30,   32,   np.nan, 35,   33,   31,   np.nan],
    "Is_Holiday":  [0,    0,    0,      1,    0,    0,    1     ],
    "Sales":       [200,  240,  260,    np.nan, 250, 300,  310  ],
})

print("=" * 60)
print("STEP 1 — RAW DATA (messy, has NaN = missing values)")
print("=" * 60)
print(raw)
print(f"\nMissing values per column:\n{raw.isna().sum()}")
print()


# -------------------------------------------------------------
# STEP 2 — dropna(): remove rows that have missing values
# -------------------------------------------------------------
# WHY: A model does math. It cannot multiply by "NaN". So we drop
#      the broken rows (or fill them). Here we drop them.
clean = raw.dropna()

print("=" * 60)
print("STEP 2 — AFTER dropna()  (broken rows removed)")
print("=" * 60)
print(clean)
print(f"\nRows before: {len(raw)}   ->   Rows after: {len(clean)}")
print("(Rows with a missing Temperature or Sales are gone.)")
print()


# -------------------------------------------------------------
# STEP 3 — FEATURE ENGINEERING: build NEW useful columns
# -------------------------------------------------------------
# The AI cannot guess "is this a weekend?" by itself.
# We TEACH it by creating the column from the Date.
clean = clean.copy()
clean["Date"] = pd.to_datetime(clean["Date"])

# New feature 1: day name (Monday, Tuesday, ...)
clean["Day_Name"] = clean["Date"].dt.day_name()

# New feature 2: Is_Weekend (1 if Saturday/Sunday, else 0)
clean["Is_Weekend"] = clean["Date"].dt.dayofweek.isin([5, 6]).astype(int)

# New feature 3 (the ice cream idea!): "Hot AND holiday" = big sales day
# If it's hot (>=32) AND a holiday, people REALLY buy ice cream.
clean["Hot_Holiday"] = ((clean["Temperature"] >= 32) &
                        (clean["Is_Holiday"] == 1)).astype(int)

print("=" * 60)
print("STEP 3 — AFTER FEATURE ENGINEERING (new helpful columns)")
print("=" * 60)
print(clean[["Date", "Day_Name", "Temperature", "Is_Holiday",
             "Is_Weekend", "Hot_Holiday", "Sales"]])
print()

print("=" * 60)
print("WHAT YOU JUST LEARNED")
print("=" * 60)
print("1. dropna() removed rows the model could not use (NaN).")
print("2. Feature engineering ADDED clues the model can learn from:")
print("     - Is_Weekend : behavior changes on weekends")
print("     - Hot_Holiday: hot + holiday = biggest ice cream day!")
print("   Same raw data, but now MUCH easier for the AI to predict.")
print("=" * 60)
