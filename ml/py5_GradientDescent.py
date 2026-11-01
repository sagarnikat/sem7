"""
QUESTION 5 (ML):
Implement the Gradient Descent Algorithm to find the local minima of the
function y = (x + 3)^2 starting from the point x = 2.

HOW IT WORKS
    1. f(x) = (x + 3)^2 is a parabola with its minimum at x = -3 (f = 0).
    2. f'(x) = 2(x + 3) is the slope: its sign points uphill.
    3. Update rule: x_new = x - learning_rate * f'(x).
    4. Repeat. Steps shrink as the slope fades, so x settles near -3.

    At learning rate 0.1 and 100 iterations, x ends around -2.999996.
    A rate that is too large overshoots; 1.0 never settles.

STEPS
    1. Define the function and its derivative
    2. Set the starting point and hyper-parameters
    3. Gradient descent function
    4. Run gradient descent
    5. Print the minimum
    6. Effect of the learning rate
    7. Observation
    8. Plots with matplotlib

RUN
    python3 ml/py5_GradientDescent.py

    In Jupyter, open py5_GradientDescent.ipynb or split this file at the
    "# %%" markers. This practical needs no imports and no dataset.
"""

# %% Step 1: Define the function and its derivative
def f(x):
    """Objective function f(x) = (x + 3)^2 (the value to minimize)."""
    return (x + 3) ** 2


def derivative(x):
    """Slope of f at x: which way is uphill, and how steep."""
    return 2 * (x + 3)

# %% Step 2: Set the starting point and hyper-parameters
# The question asks to start from x = 2.
x_start = 2
learning_rate = 0.1
iterations = 100

# %% Step 3: Gradient descent function
def gradient_descent(x_start, learning_rate, iterations, verbose_every=10):
    """Walk x downhill until iterations run out; return (final x, path)."""
    x = x_start
    path = [(x, f(x))]
    for i in range(iterations):
        gradient = derivative(x)
        x = x - learning_rate * gradient
        path.append((x, f(x)))
        if i % verbose_every == 0:
            print(f"iter {i:3d}: x = {x:.6f}, f(x) = {f(x):.6f}")
    return x, path

# %% Step 4: Run gradient descent
x_min, descent_path = gradient_descent(x_start, learning_rate, iterations)

# %% Step 5: Print the minimum
print("\nMinimum point x =", round(x_min, 6))
print("Minimum value y =", round(f(x_min), 10))
print("Expected minimum: x = -3, y = 0")

# %% Step 6: Effect of the learning rate
# A small rate converges slowly, 0.9 converges with oscillation, and 1.0
# keeps bouncing because every step overshoots the minimum.
for rate in [0.01, 0.1, 0.5, 0.9, 1.0]:
    final_x, _ = gradient_descent(2, rate, 100, verbose_every=1000)
    print(f"learning_rate={rate:<5} -> x={final_x:.6f}, f(x)={f(final_x):.6g}")

# %% Step 7: Observation
print("\nObservation")
print("  Gradient descent moves against the slope. Near the minimum the")
print("  slope is small, so the steps become small automatically. A very")
print("  large learning rate makes the updates overshoot and diverge.")

# %% Step 8: Plots with matplotlib
import matplotlib.pyplot as plt

# Plot 1: the parabola with every step of the descent drawn on it.
xs = [point[0] for point in descent_path]
ys = [point[1] for point in descent_path]
curve_x = [(-6 + i * 0.01) for i in range(901)]
curve_y = [f(value) for value in curve_x]

fig, axis = plt.subplots(figsize=(7, 5))
axis.plot(curve_x, curve_y, color="tab:gray", label="f(x) = (x + 3)^2")
axis.plot(xs, ys, "o-", color="tab:red", markersize=4,
          linewidth=1, label="descent steps")
axis.plot(x_start, f(x_start), "go", markersize=8, label="start (x = 2)")
axis.plot(x_min, f(x_min), "b*", markersize=14, label="minimum found")
axis.set_title(f"Gradient descent, learning rate = {learning_rate}")
axis.set_xlabel("x")
axis.set_ylabel("f(x)")
axis.axis([-6, 3, -2, 30])
axis.grid(alpha=0.3)
axis.legend(fontsize=8)
fig.tight_layout()
plt.show()

# Plot 2: convergence speed for different learning rates.
fig, axis = plt.subplots(figsize=(7, 5))
for rate in [0.01, 0.1, 0.5, 0.9, 1.0]:
    _, path = gradient_descent(x_start, rate, iterations, verbose_every=1000)
    axis.plot([value for _, value in path], label=f"lr = {rate}")

axis.set_title("Convergence for different learning rates")
axis.set_xlabel("Iteration")
axis.set_ylabel("f(x)")
axis.set_yscale("log")
axis.grid(alpha=0.3)
axis.legend(fontsize=8)
fig.tight_layout()
plt.show()
