# 🏎️ Day 6: Model Tuning (Optimization)

### Q1: What are "Hyperparameters"?
**A:** They are the "Settings" of the model that you choose *before* training. Examples: How many trees? How deep are the branches? 

### Q2: What is `GridSearchCV`?
**A:** It is a search tool. 
*   **Grid:** The list of settings you want to try.
*   **Search:** Trying every combination.
*   **CV (Cross-Validation):** The "Triple Check" process to make sure the score is real.

### Q3: Why is Tuning important?
**A:** It's like focusing a camera. Day 1-5 gave us a blurry image. Tuning adjusts the lens so the image (the prediction) becomes sharp and clear.

### Q4: What did we find?
**A:** Our model performs best when it is not too complex (`max_depth: 5`). This proves that simpler models are often better at predicting "unseen" data!

---

### 🧠 Tutor Challenge:
**Scenario:** You are tuning a model. 
- Option A gives 99% accuracy but uses `max_depth: 100`. 
- Option B gives 94% accuracy but uses `max_depth: 5`.
**Question:** Which one would you choose to use for a real business?
**Answer:** **Option B!** Option A is likely "memorizing" (Overfitting) and will fail when it sees new data tomorrow. Option B is more "stable."
