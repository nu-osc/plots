#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle
import itertools as it

titles = dict(
        NO = 'Normal Ordering',
        IO = 'Inverted Ordering'
        )
colors = dict(
        nova='xkcd:warm purple',
        superkamiokande='xkcd:azure',
        t2k='xkcd:green',
        foreroetal20='xkcd:steel grey',
        nufit19='xkcd:midnight'
        )

def main(args):
    #
    # RC params
    #
    plt.rc('text', usetex=True)
    plt.rcParams['grid.alpha'] = 0.1
    plt.rcParams['grid.linewidth'] = 2
    plt.rcParams.update({'font.size': 15})
    plt.rcParams.update({'legend.fontsize': 18})

    prop_cycle = plt.rcParams['axes.prop_cycle']

    #
    # Load
    #
    dtype1 = np.dtype([('id', 'U20'), ('exp', 'U20'), ('cv', 'f8'), ('left', 'f8'), ('right', 'f8'),])
    result = np.loadtxt(args.input, dtype=dtype1, skiprows=1, usecols=(0, 1, 5, 6, 7))
    rev_arr = result[::-1]
    print(result)

    #
    # Figure
    #
    fig = plt.figure(figsize=(6,9))
    plt.subplots_adjust(left=-0.05, right=1.05, top=0.90, bottom=0.35)
    ax = fig.add_subplot(111, projection='polar')
    ymax=0.1
    ax.set_ylim(0,ymax)
    ax.set_yticks([])
    ax.set_title(titles[args.ordering], pad=15)

    angle_ticks        = list(np.arange(0.0, 2*np.pi, 0.25*np.pi))
    angle_tick_labels  = [0, '$\pi/4$', '$\pi/2$', '3$\pi/4$', '$\pi$', '$5\pi/4$', '$3\pi/2$', '$7\pi/4$']
    ax.set_xticklabels(angle_tick_labels)
    ax.tick_params(axis='x', pad=7)

    text_place = []
    text_itself = []
    text_color = []
    text_offset = []
    text_roffset = []

    #
    # Some stuff
    #
    offsets = [0.0, 0.0, -0.06, -0.05, -0.05]
    roffsets = [0.0, 0.0, 0.0, 0.0, 0.0]
    if args.ordering=='IO':
        offsets = [-0.05, -0.05, 0.05, 0.05, 0.05]
        roffsets = [0.0, 0.008, 0.0, 0.01, 0.005]
    step = 0.12
    center = (0.5, 0.5)
    arcopts = dict(alpha=0.9, transform=ax.transAxes, lw=10)
    markeropts = dict(markersize=8, markerfacecolor='white')
    lineopts = dict(alpha=0.5, lw=1)
    legwidth = '12cm'
    legtitle_width = '13.7cm'

    #
    # Iterate data
    #
    styles, labels = [], []
    for count, exp in enumerate(rev_arr):
        # Numbers
        id, name, cv, left, right = exp
        if cv<0.0:
            cv = 2+cv
        theta1=np.degrees((cv-left)*np.pi)
        theta2=np.degrees((cv+right)*np.pi)
        cv_rad=cv*np.pi
        r = 0.4+step*count
        color = colors.get(id, 'black')

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

        deltacp = '\delta_{\scriptscriptstyle\mathrm{CP}}'
        name = name.replace('_', ' ')
        label = f'\\parbox{{{legwidth}}}{{{name}\hfill{{}}${cv:.2f}^{{+{right:.2f}}}_{{-{left:.2f}}}$}}'
        labels.append(label)

        # Marker
        ax.plot(cv_rad, r*ymax, 'o', markeredgecolor=color, **markeropts)
        # Line
        ax.plot((0, cv_rad), (0, step), color=color, **lineopts)

        if count<len(offsets):
            # Text via extra ticks
            text_place.append(cv_rad)
            text_itself.append(f'{cv:.2f}$\pi$')
            text_color.append(color)
            text_offset.append(offsets[count])
            text_roffset.append(roffsets[count])

    #
    # Finalize the plot
    #
    legend_title = f'\\parbox{{{legtitle_width}}}{{Experiment\hfill{{}}${deltacp}, \\pi$}}'
    fig.legend(reversed(styles), reversed(labels), loc='lower center', title=legend_title)

    for tick, label, color, offset, roffset in zip(text_place, text_itself, text_color, text_offset, text_roffset):
        ax.text(tick+offset, ymax*1.1+roffset, label, color=color, ha='center', va='center')

    tick = [ax.get_rmax(), ax.get_rmax()*0.98]
    for t in np.arange(0, np.pi*2, np.pi/12.0):
        ax.plot([t,t], tick, lw=0.72, color="k")

    #
    # Save
    #
    for out in  args.output:
        plt.savefig(out, dpi=300)
        print('Save output file:', out)

    if args.show:
        plt.show()


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('input', help='file to load')
    parser.add_argument('--ordering',  choices=('NO', 'IO'), help='ordering')
    parser.add_argument('-o', '--output', nargs='+', default=(), help='file to write')
    parser.add_argument('-s', '--show', action='store_true', help='file to write')

    main(parser.parse_args())

