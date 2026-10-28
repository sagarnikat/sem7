"""
PROBLEM STATEMENT : Gradient Descent from scratch (ML)

Find the minimum of the function f(x) = (x + 3)^2 using gradient descent.
Gradient descent is THE core optimizer behind nearly all of machine
learning: linear regression, logistic regression, neural networks all just
apply the same two steps below, repeated millions of times on
higher-dimensional versions of the same idea.

HOW IT WORKS:
1. THE FUNCTION - f(x) = (x+3)^2 is a parabola with its global minimum at
   x = -3, f(-3) = 0 (which is the "answer" we hope to converge to).
2. THE DERIVATIVE - f'(x) = 2(x + 3) is the SLOPE: its sign tells which way
   "downhill" is and its magnitude tells how steep.
3. THE UPDATE RULE - walking downhill in small steps:
        x_new = x - learning_rate * f'(x)
   The MINUS sign is the crucial bit: gradient points uphill, so we step
   against it.
4. THE LOOP - repeat `iterations` times from the starting guess x = 2.
   The steps shrink as the slope fades, so the estimate settles more and
   more closely on the minimum x = -3.

WHY HYPER-VALUES MATTER (lecture discussion points):
- learning_rate too large (e.g. 1.0 here) -> overshoot and oscillate or
  even DIVERGE; too small -> converges, but needs many more iterations.
- We stop after a fixed iteration count here (no tolerance check).
- Real training adds: random batch sampling (SGD), momentum, adaptive
  rates (Adam) - all extensions of this exact update rule.

RESULT: prints converged x (should be ~ -2.999996 after 100 iterations at
learning rate 0.1) and the corresponding minimum value ~ 0.

ONLY standard library is needed - run:  python3 "ml/GradientDescent.py"
(no dataset required for this practical).
"""


def f(x):
    """The objective function f(x) = (x + 3)^2 (the value to minimize)."""
    return (x + 3) ** 2


def derivative(x):
    """Slope of f: is position x uphill (+) or downhill (-)?"""
    return 2 * (x + 3)


def gradient_descent(x_start, learning_rate, iterations, verbose_every=10):
    """The loop that carries x toward the minimum; returns final x."""
    x = x_start
    for i in range(iterations):
        gradient = derivative(x)          # how steep, and which way is up
        x = x - learning_rate * gradient  # step AGAINST the gradient
        if i % verbose_every == 0:
            print(f"iter {i:3d}: x = {x:.6f}, f(x) = {f(x):.6f}")
    return x


def run():
    """All steps above; main() only calls this."""
    # Initial guess and hyper-parameters (same values as the notebook cell).
    x_start = 2
    learning_rate = 0.1
    iterations = 100

    x_min = gradient_descent(x_start, learning_rate, iterations)

    print("\nMinimum point x =", round(x_min, 6))
    print("Minimum value y =", round(f(x_min), 10))


if __name__ == "__main__":
    run()
