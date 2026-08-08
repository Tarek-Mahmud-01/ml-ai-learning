"""
Tutor — pure domain. Plain-English answers about how the model works.
No LLM, no framework: a small keyword-matched knowledge base for learning.
"""
from __future__ import annotations

TOPICS: dict[str, str] = {
    "training": (
        "TRAINING means showing the model many example days so it learns the "
        "'normal' pattern. We turn each worked day into 3 numbers (features): "
        "presence_hours, reported pay, and pay-per-hour. The model studies these "
        "and builds a sense of what normal looks like. Then any new day far from "
        "normal gets flagged. Type 'train' to run it and I'll show the numbers."
    ),
    "feature": (
        "A FEATURE is one number that describes a day. We use three: "
        "presence_hours (how long they were in), reported pay (what they got), "
        "and pay-per-hour (pay divided by hours). The model only sees numbers, "
        "so turning a day into good features is the most important step."
    ),
    "unsupervised": (
        "UNSUPERVISED training (IsolationForest) learns from the data WITHOUT "
        "you telling it right/wrong. It just finds days that look unusual "
        "(outliers). Good when you have no labels. This is what 'train' uses."
    ),
    "supervised": (
        "SUPERVISED training (RandomForest) learns from YOUR labels. You mark "
        "days correct or wrong (e.g. 'E100 2024-06-11 is wrong'), then say "
        "'retrain from my labels' and it learns your definition of wrong. You "
        "become the teacher. Needs enough labelled examples to be reliable."
    ),
    "isolation forest": (
        "ISOLATION FOREST isolates each point with random splits. Unusual points "
        "get isolated in very few splits, so they score as anomalies. It's fast, "
        "needs no labels, and is great for catching odd days like a 20-hour shift."
    ),
    "random forest": (
        "RANDOM FOREST is many decision trees that vote. For us it learns from "
        "your labels to predict wrong vs correct. Many trees voting is more "
        "stable than one tree, so it generalises better."
    ),
    "overfit": (
        "OVERFITTING is when a model memorises the training data instead of "
        "learning the pattern — it scores great on old data but fails on new "
        "data. Fixes: more data, simpler models, and testing on unseen days."
    ),
    "anomaly": (
        "ANOMALY DETECTION means spotting data points that don't fit the normal "
        "pattern. Here, an anomaly is a payslip/day that looks unusual — it may "
        "be a mistake or fraud the fixed rules didn't catch."
    ),
}

_HELP = (
    "I can manage employees, attendance, payroll, and the model. Try:\n"
    "• add employee Rakib rate 22 start 09:00\n"
    "• set E101 base rate to 30\n"
    "• add attendance E101 2024-06-15 present 09:00 18:00 pay 160\n"
    "• set E101 2024-06-12 pay to 190\n"
    "• check E101 june\n"
    "• train  /  E100 2024-06-11 is wrong  /  retrain from my labels\n"
    "• delete attendance E101 2024-06-12  (then repeat with 'confirm')\n"
    "• ask me: 'how does training work?'"
)


def answer(message: str) -> str:
    low = message.lower()
    # most specific first
    for key in ("isolation forest", "random forest", "unsupervised", "supervised",
                "overfit", "feature", "anomaly", "training"):
        if key in low:
            return TOPICS[key]
    if "train" in low or "learn" in low or "model" in low:
        return TOPICS["training"]
    return help_text()


def help_text() -> str:
    return _HELP
