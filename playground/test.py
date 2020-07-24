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
plt.rcParams.update({'font.size': 15})

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
ax.set_title('Normal Ordering', pad=15)

angle_ticks        = list(np.arange(0.0, 2*np.pi, 0.25*np.pi))
angle_tick_labels  = [0, '$\pi/4$', '$\pi/2$', '3$\pi/4$', '$\pi$', '$5\pi/4$', '$3\pi/2$', '$7\pi/4$']
angle_tick_colors  = [None]*len(angle_ticks)
angle_tick_offsets = [None]*len(angle_ticks)

#
# Some stuff
#
offsets = [0.0, -10, +10]
step = 0.2
center = (0.5, 0.5)
arcopts = dict(linewidth=18, alpha=0.9, transform=ax.transAxes, lw=10)
markeropts = dict(markersize=8, markerfacecolor='white')
lineopts = dict(alpha=0.5, lw=1)

#
# Iterate data
#
styles, labels = [], []
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
    styles.append(arc)
    labels.append(name.decode('utf-8'))

    # Marker
    ax.plot(cv, step*r, 'o', markeredgecolor=color, **markeropts)
    # Line
    ax.plot((0, cv), (0, step), color=color, **lineopts)

    # Text via extra ticks
    textvalue = cv/np.pi
    angle_ticks.append(cv)
    angle_tick_labels.append(f'{textvalue:.2f}$\pi$')
    angle_tick_colors.append(color)
    angle_tick_offsets.append(offsets[count])

#
# Finalize the plot
#
ax.legend(styles, labels, bbox_to_anchor=(1.0, 1.0), bbox_transform=fig.transFigure)

ax.set_xticks(angle_ticks)
ax.set_xticklabels(angle_tick_labels)

for tick, label, color, offset in zip(ax.get_xticks(), ax.get_xticklabels(), angle_tick_colors, angle_tick_offsets):
    if color:
        label.set_c(color)

    if offset:
        label.set_position((offset, 0.0))

tick = [ax.get_rmax(), ax.get_rmax()*0.98]
for t in np.arange(0, np.pi*2, np.pi*0.125):
    ax.plot([t,t], tick, lw=0.72, color="k")

#
# Save
#
plt.savefig('plot.png', dpi=300)
plt.show()
