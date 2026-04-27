# 🌳 Day 4: Decision Trees

### Q1: What is a Decision Tree?
**A:** It is a model that predicts values by learning simple decision rules inferred from the data features. Think of it as a Flowchart or a game of "20 Questions."

### Q2: Why do we use `max_depth`?
**A:** `max_depth` controls how "tall" the tree can grow. 
*   If it's too tall, it will memorize every single row (Overfitting).
*   If it's too short, it won't learn enough (Underfitting). 
We used `max_depth=3` to keep it easy to understand.

### Q3: What is a "Node" in the tree?
**A:** A node is where a question is asked (e.g., `Units_Sold <= 15`). Depending on the answer, the data goes Left (True) or Right (False).

### Q4: Why was Day 3 (95%) better than Day 4 (89%)?
**A:** In our specific ERP data, the relationship between features is very "Linear" (straightforward). Logistic Regression is mathematically better at finding straight lines. Decision Trees are better for complex, "staircase" patterns.

---

### 🧠 Tutor Challenge:
**Question:** If you are building an AI to decide if a patient has a disease, and you want to explain **EXACTLY** why the AI made that choice to a doctor, would you use Logistic Regression or a Decision Tree?
**Answer:** A **Decision Tree**! You can show the doctor the "Tree Map," and they can follow the arrows to see the logic. This is called "Explainable AI."
