#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle
import itertools as it

#
# RC params
#
plt.rc('text', usetex=True)
plt.rcParams['grid.alpha'] = 0.1
plt.rcParams['grid.linewidth'] = 2
plt.rcParams.update({'font.size': 15})
fig_size = plt.rcParams["figure.figsize"]
fig_size[1] = 10
plt.rcParams["figure.figsize"] = fig_size

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
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.3)
ax = fig.add_subplot(111, projection='polar')
ax.set_ylim(0,0.2)
ax.set_yticks([])
ax.set_title('Normal Ordering', pad=15)

angle_ticks        = list(np.arange(0.0, 2*np.pi, 0.25*np.pi))
angle_tick_labels  = [0, '$\pi/4$', '$\pi/2$', '3$\pi/4$', '$\pi$', '$5\pi/4$', '$3\pi/2$', '$7\pi/4$']
ax.set_xticklabels(angle_tick_labels)

text_place = []
text_itself = []
text_color = []
text_offset = []

#
# Some stuff
#
offsets = [0.1, 0.0, -0.2]
step = 0.2
center = (0.5, 0.5)
arcopts = dict(alpha=0.9, transform=ax.transAxes, lw=10)
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
    ang_dummy = Rectangle((0,0), 1, 1,
                          color=color
                         )
    ax.add_patch(arc)
    styles.append(ang_dummy)
    
    cv_label = str(round(cv/np.pi, 2))
    left_label = str(round((left)/np.pi, 2))
    right_label = str(round((right)/np.pi, 2))
    labels.append(name.decode('utf-8')+": $\delta_{CP} = $"+cv_label+"$^{+"+right_label+"}_{-"+left_label+"}\pi$")

    # Marker
    ax.plot(cv, step*r, 'o', markeredgecolor=color, **markeropts)
    # Line
    ax.plot((0, cv), (0, step), color=color, **lineopts)

    # Text via extra ticks
    textvalue = cv/np.pi
    text_place.append(cv)
    text_itself.append(str(round(cv/np.pi, 2))+"$\pi$")
    text_color.append(color)
    text_offset.append(offsets[count])

#
# Finalize the plot
#
ax.legend(styles, labels, bbox_to_anchor=(0.7, 0.25), bbox_transform=fig.transFigure)

for tick, label, color, offset in zip(text_place, text_itself, text_color, text_offset):
    ax.text(tick+offset, 0.25, label, color=color)

tick = [ax.get_rmax(), ax.get_rmax()*0.98]
for t in np.arange(0, np.pi*2, np.pi/12.0):
    ax.plot([t,t], tick, lw=0.72, color="k")

#
# Save
#
plt.savefig('plot.png', dpi=300)
plt.show()
