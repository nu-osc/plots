#!/usr/bin/env python
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
from math import cos,sin,pi
import pandas as pd
from matplotlib.patches import Arc


dtype1 = np.dtype([('exp', '|S20'), ('cv', 'f8'), ('left', 'f8'), ('right', 'f8'),])
result = np.loadtxt("../samples/deltaCP/v4.0-neutrino2020/deltaCP_NO.dat",dtype=dtype1, skiprows=1, usecols=(1, 5, 6, 7))
#result = pd.read_csv("table.txt", sep=" ", header=None)
#result=pd.read_table("../samples/deltaCP/v4.0-neutrino2020/deltaCP_NO.dat", sep=" ")
print(result)

fig = plt.figure()
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
ax = fig.add_subplot(111, projection='polar')
colors = ['xkcd:green', 'xkcd:azure', 'xkcd:green']
count=0
step = 0.2
rev_arr = result[::-1]
for exp in rev_arr:
    name, cv, left, right = exp
    ax.set_ylim(0,0.4)
    arc = Arc((0.5, 0.5), 0.4+step*count, 0.4+step*count, theta1=(float(cv)-float(left))/pi*180, theta2=(float(cv)+float(right))/pi*180, transform=ax.transAxes, lw=4, color=colors[count])
    ax.add_patch(arc)
    ax.set_yticks([])
    angle_ticks = [0, '$\pi/4$', '$\pi/2$', '3$\pi/4$', '$\pi$', '$5\pi/4$', '$3\pi/2$', '$7\pi/4$', '$2\pi$']
    ax.set_xticklabels(angle_ticks)
    #ax.map(plt.plot, "theta", "r")
    ax.text(float(cv), 0.4*(0.35+step*count), name.decode('utf-8'))
    ax.plot(float(cv), 0.4*(0.4+step*count), 'o', markersize=8, markerfacecolor=colors[count], markeredgecolor='k')
    count = count + 1
plt.show()
