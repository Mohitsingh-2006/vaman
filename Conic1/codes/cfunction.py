import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters (change if you want)
a =2 + np.sqrt(2)
b= a - 2

# Grid for theta0 (negative) and theta1 (positive)
theta0_vals = np.linspace(-9.0, 0.0, 500)   # theta0 in [-2, 0]
theta1_vals = np.linspace(0.0, 12.0, 500)    # theta1 in [0, 4]

T0, T1 = np.meshgrid(theta0_vals, theta1_vals, indexing='xy')

# compute s(theta) and C(theta)
s = (1.0 - np.exp(b * T0)) / b - (1.0 - np.exp(-a * T1)) / a
C = s**2

# Plot
fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(T0, T1, C, rstride=1, cstride=1, linewidth=0, antialiased=True)

ax.set_xlabel(r'$\theta_0$ (negative)')
ax.set_ylabel(r'$\theta_1$ (positive)')
ax.set_zlabel(r'$C(\theta)$')
ax.set_title(r'3D surface of $C(\theta)=\left(\frac{1-e^{b\theta_0}}{b}-\frac{1-e^{-a\theta_1}}{a}\right)^2,a = 3.41 ,b= 1.41$')

# adjust view angle for a clearer visualization
ax.view_init(elev=30, azim=-60)

plt.tight_layout()
plt.show()
fig.savefig('../figs/C_theta_function.png', dpi=200)

