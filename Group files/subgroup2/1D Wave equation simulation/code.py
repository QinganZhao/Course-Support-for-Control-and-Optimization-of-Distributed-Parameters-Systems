import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from matplotlib import rc
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

## parameter
a = 1  ## a coefficient of stiffness
L = 2  ## The string is constrained at x=0 and x=L.
T = 4  ## maxium time for this simulation.
dx = 0.01  ## time step
dt = 0.01  ## distance step
N = int(L / dx);
M = int(T / dt);
r = (a * dt / dx) ** 2  ## a parameter

## initial shape of the string
def initial(x):
    tmp = math.sin(math.pi * x)
    return tmp

## initial speed of the string
def diff(x):
    tmp = 0 * x
    return tmp

## Define an array and a blank matrix for later use.
x = [0]
h = np.zeros((M + 1, N + 1))

## t=0
for i in range(N):
    x.append(x[i] + dx)  ## x axis
    h[0, i + 1] = initial(x[i + 1])  ## displacement of the string

## t=dt
for i in range(N - 1):
    h[1, i + 1] = h[0, i + 1] + r * (h[0, i] + h[0, i + 2] - 2 * h[0, i + 1]) / 2 + dx * diff(x[i + 1])
    ## displacement of the string

## t=n*dt n>1
for j in range(1, M):
    for i in range(N - 1):
        h[j + 1, i + 1] = (h[j, i + 2] + h[j, i] - 2 * h[j, i + 1]) * r - h[j - 1, i + 1] + 2 * h[j, i + 1]
        ## displacement of the string

t = [0]
for j in range(M):
    t.append(t[j] + dt)  ## t axis

## Plot the 3D figure.
fig = plt.figure()
ax = Axes3D(fig)
X, T= np.meshgrid(x,t)
ax.plot_surface(X, T, h, cmap='rainbow')
plt.title(u'Vibrating String',fontsize=14)
ax.set_xlabel('X')
ax.set_ylabel('T')
ax.set_zlabel('h')
plt.show()

## Plot the shape of the string when t=0, 0.5, 1, 1.5 & 2
for i in range(5):
    plt.scatter(x,h[i*50,],label="t="+str(i*0.5))
    plt.title(u'Shape of the String',fontsize=14)
    plt.xlabel(u'x',fontsize=14)
    plt.ylabel(u'h',fontsize=14)
    plt.legend(loc='upper left')
    plt.show()