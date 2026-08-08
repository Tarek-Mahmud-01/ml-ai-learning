# 📊 Understanding Your Sales Data (Easy Notes)

This explains your `data/erp_data.csv` file in simple words.

---

## 🧾 What is "Data Overview"?
When you print a table, pandas shows the **first 5 rows** so you can see what your data looks like. It is just a *preview* — like looking at the first page of a book. It does NOT mean only 5 rows exist.

---

## 📋 What each column means

| Column | Simple meaning | Example |
|---|---|---|
| **Date** | When the sale happened (day + hour) | 2024-01-01 00:00:00 |
| **Product_ID** | Which product was sold | P004 |
| **Category** | Type of product | Food |
| **Region** | Where it was sold | East |
| **Units_Sold** | How many pieces sold | 43 |
| **Unit_Price** | Price of ONE piece (before discount) | $283.28 |
| **Discount** | Price cut, as a fraction (0.14 = 14% off) | 0.14 |
| **Cost_Price** | What it COST the company to make ONE piece | $250.62 |
| **Revenue** | Total money that came IN | $10,475.69 |
| **Profit** | Money left AFTER paying costs (can be negative!) | -$300.97 |

---

## 🧮 The Formulas (the important part!)

### 1) Revenue = money coming in
```
Revenue = Units_Sold × Unit_Price × (1 − Discount)
```
**Why `(1 − Discount)`?** If discount is 14% (0.14), the customer pays 86% of the price.
So we multiply by `(1 − 0.14) = 0.86`.

### 2) Profit = money you actually keep
```
Profit = Revenue − (Cost_Price × Units_Sold)
```
You subtract the total cost of making all the units. If cost is bigger than revenue → **Profit is negative** (you lost money).

---

## ✅ Worked Example — Row 0 (real numbers from your file)

**Given:**
- Units_Sold = 43
- Unit_Price = 283.28
- Discount = 0.14
- Cost_Price = 250.62

**Step 1 — Revenue:**
```
= 43 × 283.28 × (1 − 0.14)
= 43 × 283.28 × 0.86
= 10,475.69   ✅ matches your data
```

**Step 2 — Profit:**
```
= Revenue − (Cost_Price × Units_Sold)
= 10,475.69 − (250.62 × 43)
= 10,475.69 − 10,776.66
= −300.97    ✅ matches your data
```

👉 **Meaning:** They sold 43 units but the cost to make them was HIGHER than the money earned → the company **LOST $300.97** on this sale. The big discount + high cost ate the profit.

---

## 😀 Another Example — Row 3 (a GOOD sale)

- Units = 24, Price = 78.21, Discount = 0.03, Cost = 22.59

```
Revenue = 24 × 78.21 × 0.97 = 1,820.73
Profit  = 1,820.73 − (22.59 × 24) = 1,820.73 − 542.16 = 1,278.57  ✅
```
👉 **Meaning:** Cheap to make ($22.59) but sold for much more → **profit of $1,278.57**. This is a healthy sale!

---

## 💡 The big lesson
- **High Revenue does NOT mean profit.** Row 0 had huge revenue ($10k) but LOST money, because the cost was too high.
- **Profit is what really matters.** Watch `Cost_Price` and `Discount` — they decide if you win or lose.

---

## 🖼️ What are the PNG files in `reports/`?
Those are **charts (pictures)** your earlier scripts made from this data. They help you SEE patterns instead of reading numbers:

| PNG file | What it shows |
|---|---|
| `histograms.png` | How values are spread (e.g. most common price) |
| `correlation_heatmap.png` | Which columns move together (e.g. does price affect profit?) |
| `scatter_plot.png` | Relationship between two columns (dots on a graph) |
| `revenue_by_category.png` | Which category earns the most |
| `rf_feature_importance.png` | Which columns the AI found most useful |
| `decision_tree.png` | A picture of how the model makes decisions |

👉 To view them: open the `reports/` folder and **double-click** any `.png` — it opens like a normal image.
