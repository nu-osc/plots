#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle
import itertools as it

def main(args):

#
# RC params
#
    plt.rc('text', usetex=True)
    plt.rcParams['grid.alpha'] = 0.1
    plt.rcParams['grid.linewidth'] = 2
    plt.rcParams.update({'font.size': 15})
    plt.rcParams.update({'legend.fontsize': 18})
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 8
    fig_size[1] = 4
    plt.rcParams["figure.figsize"] = fig_size

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    colors = {'nova' : 'xkcd:green', 't2k' : 'xkcd:green', 'minos' : 'xkcd:green',
              'superkamiokande' : 'xkcd:azure', 'icecube' : 'xkcd:azure',
              'nufit5.0' : 'black', 'foreroetal.' : 'black'}

#
# Load
#
    filename = 'amplitude23_NO.dat'
    #if args.input:
    #    filename = args.input
    dtype1 = np.dtype([('id', 'U20'), ('exp', 'U20'), ('cv', 'f8'), ('left', 'f8'), ('right', 'f8'), ('latex', 'U30')])
    result = np.loadtxt(filename, dtype=dtype1, skiprows=1, usecols=(0, 1, 5, 6, 7, 9))
    print(result)

#
# Figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('$\sin^2 \\theta_{23}$')
    plt.subplots_adjust(left=0.25, right=0.85, top=0.9, bottom=0.15)
    ax.set_xlim(0.3,0.7)
    ax.set_ylim(0.5, 7.5)
    plt.plot([0.5, 0.5], [0.5, 7.5], ls='--', color='grey', alpha=0.5)
    
    exp_name = []
    latex_text = []
    
    #
    # Iterate data
    #
    
    for count, exp in enumerate(result):
        id, name, cv, left, right, latex = exp
        exp_name.append(name)
        latex_text.append(latex)
        plt.errorbar(cv, count+1, xerr=np.array([[left, right]]).T, color=colors[id])
        plt.plot(cv, count+1, 'o', markerfacecolor=colors[id], markeredgecolor=colors[id])

        
    y_axis = np.arange(1, 8, 1)
    plt.yticks(y_axis, exp_name)

    
    double_y = ax.twinx()
    double_y.set_ylim(0.5,7.5)
    double_y.tick_params(axis='y', direction='out', labelleft=False, labelright=True, pad=70)
    double_y.set_yticks(y_axis)
    double_y.set_yticklabels(latex_text, ha='right')
    
    
    #ax.yaxis.grid(True, which='minor')
    ax.tick_params(top=True)
    
    outfilename='plot.png'
    if args.output:
        outfilename = args.output
    plt.savefig(outfilename, dpi=300)
    plt.show()
    

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--input', help='file to load')
    parser.add_argument('--output', help='file to write')

    main(parser.parse_args())

