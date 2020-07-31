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
    colors = {'nova' : 'xkcd:fuchsia', 't2ksk' : 'xkcd:blue green', 'icupgr' : 'xkcd:peacock blue', 'juno':'xkcd:fire engine red', 'pingu' : 'xkcd:dark sky blue', 'orca' : 'xkcd:muddy brown', 't2hk' : 'xkcd:green', 'dune':'xkcd:violet', 'ino' : 'orange', 't2hkk' : 'xkcd:green',}
    
    fullnames = {'nova' : 'NOvA', 't2ksk' : 'T2K+SuperK', 'icupgr' : 'IceCube Upgrade', 'juno' : 'JUNO', 'pingu' : 'PINGU', 'orca': 'KM3NeT/ORCA', 't2hk' : 'T2HK', 'dune' : 'DUNE', 'ino' : 'ICAL @ INO', 't2hkk' : 'T2HKK'}
    
    position = {'nova' : (2022, 3.25), 't2ksk' : (2020.25, 1.5), 'icupgr' : (2025.25, 1.5), 'juno' : (2023.5, 2.5), 'pingu' : (2031, 3.5), 'orca': (2027, 4), 't2hk' : (2034.5, 4), 'dune' : (2029, 8), 'ino' : (2035, 2.5), 't2hkk' : (2033.5, 8)}

#
# Load
#
    filenames = ['nova', 't2ksk', 'icupgr', 'juno', 'pingu', 'orca', 't2hk', 'dune', 'ino', 't2hkk']
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
    plt.title('Future MH sensitivity', pad=20)
    ax.set_xlabel('Year')
    ax.set_ylabel('Sensitivity ($\sigma$)')
    ax.set_xlim(2020, 2040)
    ax.set_ylim(0, 10.0)

    plt.plot([2020.0, 2040.0], [5.0, 5.0], ls='--', color='grey', alpha=0.5)

    for count, exp in enumerate(exps):
        revert_max = exp['high_values'][::-1]
        size = len(revert_max) - 1
        color=colors[exp['id']]
        name=fullnames[exp['id']]
        text_place_x=position[exp['id']][0]
        text_place_y=position[exp['id']][1]
        poly = Polygon(exp['low_values'] + revert_max, facecolor=color, edgecolor=color, alpha=0.3)
        ax.add_patch(poly)
        if exp['id'] == 't2hkk' or exp['id'] == 'pingu' or exp['id'] == 'ino':
            poly.set_hatch('/')
        t = ax.text(text_place_x, text_place_y, name, color=color)
        t.set_bbox(dict(facecolor='white', alpha=0.3, edgecolor='white'))
        
    plt.minorticks_on()
    plt.grid()
    x_axis = np.arange(2020, 2042, 2)
    #print(x_axis)
    ax.set_xticks(x_axis)
    ax.set_xticklabels(['2020', '2022', '2024', '2026', '2028', '2030', '2032', '2034', '2036', '2038', '2040'])
    ax.tick_params(top=True, right=True)
    
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

