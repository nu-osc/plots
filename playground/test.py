#!/usr/bin/env python
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
from math import cos,sin
import pandas as pd
from matplotlib.patches import Arc


dtype1 = np.dtype([('exp', '|S10'), ('cv', 'f8'), ('left', 'f8'), ('right', 'f8'),])
result = np.loadtxt("../samples/deltaCP/v4.0-neutrino2020/deltaCP_NO.dat", delimiter=' ',dtype=dtype1, skiprows=1, usecols=(1, 5, 6, 7))
#result = pd.read_csv("table.txt", sep=" ", header=None)
#result=pd.read_table("../samples/deltaCP/v4.0-neutrino2020/deltaCP_NO.dat", sep=" ")
print(result)

fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
count=0
step = 0.2
for exp in result:
    ax.set_ylim(0,0.4)
    arc = Arc((0.5, 0.5), 0.4+step*count, 0.4+step*count, theta1=(float(exp[1])-float(exp[2]))*180, theta2=(float(exp[1])+float(exp[3]))*180, transform=ax.transAxes, lw=8)
    ax.add_patch(arc)
    ax.set_yticks([])
    ax.text(np.deg2rad(float(exp[1])*180), 0.4*(0.7+step*count), exp[0])
    count = count + 1
plt.show()
