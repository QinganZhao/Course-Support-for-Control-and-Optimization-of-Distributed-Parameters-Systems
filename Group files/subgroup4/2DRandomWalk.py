# -*- coding: utf-8 -*-
"""
Created on Wed Oct 04 20:28:59 2017

@author: Rob Ruigrok
"""

# This file will model/simulate the random motion

import numpy as np
import matplotlib.pyplot as plt
from random import *
import math
#from matplotlib import mpl,pyplot
import pylab

###############################################################################
########################## START INPUT ########################################
###############################################################################

GridSizeSquare = 20                                         #define the size of your grid. There will be walls around the box
Pos_init = np.ceil(np.array([0.4,0.4])*GridSizeSquare)      #define starting position as ratio or grid size
T = 0.1*np.power(GridSizeSquare, 2)                         #this is the total amount of time steps, scale with square of grid size
n_particles = 10000           # amount of particles. 10000+ gives a nice distribution
subplot_row = 2             # define the amount of subplots that you like
subplot_column = 2
motion_prob = np.array([0.2,0.2,0.2,0.2,0.2])   #defines the probabilities for drift: ([up,right,down,left,no motion]) 

###############################################################################
########################## END INPUT ##########################################
###############################################################################

x_grid = GridSizeSquare     #only look at square grids, but this could be changed
y_grid = GridSizeSquare
n_subplot = subplot_row*subplot_column;
Plot_interval = np.floor((T-1)/(n_subplot-1));          #This determines when you take snapshots of the proces, every "Plot_interval" timesteps

# now define the probabilities of the random walk
# notation of motion ([up,right,down,left,no motion])
motion_prob = motion_prob/np.sum(motion_prob)               # normalize in case probabilities do not add up to 1...
motion_xy = np.array([[0,1],[1,0],[0,-1],[-1,0],[0,0],])    # define the change in coordinates of every motion
motion_prob_percentile = np.cumsum(motion_prob)             # used later to draw from with randomizer

# make an empty data grid from where you are going to count the amount occurances and hits against the wall
Data = np.zeros((x_grid+2,y_grid+2)) #be careful with x-y being row-column here, "+2" for wall data
Data_resized = np.zeros((Data.shape[0]+1,Data.shape[1]+1))  #for plotting purposes, I need to add an extra row an column
Data_TimeVarying = np.zeros((n_subplot,Data_resized.shape[0],Data_resized.shape[1]))    #for subplots
# prepare some arrays for later plotting (not in loop for speed)
xx, yy = pylab.meshgrid(
    pylab.linspace(-1,x_grid+1,x_grid+3),
    pylab.linspace(-1,y_grid+1,y_grid+3))

for i in range(1, n_particles+1):
    # Initialize simulation
    t = 0
    HitWall = False
    Pos = Pos_init
    Subplot = 1
    
    # start simulation
    while t < T and not HitWall:
                
         # Now continue with the motion simulation
        MotionRandom = random()
        IndexMotion = np.argmax(motion_prob_percentile>MotionRandom)
        Pos = Pos + motion_xy[IndexMotion,:] #this works
        
        # Now check for hitting the wall
        if Pos[0] == 0 or Pos[1] == 0 or Pos[0] == x_grid+1 or Pos[1] == y_grid+1:
            if Subplot <= n_subplot:             
                Data_TimeVarying[Subplot-1,Pos[0],Pos[1]] = Data_TimeVarying[Subplot-1,Pos[0],Pos[1]]+1
            HitWall = True

        # Now record the position for time dependent plotting purposes
        if t % Plot_interval == 0 and Subplot <= n_subplot and not(HitWall):   #so create a subplot every Plot_interval time steps
            Data_TimeVarying[Subplot-1,Pos[0],Pos[1]] = Data_TimeVarying[Subplot-1,Pos[0],Pos[1]]+1
            Subplot = Subplot+1        
        
        t = t+1
    
    
    #This was basically the whole simulation, now save the results
    Data[Pos[0],Pos[1]] = Data[Pos[0],Pos[1]] + 1
    # I need to give resize Data with an extra row and column, since pcolor doesn't plot the full range of the matrix...
    Data_resized[:-1,:-1] = Data       


# Now I need to do some post-processing of the intermediate measurements.
# I need to add the particles that hit the wall in earlier time steps to the 
# later plots, so the total amount of particles is always n  
Data_TimeVarying_Corrected = np.cumsum(Data_TimeVarying,axis=0)
Data_TimeVarying_Corrected[:,1:x_grid+1,1:y_grid+1] = Data_TimeVarying[:,1:x_grid+1,1:y_grid+1]


# This loop creates several subplots of the time instaces that you specified at the input
plt.figure()
for j in range(1, n_subplot+1):
    #Now visualize the outcomes
    pylab.subplot(subplot_row, subplot_column, j)
    pylab.pcolor(xx,yy,np.transpose(Data_TimeVarying_Corrected[j-1,:,:]))
    TitleString = 'Distribution at t = ' + str((j-1)*Plot_interval+1)
    pylab.title(TitleString)
    # and a color bar to show the correspondence between function value and color
    pylab.colorbar()
    pylab.hold(True)
    pylab.plot([0, x_grid],[0, 0], 'r',[0, x_grid],[y_grid, y_grid], 'r',[0, 0],[0, y_grid], 'r',[x_grid, x_grid],[0, y_grid], 'r')
    pylab.plot(Pos_init[0]-0.5,Pos_init[1]-0.5,'ro')

pylab.show()

# This plot shows the final distribution, including distribution along the walls
plt.figure()
pylab.pcolor(xx,yy,np.transpose(Data_resized))
pylab.title('Final distribution at t = %d, including hitting walls' %T)
# and a color bar to show the correspondence between function value and color
pylab.colorbar()
pylab.hold(True)
pylab.plot([0, x_grid],[0, 0], 'r',[0, x_grid],[y_grid, y_grid], 'r',[0, 0],[0, y_grid], 'r',[x_grid, x_grid],[0, y_grid], 'r')
pylab.plot(Pos_init[0]-0.5,Pos_init[1]-0.5,'ro')
pylab.show

    
    
    
    
    