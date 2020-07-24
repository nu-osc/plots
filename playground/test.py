#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc
import itertools as it

#
# RC params
#
plt.rc('text', usetex=True)
plt.rcParams['grid.alpha'] = 0.1
plt.rcParams['grid.linewidth'] = 2
plt.rcParams.update({'font.size': 14})

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
colors = ['xkcd:warm purple', 'xkcd:azure', 'xkcd:green']

#
# Load
#
dtype1 = np.dtype([('exp', '|S20'), ('cv', 'f8'), ('left', 'f8'), ('right', 'f8'),])
result = np.loadtxt("../samples/deltaCP/v4.0-neutrino2020/deltaCP_NO.dat",dtype=dtype1, skiprows=1, usecols=(1, 5, 6, 7))
rev_arr = result[::-1]
print(result)

#
# Figure
fig = plt.figure()
plt.subplots_adjust(left=-0.12, right=0.85, top=0.85, bottom=0.1)
ax = fig.add_subplot(111, projection='polar')
ax.set_ylim(0,0.2)
ax.set_yticks([])
angle_ticks = [0, '$\pi/4$', '$\pi/2$', '3$\pi/4$', '$\pi$', '$5\pi/4$', '$3\pi/2$', '$7\pi/4$', '$2\pi$']
ax.set_xticklabels(angle_ticks)
ax.set_title('Normal Ordering', pad=15)

#
# Some stuff
#
offset = [1.03, 1.0, 0.96]
step = 0.2
center = (0.5, 0.5)
arcopts = dict(linewidth=18, alpha=0.9, transform=ax.transAxes, lw=15)
markeropts = dict(markersize=8, markerfacecolor='white')
lineopts = dict(alpha=0.5)

#
# Iterate data
#
for count, (exp, color) in enumerate(zip(rev_arr, it.cycle(colors))):
    # Numbers
    name, cv, left, right = exp
    theta1=np.degrees(cv-left)
    theta2=np.degrees(cv+right)
    r = 0.4+step*count

    # Arc
    arc = Arc(center, r, r,
              theta1=theta1, theta2=theta2,
              color=color,
              **arcopts
              )
    ax.add_patch(arc)

    # Marker
    ax.plot(cv, step*r, 'o', markeredgecolor=color, **markeropts)
    # Line
    ax.plot((0, cv), (0, step), color=color, label=name.decode('utf-8'), **lineopts)

    # Text
    ax.text(cv*offset[count], 0.25, str(round(cv/np.pi, 2))+"$\pi$", color=color)

#
# Finalize the plot
#
ax.legend(bbox_to_anchor=(1.0, 1.0), bbox_transform=fig.transFigure)

tick = [ax.get_rmax(),ax.get_rmax()*0.98]
for t  in np.deg2rad(np.arange(0,360,15)):
    ax.plot([t,t], tick, lw=0.72, color="k")

#
# Save
#
plt.savefig('plot.png', dpi=300)
plt.show()
