# 📉 Day 3: Logistic Regression (Classification)

### Q1: What is "Classification"?
**A:** It is the process of predicting which "Category" something belongs to. Unlike Linear Regression which gives us a specific number, Classification tells us "Group A" or "Group B."

### Q2: Why did we use `StandardScaler`?
**A:** Imagine comparing a mouse (weight in grams) and an elephant (weight in tons). The AI thinks the elephant is 1,000,000 times more important because the number is bigger. Scaling makes them comparable (e.g., "Small for its kind" vs "Big for its kind").

### Q3: What is the "Classification Report"?
**A:** It's the AI's Report Card.
*   **Precision:** Accuracy of positive predictions.
*   **Recall:** Ability to find all positive instances.
*   **F1-Score:** The balance between the two.
*   **Accuracy:** Overall "How many did I get right?" (We got 95%!).

### Q4: Why save the `scaler` along with the `model`?
**A:** Because the model "learned" on scaled data. If you try to give it raw numbers later, it will get confused. You must use the same "ruler" (the scaler) to measure new data.

---

### 🧠 Tutor Challenge:
**Scenario:** You built an AI to detect if an email is **Spam**.
**Question:** If the AI marks an important email from your boss as "Spam," is that a problem with **Precision** or **Recall**?
**Answer:** That's a **Precision** problem. Precision is about making sure that when you say "Spam," it really IS spam. 
