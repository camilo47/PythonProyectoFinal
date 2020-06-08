# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 08:44:02 2020

@author: kmisk
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

MONTHS = [ 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
DAYS = []

def loadDays():
    
    tmp_range = range(1,32)
    for x in tmp_range:
        DAYS.append(x)      

loadDays()

result=[]

for i in range(1,13):
    result.append(['0','0','0','0',i,'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'])

result = np.array(result, dtype=np.float)

fig=plt.figure(figsize=(20, 10), dpi=60)
ax1=fig.add_subplot(111, projection='3d')


xlabels = np.array(DAYS)
xpos = np.arange(xlabels.shape[0])
ylabels = np.array(MONTHS) 
ypos = np.arange(ylabels.shape[0])

xposM, yposM = np.meshgrid(xpos, ypos, copy=False)

zpos=result
zpos = zpos.ravel()

dx=0.5
dy=0.5
dz=zpos

ax1.w_xaxis.set_ticks(xpos + dx/2.)
ax1.w_xaxis.set_ticklabels(xlabels)

ax1.w_yaxis.set_ticks(ypos + dy/2.)
ax1.w_yaxis.set_ticklabels(ylabels)

values = np.linspace(0.2, 1., xposM.ravel().shape[0])
colors = cm.rainbow(values)
ax1.bar3d(xposM.ravel(), yposM.ravel(), dz*0, dx, dy, dz, color=colors)
plt.show()