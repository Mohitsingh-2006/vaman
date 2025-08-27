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

fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(x, f_orig, linewidth=1.6,
        label=f'f(x), p={theta[0]:.5f}, q={theta[1]:.5f}')
ax.plot(x, f_ref, linewidth=1.6, label='f(-x)')
ax.axvline(0.0, linewidth=0.8, color='k')
ax.axhline(0.0, linewidth=0.8, color='k')

# Title and labels
ax.set_title("Narayanpal logo")
ax.set_xlabel("x")
ax.set_ylabel("y")

# Set limits
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])

# ✅ Major ticks (with labels)
ax.set_xticks([-5, -3, -1, 0, 1, 3, 5])
ax.set_yticks([-5, -3, -1, 0, 1, 3, 5])

# ✅ Minor ticks (for grid only)
ax.set_xticks([-4, -2, 2, 4], minor=True)
ax.set_yticks([-4, -2, 2, 4], minor=True)

# ✅ Enable both major and minor grids
ax.grid(which='major', linestyle='-', linewidth=0.8)
ax.grid(which='minor', linestyle='--', linewidth=0.6, alpha=0.5)

ax.legend(loc='upper right')
fig.tight_layout()

# Save directory and filenames (adjust as needed)
out_dir = "../figs"
os.makedirs(out_dir, exist_ok=True)   # safe: creates if missing
png_path = os.path.join(out_dir, "figure_new.png")

# Save high-quality images BEFORE showing (important)
fig.savefig(png_path, dpi=300, bbox_inches='tight')

print(f"Saved: {png_path}")

# Now show (safe — file already written)
plt.show()

# Optionally close figure to free memory
plt.close(fig)

