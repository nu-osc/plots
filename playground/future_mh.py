#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle, Polygon
import itertools as it

def main(args):

#
# RC params
#
    plt.rc('text', usetex=True)
    plt.rcParams['grid.alpha'] = 0.1
    plt.rcParams['grid.linewidth'] = 2
    plt.rcParams.update({'font.size': 20})
    plt.rcParams.update({'legend.fontsize': 18})
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 14
    fig_size[1] = 7
    plt.rcParams["figure.figsize"] = fig_size

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    colors = {'nova' : 'xkcd:hot magenta', 't2ksk' : 'xkcd:dark sky blue', 'icupgr' : 'xkcd:slate grey', 'juno':'xkcd:fire engine red', 'pingu' : 'xkcd:dark grey blue', 'orca' : 'xkcd:teal', 't2hk' : 'xkcd:dark sky blue', 'dune':'xkcd:violet'}
    
    fullnames = {'nova' : 'NOvA', 't2ksk' : 'T2K+SuperK', 'icupgr' : 'IceCube Upgrade', 'juno' : 'JUNO', 'pingu' : 'PINGU', 'orca': 'KM3NeT/ORCA', 't2hk' : 'T2HK', 'dune' : 'DUNE'}
    
    position = {'nova' : (2022, 3.25), 't2ksk' : (2020.25, 1.5), 'icupgr' : (2025, 1.5), 'juno' : (2023.5, 2.5), 'pingu' : (2031, 3.5), 'orca': (2027, 4), 't2hk' : (2034.5, 4), 'dune' : (2029, 8)}

#
# Load
#
    filenames = ['nova', 't2ksk', 'icupgr', 'juno', 'pingu', 'orca', 't2hk', 'dune']
    dtype1 = np.dtype([('year', 'f8'), ('min', 'f8'), ('max', 'f8')])
    exps = []
    for exp in filenames:
        result = np.loadtxt('sens_data/'+exp+'.txt', dtype=dtype1, usecols=(0, 1, 2))
        #print(result)
        low = []
        high = []
        for line in result:
            year, min, max = line
            low.append((year, min))
            high.append((year, max))
        this_exp = {'id': exp, 'low_values' : low, 'high_values' : high}
        exps.append(this_exp)
    
    #print(exps)

#
# Figure
    fig, ax = plt.subplots()
    plt.title('Future MH sensitivity', pad=15)
    ax.set_xlabel('Year')
    ax.set_ylabel('Sigma')
    ax.set_xlim(2020, 2040)
    ax.set_ylim(0, 10.0)

    for count, exp in enumerate(exps):
        revert_max = exp['high_values'][::-1]
        size = len(revert_max) - 1
        color=colors[exp['id']]
        name=fullnames[exp['id']]
        text_place_x=position[exp['id']][0]
        text_place_y=position[exp['id']][1]
        poly = Polygon(exp['low_values'] + revert_max, facecolor=color, edgecolor=color, alpha=0.3)
        ax.add_patch(poly)
        ax.text(text_place_x, text_place_y, name, color=color)
        
    plt.minorticks_on()
    plt.grid()
    x_axis = np.arange(2020, 2042, 2)
    #print(x_axis)
    ax.set_xticks(x_axis)
    ax.set_xticklabels(['2020', '2022', '2024', '2026', '2028', '2030', '2032', '2034', '2036', '2038', '2040'])
    
    outfilename='plot.png'
    if args.output:
        outfilename = args.output
    plt.savefig(outfilename, dpi=300)
    plt.show()
    

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--output', help='file to write')

    main(parser.parse_args())

