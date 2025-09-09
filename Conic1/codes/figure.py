# Updated plot: f(t) in blue with grid lines at integer ticks from -5 to 5
import numpy as np
import matplotlib.pyplot as plt

# given values
a = 2 + np.sqrt(2)
b = np.sqrt(2)

# time axis
t = np.linspace(-5, 5, 2000)

# unit step using numpy.heaviside (heaviside(x, 1) gives 1 at x==0)
u_pos = np.heaviside(t, 1)    # u(t)
u_neg = np.heaviside(-t, 1)   # u(-t)

# combined signal
f = np.exp(-a * t) * u_pos + np.exp(b * t) * u_neg

# plotting only the combined f(t) in blue and set y-limits to [-5, 5]
plt.figure(figsize=(5, 5))
plt.plot(t, f, color='blue', linewidth=1.8, label=r'$f(t)=e^{-at}u(t)+e^{bt}u(-t)$')
plt.axvline(0, linestyle='-.', linewidth=0.8)  # show t=0 boundary
plt.title('Narayanpal logo')
plt.xlabel('t')
plt.ylabel('f(t)')
plt.ylim(-5, 5)

# set ticks at every integer and show grid lines there
ticks = np.arange(-5, 6, 1)
plt.xticks(ticks)
plt.yticks(ticks)
plt.grid(which='major', linestyle='--', linewidth=0.6)
plt.legend()
plt.tight_layout()
plt.show()

