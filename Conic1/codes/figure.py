import os
import numpy as np
import matplotlib.pyplot as plt

# -------------------- Helpers --------------------
def safe_exp(x):
    return np.exp(np.clip(x, -700, 700))

def cost(a, b, theta):
    p, q = float(theta[0]), float(theta[1])
    return ((1 - safe_exp(b * p)) / b) - ((1 - safe_exp(-a * q)) / a)

def grad_cost(a, b, theta):
    p, q = float(theta[0]), float(theta[1])
    return np.array([-safe_exp(b * p), -safe_exp(-a * q)])

def solve_theta(a, b, theta0, max_iter=2000, tol=1e-16):
    theta = theta0.astype(float).copy()
    for i in range(max_iter):
        C = cost(a, b, theta)
        J = grad_cost(a, b, theta)
        denom = J.dot(J)
        if denom == 0 or np.isnan(denom):
            break
        delta = - (C / denom) * J
        theta += delta
        if abs(C) < tol:
            break
    return theta, C, i + 1

# -------------------- Parameters & solve --------------------
a = 2.0 + np.sqrt(2.0)
b = a - 2.0
theta0 = np.array([-2.0, 3.0])
theta, final_cost, iters = solve_theta(a, b, theta0)
print(f"Solved theta = {theta}, final cost = {final_cost:.3e}, iterations = {iters}")

# -------------------- Domain & adaptive sampling --------------------
eps = 1e-8
Xpos = -np.log(eps) / a
Xneg = -np.log(eps) / b
margin = 1.05
x_min = -Xneg * margin
x_max =  Xpos * margin

center_half = max(0.8, 2.0 / min(a, b))
left_n, center_n, right_n = 600, 2200, 600
x_left   = np.linspace(x_min, -center_half, left_n, endpoint=False)
x_center = np.linspace(-center_half, center_half, center_n, endpoint=False)
x_right  = np.linspace(center_half, x_max, right_n)
x = np.concatenate([x_left, x_center, x_right])

# -------------------- Evaluate curves --------------------
f_orig = np.where(x > 0, safe_exp(-a * x), safe_exp(b * x))
f_ref  = np.where(x > 0, safe_exp(-b * x), safe_exp(a * x))

# -------------------- Plot and save (save BEFORE show) --------------------
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(x, f_orig, linewidth=1.6,
        label=f'Original f(x), p={theta[0]:.5f}, q={theta[1]:.5f}')
ax.plot(x, f_ref, linestyle='--', linewidth=1.6, label='Reflection f(-x)')
ax.axvline(0.0, linewidth=0.8, color='k')

ax.set_title("Optimized plot: original curve and its reflection")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True)
ax.legend(loc='upper right')

y_max = max(f_orig.max(), f_ref.max())
ax.set_ylim([-0.02 * y_max, y_max * 1.05])
ax.set_xlim([x_min, x_max])
fig.tight_layout()

# Save directory and filenames (adjust as needed)
out_dir = "../figs"
os.makedirs(out_dir, exist_ok=True)   # safe: creates if missing
png_path = os.path.join(out_dir, "figure_new.png")
svg_path = os.path.join(out_dir, "figure_new.svg")

# Save high-quality images BEFORE showing (important)
fig.savefig(png_path, dpi=300, bbox_inches='tight')
fig.savefig(svg_path, bbox_inches='tight')  # vector format

print(f"Saved: {png_path}")
print(f"Saved: {svg_path}")

# Now show (safe — file already written)
plt.show()

# Optionally close figure to free memory
plt.close(fig)

