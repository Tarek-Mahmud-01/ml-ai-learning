r"""
=====================================================================
DAY 1 — PRACTICE WORKSHEET  (you write the code!)
=====================================================================
Topic: Linear Algebra = the math inside a neural network layer.

HOW THIS WORKS:
  - Each TASK has a "# YOUR CODE HERE" line.
  - Replace `None` with your answer.
  - Run the file. It will CHECK each task and tell you PASS or TRY AGAIN.

Run with:
  venv\Scripts\python.exe day1_practice.py

Do them in order. If stuck > 15 min, scroll to the HINTS at the bottom.
=====================================================================
"""
import numpy as np

print("=" * 55)
print("DAY 1 PRACTICE — write your answers, then run me")
print("=" * 55)

results = []
def check(name, condition):
    status = "PASS ✅" if condition else "TRY AGAIN ❌"
    results.append(condition)
    print(f"  {name:<38} {status}")


# =============================================================
# TASK 0 — EXAMPLE (already solved — copy this pattern!)
# =============================================================
# GOAL: make a vector with the numbers 10, 20, 30.
#
# INPUT  (what we start with): the numbers 10, 20, 30
# ANSWER (what YOU write):     np.array([10, 20, 30])
# OUTPUT (what comes out):     [10 20 30]
#
# See below -> the `None` was replaced with a real answer.
# This one already PASSES so you can see how it looks. Copy the idea.
# -------------------------------------------------------------
example = np.array([10, 20, 30])   # <-- this is a finished answer

check("Task 0: EXAMPLE (already done)",
      list(example) == [10, 20, 30])
print(f"     input : 10, 20, 30   ->   output: {example}")
print()


# -------------------------------------------------------------
# TASK 1 — Create a vector
# Make a NumPy array with the numbers 2, 4, 6, 8.
#
# EXPLAIN: A "vector" is just a list of numbers in a row.
#   In AI, your data is ALWAYS vectors. One employee, one image,
#   one sentence -> all become a vector of numbers. This is step 1
#   of everything. np.array turns a normal Python list into a fast
#   math object that NumPy can compute with.
# -------------------------------------------------------------
v = np.array([2, 4, 6, 8])  # YOUR CODE HERE  (hint: np.array([...]))

check("Task 1: vector [2,4,6,8]",
      isinstance(v, np.ndarray) and list(v) == [2, 4, 6, 8])


# -------------------------------------------------------------
# TASK 2 — Dot product (this is ONE neuron)
# inputs = [1, 2, 3], weights = [0.5, 0.5, 0.5]
# Compute the dot product (multiply pairs, add them up).
#
# EXPLAIN: The dot product IS a neuron's brain.
#   Multiply each input by its weight, then add them all:
#     (1*0.5) + (2*0.5) + (3*0.5) = 0.5 + 1.0 + 1.5 = 3.0
#   "Weight" = how important each input is. Big weight = matters more.
#   Learning = the AI slowly changing these weights to get better.
# -------------------------------------------------------------
inputs = np.array([1, 2, 3, 4])
weights = np.array([0.5, 0.5, 0.5, 0.5])

dot = np.dot(inputs, weights)  # YOUR CODE HERE  (hint: np.dot(...) )

check("Task 2: dot product = 4.0", dot == 5.0)




# -------------------------------------------------------------
# TASK 3 — Add a bias
# A neuron is:  dot_product + bias.  Bias here = 1.0
# Use your `dot` from Task 2.
#
# EXPLAIN: "Bias" is an extra number added at the end.
#   Full neuron =  (inputs . weights) + bias
#   Think of bias like the starting point / base value. Even if all
#   inputs are 0, the bias lets the neuron still output something.
#   Weights = the slope, bias = the shift up/down. Both get learned.
# -------------------------------------------------------------
bias = 1.0
neuron_output = dot + bias  # YOUR CODE HERE

check("Task 3: neuron output = 6.0", neuron_output == 6.0)


# -------------------------------------------------------------
# TASK 4 — Matrix multiply (this is a full LAYER)
# Multiply matrix M by matrix N using the @ operator.
#
# EXPLAIN: One neuron = one dot product. But a LAYER has MANY
#   neurons working at once. Doing many dot products together =
#   MATRIX MULTIPLICATION. The `@` symbol means "matrix multiply".
#   Note: M here is the "identity matrix" (1s on the diagonal).
#   Multiplying by identity gives back the SAME matrix -- like
#   multiplying a number by 1. That's why M @ N == N.
# -------------------------------------------------------------
M = np.array([[1, 0],
              [0, 1]])          # identity matrix
N = np.array([[7, 8],
              [9, 20]])
product = M @ N  # YOUR CODE HERE  (hint: M @ N)

check("Task 4: M @ N equals N",
      product is not None and np.array_equal(product, N))


# -------------------------------------------------------------
# TASK 5 — Shapes matter
# Give the SHAPE of matrix N as a tuple, e.g. (2, 2).
#
# EXPLAIN: "Shape" = how many rows and columns. (2, 2) means
#   2 rows and 2 columns. Shapes are the #1 cause of bugs in deep
#   learning! To multiply A @ B, the inner numbers MUST match:
#   (2,3) @ (3,4) works -> gives (2,4). (2,3) @ (2,4) FAILS.
#   Checking .shape all the time will save you hours later.
# -------------------------------------------------------------
n_shape = N.shape  # YOUR CODE HERE  (hint: N.shape)

check("Task 5: shape of N is (2,2)", n_shape == (2, 2))


# -------------------------------------------------------------
# TASK 6 — Apply ReLU (the most common activation)
# ReLU(x) = x if x > 0, else 0.
# Apply it to this array. (hint: np.maximum(0, x))
#
# EXPLAIN: ReLU is an "activation function". After a neuron does
#   its math, ReLU throws away negatives (turns them to 0) and keeps
#   positives. Why? It adds "non-linearity" -- this is what lets a
#   network learn complex patterns (curves, not just straight lines).
#   Without activations, 100 layers would still act like just 1.
#   ReLU is the most used because it is simple and fast.
# -------------------------------------------------------------
x = np.array([-3, -1, 0, 2, 5])
relu = np.maximum(0, x)  # YOUR CODE HERE

check("Task 6: ReLU = [0,0,0,2,5]",
      relu is not None and list(relu) == [0, 0, 0, 2, 5])
x = np.array([-3, -1, 0, 2, 5])

relu2 =np.maximum(1, x)
check("Task 6: ReLU = [1,1,1,2,5]",
      relu2 is not None and list(relu2) == [1, 1, 1, 2, 5])


# -------------------------------------------------------------
# SCORE
# -------------------------------------------------------------
print("-" * 55)
passed = sum(1 for r in results if r)
total = len(results)
print(f"  SCORE: {passed}/{total}")
if passed == total:
    print("  🎉 PERFECT! You understand a neural layer. Ready for Day 2.")
else:
    print("  Keep going — fix the ❌ tasks and run again. See HINTS below.")
print("=" * 55)


# =====================================================================
# HINTS (only look if stuck!)
# =====================================================================
# Task 1:  v = np.array([2, 4, 6, 8])
# Task 2:  dot = np.dot(inputs, weights)      # or: (inputs * weights).sum()
# Task 3:  neuron_output = dot + bias
# Task 4:  product = M @ N
# Task 5:  n_shape = N.shape
# Task 6:  relu = np.maximum(0, x)
# =====================================================================
