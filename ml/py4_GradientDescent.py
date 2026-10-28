"""
QUESTION 4 (ML):
Implement the Gradient Descent Algorithm to find the local minima of a
function - for example, find the local minima of y = (x + 3)^2 starting
from the point x = 2.

HOW IT WORKS:
1. FUNCTION - f(x) = (x+3)^2 is a parabola with its minimum at x = -3
   (f = 0); that is the "answer" the algorithm must find by itself.
2. DERIVATIVE - f'(x) = 2(x+3) is the slope: its sign points uphill,
   its magnitude says how steep.
3. UPDATE RULE - step AGAINST the gradient:
       x_new = x - learning_rate * f'(x)
4. LOOP - repeat 100 times from x = 2. Steps shrink as the slope fades,
   so x settles ever closer to -3 (after 100 iterations at lr = 0.1 it
   lands around -2.999996).

WHY HYPER-PARAMETERS MATTER (discussion points):
- learning_rate too big (e.g. 1.0) -> overshoot, oscillate or diverge;
  too small -> converges but needs far more iterations.
- This demo stops at a fixed iteration count; real training adds
  tolerance-based stopping, mini-batches (SGD), momentum, Adam.

NOTE: this practical needs no imports and no dataset file - it is pure
math, so there is no STEP 2 file-creation stage.

COMMANDS (run from the repository root):
    install dependencies : none
    run the program      : python3 ml/py4_GradientDescent.py
"""

# ============================================================
# STEP 1 : IMPORTS
# ============================================================
# none - this program needs only the standard built-ins


# ============================================================
# STEP 2 : THE FUNCTION AND ITS DERIVATIVE (no dataset needed)
# ============================================================
def f(x):
    """Objective function f(x) = (x + 3)^2 (the value to minimize)."""
    return (x + 3) ** 2


def derivative(x):
    """Slope of f at x: which way is uphill, and how steep."""
    return 2 * (x + 3)


# ============================================================
# STEP 3 : THE GRADIENT DESCENT LOOP (uses the functions above)
# ============================================================
def gradient_descent(x_start, learning_rate, iterations, verbose_every=10):
    """Walk x downhill until iterations run out; return the final x."""
    x = x_start
    for i in range(iterations):
        gradient = derivative(x)            # direction/steepness of uphill
        x = x - learning_rate * gradient    # step against the gradient
        if i % verbose_every == 0:
            print(f"iter {i:3d}: x = {x:.6f}, f(x) = {f(x):.6f}")
    return x


# ============================================================
# STEP 4 : DRIVER - start at x = 2, run 100 steps, print minimum
# ============================================================
def run():
    x_start, learning_rate, iterations = 2, 0.1, 100

    x_min = gradient_descent(x_start, learning_rate, iterations)

    print("\nMinimum point x =", round(x_min, 6))
    print("Minimum value y =", round(f(x_min), 10))


if __name__ == "__main__":
    run()