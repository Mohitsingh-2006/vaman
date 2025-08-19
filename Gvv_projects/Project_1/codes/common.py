import numpy as np

rgb = lambda x,y,z: (x/255, y/255, z/255)

# Returns the curve of a function f from x = k1 to k2
def func_gen(f, k1, k2):
    x = np.linspace(k1,k2,101).reshape(-1,1) # Odd amount to ensure there is a sample point at x=0
    y = np.vectorize(f)(x)

    return np.hstack((x,y))

# Returns function g given parameters a and b
def func_param(a,b):
    return lambda x: np.e**(b*x) if x<0 else np.e**(-a*x)

# Returns inverse function of both parts of g given parameters a and b
def func_inv_param(a,b):
    return lambda x: np.log(x)/(b), lambda x: np.log(x)/(-a)