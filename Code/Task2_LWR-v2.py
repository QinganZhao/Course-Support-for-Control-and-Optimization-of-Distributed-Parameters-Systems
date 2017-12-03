#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 07:38:39 2017

@author: Lorna
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
Data structure creation and initialisation
"""
# Global parameters
T_final=3600 # time duration
N_t=500 # number of time steps: the time step value dt is computed later
X_final=5000 # road length
N_x=100 # number of space steps: the space step value dx is computed later
rho0=0.2 #jam density in Greenshield flux function(number of vehicles/m)
v0=15 #free flow velocity(m/s)

# structures for visualization and computation of time/space steps
T,dt=np.linspace(0,T_final,num=N_t,endpoint=True,retstep=True)
X,dx=np.linspace(0,X_final,num=N_x,endpoint=True,retstep=True)
#set the range and sample number of time(T)–[0,3600]seconds in every 7.2 seconds
#set the range and sample number of distance(X)–[0,5000]meters in every 50 meters
print("dx = ",dx,"  dt = ",dt)

# structure for simulation: density as a function of space and time
rho = np.zeros((N_x,N_t))
# initialization of the density at time 0 with a continuous function
for x in range(int(N_x/2)):
    rho[x][0] = rho0/3+rho0*x/N_x/3 # from rho0/3 to rho0/2
for x in range(int(N_x/2),N_x):
    # rho[x][0] = rho0/3+rho0*x/N_x/3 # from rho0/2 to rho0*2/3
    rho[x][0] = rho0/3+rho0*x/N_x/3
print("t = 0")
plt.plot(X,rho[:,0])
plt.show()#plot the density in the range of x at t=0

    
"""
Start the main simulation loop
Note that the naive Euler integration scheme is ALWAYS numerically unstable
Learn about Von Neumann stability analysis
And use the simple (stable) Lax scheme
But stability needs the Courant Friedrichs Levy condition to be verified
Trick: if unstable, decrease value of dt
"""
for t in range(N_t-1): # at timestep t, compute rho at t+1
    for x in range(1,N_x-1):
        #calculate density at t+1 on i based on density at t on i and i+1
        dr = v0*dt/dx*(2*rho[x][t]/rho0-1)*(rho[x+1][t]-rho[x-1][t])/2
        r = (rho[x-1][t]+rho[x+1][t])/2 + dr #this is Lax Scheme
        rho[x][t+1] = r
    # for x==N_x, we take the derivative backward
    x = 0
    dr = v0*dt/dx*(2*rho[x][t]/rho0-1)*(rho[x+1][t]-rho[x][t])
    r = (rho[x][t]+rho[x+1][t])/2 + dr
    rho[x][t+1] = r
    x = N_x-1
    dr = v0*dt/dx*(2*rho[x][t]/rho0-1)*(rho[x][t]-rho[x-1][t])
    r = (rho[x][t]+rho[x-1][t])/2 + dr
    rho[x][t+1] = r
    if((t+1)%int(N_t/5)==int(N_t/5)-1):
        print("t = ",t)
        plt.plot(X,rho[:,t])
        plt.show()#plot the density in the range of x at t=98,198,298,398,498
    
        
X,T = np.meshgrid(X,T)
Z = rho.reshape(X.shape)

fig=plt.figure()
ax=Axes3D(fig)
ax.plot_surface(X,T,Z, rstride=1, cstride=1, cmap='rainbow')
plt.show()#plot the 3d figure
