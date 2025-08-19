import numpy as np
import matplotlib.pyplot as plt


def gradient(a,b, theta):
    return np.array([-np.exp(b*theta[0]), -np.exp(-a*theta[1])])

def cost(a,b,theta):
    return ((1-np.exp(b*theta[0]))/b) - ((1-np.exp(-a*theta[1]))/a) 

epochs = 10000000
L = 0.0001
a = 2+ np.sqrt(2)
b= a - 2

theta = np.array([-2,3])

for epoch in range(epochs):
    theta = theta - cost(a,b,theta)*gradient(a,b,theta)*L
    costFunc = cost(a,b,theta)
    if(np.abs(costFunc**2) <= 1e-20): 
        print(f"Cost Has Become Zero, theta has converged, Cost = {costFunc}, epoch = {epoch}")
        break
print(theta)

x = np.linspace(theta[0], theta[1], 1000)
f = np.where(x>0, np.exp(-a*x), np.exp(b*x))

plt.figure(figsize=(10, 6))
plt.plot(x, f, label=f'f(x) with (p={theta[0]}, q={theta[1]})')
plt.title("NarayanPal Logo")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.savefig('../figs/window.png')
plt.legend()
plt.show()