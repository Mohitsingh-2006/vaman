import numpy as np
import matplotlib.pyplot as plt

# -------------------- Numerically-safe helpers --------------------
def safe_exp(x):
    # Clip before exp to avoid overflow; double precision safe limit ~709
    return np.exp(np.clip(x, -700, 700))

def cost(a, b, theta):
    p, q = float(theta[0]), float(theta[1])
    return ((1 - safe_exp(b * p)) / b) - ((1 - safe_exp(-a * q)) / a)

def grad_cost(a, b, theta):
    # ∇C = [dC/dp, dC/dq] = [-exp(b p), -exp(-a q)]
    p, q = float(theta[0]), float(theta[1])
    return np.array([-safe_exp(b * p), -safe_exp(-a * q)])

# -------------------- Fast solver (Gauss-Newton-like) --------------------
def solve_theta(a, b, theta0, max_iter=2000, tol=1e-16):
    theta = theta0.astype(float).copy()
    for i in range(max_iter):
        C = cost(a, b, theta)
        J = grad_cost(a, b, theta)
        denom = J.dot(J)
        if denom == 0 or np.isnan(denom):
            break
        # exact scalar residual update: Δθ = - (C / ||J||^2) * J
        delta = - (C / denom) * J
        theta += delta
        if abs(C) < tol:
            break
    return theta, C, i + 1

# -------------------- Parameters & solve θ --------------------
a = 2.0 + np.sqrt(2.0)
b = a - 2.0
theta0 = np.array([-2.0, 3.0])
theta, final_cost, iters = solve_theta(a, b, theta0)
print(f"Solved theta = {theta}, final cost = {final_cost:.3e}, iterations = {iters}")

# -------------------- Analytic plotting domain from tail-decay ----
eps = 1e-8  # smaller -> wider domain
Xpos = -np.log(eps) / a   # for x > 0 where exp(-a x) = eps
Xneg = -np.log(eps) / b   # for x < 0 where exp(b x) = eps
margin = 1.05
x_min = -Xneg * margin
x_max =  Xpos * margin

# -------------------- Adaptive sampling (dense near peak) -----------
center_half = max(0.8, 2.0 / min(a, b))  # central region half-width
left_n   = 600    # points for left tail (coarse)
center_n = 2200   # dense center (fine)
right_n  = 600    # right tail

x_left   = np.linspace(x_min, -center_half, left_n, endpoint=False)
x_center = np.linspace(-center_half, center_half, center_n, endpoint=False)
x_right  = np.linspace(center_half, x_max, right_n)
x = np.concatenate([x_left, x_center, x_right])

# -------------------- Vectorized evaluation -------------------------
# Original: f(x) = exp(-a x) for x>0 ; exp(b x) for x<=0
f_orig = np.where(x > 0, safe_exp(-a * x), safe_exp(b * x))

# Reflection f(-x): for x>0 -> exp(-b x), for x<=0 -> exp(a x)
f_ref = np.where(x > 0, safe_exp(-b * x), safe_exp(a * x))

# -------------------- Plot -------------------------
plt.figure(figsize=(12, 5))
plt.plot(x, f_orig, linewidth=1.6, label=f'Original f(x), p={theta[0]:.5f}, q={theta[1]:.5f}')
plt.plot(x, f_ref, linestyle='--', linewidth=1.6, label='Reflection f(-x)')
plt.axvline(0.0, linewidth=0.8)

plt.title("Optimized plot: original curve and its reflection")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend(loc='upper right')

y_max = max(f_orig.max(), f_ref.max())
plt.ylim([-0.02 * y_max, y_max * 1.05])
plt.xlim([x_min, x_max])

plt.show()
plt.savefig('../figs/figure_new.png')
