# 📈 Day 2: Linear Regression

### Q1: What is the "Target" vs "Features"?
**A:** 
*   **Target (y):** The goal or the answer we want the AI to find. In our case, it was **Revenue**.
*   **Features (X):** The "clues" or inputs we give the AI to help it find the answer. We used **Units Sold, Unit Price, and Discount**.

### Q2: Why do we use `train_test_split`?
**A:** To prevent **Overfitting** (memorizing). If a student memorizes the answers to a practice test, they will fail the real exam. Splitting the data ensures the AI actually learns the "logic" instead of just memorizing the rows.

### Q3: What does the R2 Score mean?
**A:** It tells us how much of the "variance" (the changes in data) our model explains. 
*   **0.87** means our model is 87% accurate at following the trend of the data.

### Q4: What is `joblib`?
**A:** It is like a "Save Game" button for AI. Training a model can take a long time. `joblib` allows us to save the trained model to a file so we can use it later without retraining.

---

### 🧠 Tutor Challenge:
**Question:** If we added a feature called `Store_Color` (the color of the paint on the walls), do you think the R2 score would go up or down?
**Answer:** It might stay the same or go down! Adding "useless" features confuses the AI. Choosing the **right** features is called "Feature Selection."
