
# coding: utf-8



import numpy as np
import scipy as scip
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter




T_final = 100
N_t = 200
X_final = 1
N_x = 100

# Calculate time and x steps based on sampling size and # of samples
T,dt = np.linspace(0,T_final,N_t+1,0,1) 
X,dx = np.linspace(0,X_final,N_x+1,0,1) 

alpha = 9.7e-5          # Thermal diffusivity of Aluminium in m^2/s
Fo = (alpha*dt)/(dx*dx) # Fourier number = diffusive transport rate/storage rate

u_cur = u_old = u_z = np.zeros(N_x+1) # Initialize the N state and the N-1 state
#u_old = np.zeros((N_t,N_x+1))




# Define your initial condition here. This could be some function IC(x),
#  however for simplicity's sake we take a rod with a uniform temperature
#  and in contact with a hot plate at one end

u_old[:] = 25  # Set the whole rod to be a constant temperature
u_old[0] = 200 # Set a high temperature at the boundary wall
#u_old
u_z = u_old




plt.figure(1)

for t in range(0,N_t):
    for i in range(1,N_x):
        # Forward Euler solution to 1D Heat Eq. PDE
        u_cur[i] = Fo*(u_old[i+1] - 2*u_old[i] + u_old[i-1]) + u_old[i]
    u_cur[0] = 200  # Set the left boundary to be our high of 200 
    u_old[:] = u_cur # We move to the next time step, reset N-1 state
    
    u_z = np.vstack((u_z,u_cur)) # Add to the history (used for surface plot)
    if(t%40==0):
        plt.plot(X,u_cur)
plt.show()




# Make data.
X, T = np.meshgrid(X, T)
Z = u_z




# Plot the surface.
fig = plt.figure()
ax = fig.gca(projection='3d')

surf = ax.plot_surface(X, T, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.0f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

