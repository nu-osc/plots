#!/usr/bin/env python
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
from math import cos,sin

f = open("table.txt", "r")
lines=f.readlines()
result=[]
for x in lines:
    arr=[x.split(' ')[0], x.split(' ')[1], x.split(' ')[2], x.split(' ')[3].replace('\n', '')]
    result.append(arr)
f.close()
print(result)

fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
count=0
step = 0.1
for exp in result:
    for curve in [[[(float(exp[1])-float(exp[2]))*180 , (float(exp[1])+float(exp[3]))*180], [0.1+count*step, 0.1+count*step]]]:
        curve[0] = np.deg2rad(curve[0])
        x = np.linspace( curve[0][0], curve[0][1], 500)
        y = interp1d( curve[0], curve[1])(x)
        ax.plot(x, y, linewidth=7.0)
        ax.text(np.deg2rad(float(exp[1])*180), (0.1+count*step), exp[0])
    count = count + 1
print(count)
plt.show()
