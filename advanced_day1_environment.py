r"""
=====================================================================
ADVANCED DAY 1 — Environment Check + Linear Algebra Intuition
=====================================================================
Goal for today:
  1. Confirm your environment works (all libraries import).
  2. THEORY: A neural network layer is just matrix multiplication.
  3. PROJECT: Multiply two matrices BY HAND, then verify with NumPy.

Run this file with:   venv\Scripts\python.exe advanced_day1_environment.py
=====================================================================
"""

# ---------------------------------------------------------------
# PART 0 — Environment check (does everything import?)
# ---------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib
import sklearn
import torch

print("=" * 55)
print("ENVIRONMENT CHECK")
print("=" * 55)
print(f"NumPy        : {np.__version__}")
print(f"pandas       : {pd.__version__}")
print(f"matplotlib   : {matplotlib.__version__}")
print(f"scikit-learn : {sklearn.__version__}")
print(f"PyTorch      : {torch.__version__}")
print(f"GPU (CUDA)?  : {torch.cuda.is_available()}  (CPU is totally fine for learning)")
print()


# ---------------------------------------------------------------
# PART 1 — THEORY: the dot product
# ---------------------------------------------------------------
# A single neuron computes:  output = (inputs . weights) + bias
# The "." is a DOT PRODUCT: multiply pairs, then add them up.
#
#   inputs  = [x1, x2, x3]
#   weights = [w1, w2, w3]
#   dot     = x1*w1 + x2*w2 + x3*w3
# ---------------------------------------------------------------
print("=" * 55)
print("PART 1 — Dot product = one neuron's core math")
print("=" * 55)

inputs = np.array([1.0, 2.0, 3.0])
weights = np.array([0.2, 0.8, -0.5])
bias = 2.0

# By hand:
manual = inputs[0]*weights[0] + inputs[1]*weights[1] + inputs[2]*weights[2] + bias
# With NumPy:
numpy_way = np.dot(inputs, weights) + bias

print(f"Neuron output (by hand) : {manual}")
print(f"Neuron output (NumPy)   : {numpy_way}")
print(f"Match? {np.isclose(manual, numpy_way)}")
print()


# ---------------------------------------------------------------
# PART 2 — PROJECT: matrix multiplication by hand vs NumPy
# ---------------------------------------------------------------
# A LAYER of neurons = a MATRIX multiply.
# Rule: result[i][j] = sum over k of  A[i][k] * B[k][j]
# ---------------------------------------------------------------
print("=" * 55)
print("PART 2 — PROJECT: matrix multiply (a neural layer)")
print("=" * 55)

A = np.array([[1, 2],
              [3, 4]])          # shape (2, 2)
B = np.array([[5, 6],
              [7, 8]])          # shape (2, 2)


def matmul_by_hand(A, B):
    """Multiply two matrices using only loops — no np.dot."""
    rows_A, cols_A = A.shape
    rows_B, cols_B = B.shape
    assert cols_A == rows_B, "Inner dimensions must match!"

    result = np.zeros((rows_A, cols_B))
    for i in range(rows_A):            # each row of A
        for j in range(cols_B):        # each column of B
            total = 0
            for k in range(cols_A):    # walk the shared dimension
                total += A[i][k] * B[k][j]
            result[i][j] = total
    return result


manual_result = matmul_by_hand(A, B)
numpy_result = A @ B               # '@' is the matrix-multiply operator

print("A =\n", A)
print("B =\n", B)
print("\nBy hand (loops):\n", manual_result)
print("\nNumPy (A @ B):\n", numpy_result)
print("\nMatch?", np.allclose(manual_result, numpy_result))
print()


# ---------------------------------------------------------------
# PART 3 — Same idea in PyTorch (tomorrow's tool)
# ---------------------------------------------------------------
print("=" * 55)
print("PART 3 — The exact same math in PyTorch tensors")
print("=" * 55)
tA = torch.tensor(A, dtype=torch.float32)
tB = torch.tensor(B, dtype=torch.float32)
print("torch result (tA @ tB):\n", tA @ tB)
print()

print("=" * 55)
print("DAY 1 COMPLETE. Key idea:")
print("  A neural network layer = matrix multiplication + bias.")
print("  You just built it by hand. Tomorrow: calculus & gradients.")
print("=" * 55)

# ---------------------------------------------------------------
# YOUR EXERCISE (try before Day 2):
#   1. Change A to shape (2,3) and B to shape (3,2). Does it still work?
#   2. What happens if inner dimensions DON'T match? (try it, read the error)
#   3. Add a third matrix C and compute A @ B @ C.
# ---------------------------------------------------------------
