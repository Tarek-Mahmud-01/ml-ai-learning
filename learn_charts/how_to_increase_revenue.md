# 💰 How Revenue Is Calculated + 30-Day Plan to Increase It

Based on YOUR real data and trained model. Easy words.

---

## PART 1 — How the calculation works

Your model learned this exact formula from the data:

```
Revenue = -5006.27
        + 230.63 × Units_Sold      ← each extra unit sold
        +  22.43 × Unit_Price      ← each $1 higher price
        - 6181.26 × Discount       ← each 0.01 (1%) discount
        -   0.66 × Cost_Price      ← almost no effect on revenue
```

**How to read the coefficients (the numbers in front):**
- **+230.63 on Units_Sold** → sell **1 more unit** = about **+$231** revenue. 🟢 BIGGEST lever.
- **+22.43 on Unit_Price** → raise price by **$1** = about **+$22** revenue. 🟢
- **−6181 on Discount** → give **1% more discount** (0.01) = about **−$62** revenue. 🔴 hurts!
- **−0.66 on Cost_Price** → almost 0 → cost does NOT change revenue (it changes PROFIT instead).

👉 The sign tells direction: **+ = increases revenue, − = decreases it.**
👉 The size tells power: 230 is big, 0.66 is tiny.

### Worked example
An average sale: 26 units, price $256, discount 10% (0.10), cost $151:
```
Revenue = -5006 + 230.63×26 + 22.43×256 - 6181×0.10 - 0.66×151
        = -5006 + 5996 + 5742 - 618 - 100
        ≈ 6014   (close to your real average ~$5,914) ✅
```

---

## PART 2 — What actually drives revenue (from your data)

Correlation with Revenue (−1 to +1):
| Feature | Corr | Meaning |
|---|---|---|
| **Units_Sold** | **+0.67** | 🥇 sell more = most revenue |
| **Unit_Price** | **+0.64** | 🥈 higher price = more revenue |
| Discount | −0.10 | discounts slightly lower revenue |
| Cost_Price | −0.02 | no effect on revenue |

**The 3 real levers you control:**
1. 📈 **Sell more units** (marketing, stock, popular products)
2. 💵 **Raise price** carefully (test small increases)
3. ✂️ **Cut wasteful discounts** (they eat revenue fast)

---

## PART 3 — 🗓️ 30-Day Plan to Increase Revenue

### Week 1 (Days 1–7) — MEASURE
- Find your **top 5 products** by revenue (highest sellers).
- Find products with **high discount but low profit** (wasting money).
- Note your current weekly revenue = your **starting number**.

### Week 2 (Days 8–14) — SELL MORE UNITS (biggest lever)
- Push your **top 5 products** harder (feature them, promote them).
- Make sure best-sellers are **never out of stock**.
- Target: **+10% units** on top products.
  - Example: +3 units/sale × $231 ≈ **+$693 per sale**.

### Week 3 (Days 15–21) — FIX PRICING & DISCOUNTS
- Reduce discounts on items that already sell well (they don't need it).
  - Cutting discount from 15% → 10% ≈ **+$309 revenue** per sale (5% × $61.81).
- Test a **small price increase** (+3–5%) on 2–3 popular products.
  - Watch if units drop. If sales stay → pure revenue gain.

### Week 4 (Days 22–30) — DOUBLE DOWN & MEASURE
- Keep what worked, drop what didn't.
- Focus budget on your **best category** (your data: Electronics earns most).
- Compare new weekly revenue vs your Week 1 starting number.
- Goal: **+15–25% revenue** vs Day 1. 🎯

---

## PART 4 — ⚠️ Important warning
**Revenue ≠ Profit.** Raising price or selling more is good, but always check
**Cost_Price**. A sale with huge revenue can still LOSE money if cost is too high.
(Remember Row 0: $10k revenue but −$300 profit.)

👉 Best strategy: grow **Units_Sold** of **low-cost, high-price** products.
That grows BOTH revenue and profit.

---

## Quick summary
| Action | Effect on revenue | Power |
|---|---|---|
| Sell 1 more unit | +$231 | 🟢🟢🟢 |
| Raise price $1 | +$22 | 🟢🟢 |
| Add 1% discount | −$62 | 🔴🔴 |
| Change cost | ~$0 | ⚪ (affects profit, not revenue) |
