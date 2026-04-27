# 📘 Day 1: Environment & Data Wrangling

### Q1: What is "Data Wrangling"?
**A:** It is the process of cleaning, transforming, and mapping raw data into a format that is useful for downstream tasks like Machine Learning. Think of it as "prepping the ingredients" before cooking.

### Q2: Why did we use `dropna()`?
**A:** Machine Learning models are based on mathematical equations. You cannot perform math on a "Missing Value" (NaN). If we don't remove or fill these gaps, the computer will crash or give incorrect "hallucinated" results.

### Q3: What is "Feature Engineering"?
**A:** It is the "creative" part of Data Science. We take raw data (like a Date) and create new, more useful columns (like "Day of Week" or "Is Weekend"). These give the AI better "clues" to solve the problem.

### Q4: Why save a `cleaned_data.csv`?
**A:** It creates a "checkpoint." You don't want to run your cleaning script every single time you train a model. By saving the clean version, your Day 2, Day 3, and Day 4 scripts will always start with perfect data.

---

### 🧠 Think Like a Data Scientist:
**Scenario:** You are predicting ice cream sales.
**Question:** If you have a column for `Temperature`, why might you also want a column for `Is_Holiday`?
**Answer:** Because even if it's hot, you might sell less if schools are open. If it's a holiday, people go out more! Feature engineering helps capture these human behaviors.
