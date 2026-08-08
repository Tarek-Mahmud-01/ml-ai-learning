# 📊 Your 6 Charts — Explained the Easy Way

These are the pictures in your `reports/` folder. Each one helps you SEE your
sales data instead of reading numbers. Here is what each shows and how to read it.

---

## 1) correlation_heatmap.png — "What moves together?"
A grid of numbers from **−1 to +1**.
- 🔴 red / near **+1** = go UP together
- 🔵 blue / near **−1** = one UP, other DOWN
- ⚪ near **0** = no relation

**Your key findings:**
| Pair | Number | Meaning |
|---|---|---|
| Profit ↔ Revenue | +0.77 | more revenue → more profit ✅ |
| Profit ↔ Unit_Price | +0.69 | higher price → more profit 💰 |
| Profit ↔ Cost_Price | **−0.48** | 🔵 higher cost → LESS profit ⚠️ |
| Discount ↔ Profit | −0.08 | discount barely matters |

👉 Lesson: **Cost_Price is the enemy of profit.**

---

## 2) revenue_by_category.png — "Which product type earns most?"
A bar chart. Taller bar = more revenue.
- 🥇 Electronics ≈ 1.52M (highest)
- 🥈 Furniture
- 🥉 Food
- Apparel (lowest)

The thin black line on each bar = the "give or take" range (uncertainty).
👉 Lesson: **Electronics brings the most revenue.**

---

## 3) rf_feature_importance.png — "Which clues did the AI use most?"
When the Random Forest predicted profit, this shows what it cared about:
- Unit_Price = **0.56** (most important) 🥇
- Cost_Price = 0.26
- Units_Sold = 0.10
- Hour = 0.03, Discount = 0.03 (almost ignored)

👉 Lesson: **Price and Cost decide profit. Hour and Discount don't help much.**

---

## 4) histograms.png — "How are values spread out?"
7 small charts. Each bar = how many rows fall in that range. Shape tells a story:
- **Units_Sold, Unit_Price, Cost_Price, Discount** → flat/even (random spread).
- **Revenue** → "leaning left": MANY small sales, FEW big sales.
- **Profit** → a hill (bell shape) centered near 0. Some sales lose money
  (left of 0), some win (right of 0). Most are near the middle.
- **Hour** → tall spikes at certain hours = busy sale times.

👉 Lesson: A histogram shows where most of your data sits.

---

## 5) scatter_plot.png — "Relationship between two things"
Dots on a graph (this was a tiny demo dataset: feature1, feature2, target).
- Each dot is one data point.
- Scatter plots show if two columns rise together or not.
👉 In real use: plot Unit_Price (x) vs Profit (y) to SEE the +0.69 relation as dots.

---

## 6) decision_tree.png — "How the AI makes a decision" ⭐
This is the AI's "flowchart" for guessing **High Profit** or **Low Profit**.
Read it top to bottom. Each box asks a YES/NO question:

- **Top box:** `Unit_Price <= 276.38?`
  - **True (left)** → cheaper items → then it checks `Cost_Price <= 115.28?`
  - **False (right)** → expensive items → then checks `Cost_Price <= 281.26?`
- Keep following the arrows until you reach a bottom box = the final guess.

**Words in each box:**
- `samples` = how many sales reached this box.
- `value = [Low, High]` = how many were Low vs High profit.
- `class` = the box's decision.
- `gini` = how "mixed" the box is (0.0 = perfectly pure/certain).

👉 Example path: expensive item (Unit_Price > 276) + normal cost (Cost_Price <= 281)
   + sold more than 1 unit → box with value [13, 306] → **High Profit** ✅
👉 Lesson: The tree learned that **expensive items with reasonable cost = profit.**

---

## 🖼️ How to OPEN these pictures
Open the `reports/` folder in the file explorer and **double-click** any `.png`.
It opens like a normal photo. No code needed.
