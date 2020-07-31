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
    fig_size[1] = 8
    plt.rcParams["figure.figsize"] = fig_size

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    
    colors = {'nova' : 'xkcd:fuchsia', 't2ksk' : 'xkcd:blue green', 'icupgr' : 'xkcd:peacock blue', 'juno':'xkcd:fire engine red', 'pingu' : 'xkcd:dark sky blue', 'orca' : 'xkcd:muddy brown', 't2hk' : 'xkcd:green', 'dune':'xkcd:violet', 'ino' : 'orange', 't2hkk' : 'xkcd:green',}
    
    fullnames = {'nova' : 'NOvA', 't2ksk' : 'T2K+SuperK', 'icupgr' : 'IceCube Upgrade', 'juno' : 'JUNO', 'pingu' : 'PINGU$^{\star}$', 'orca': 'KM3NeT/ORCA', 't2hk' : 'T2HK', 'dune' : 'DUNE', 'ino' : 'ICAL @ INO$^{\star}$', 't2hkk' : 'T2HKK$^{\star}$'}
    
    position = {'nova' : (2022.5, 3.5), 't2ksk' : (2020.25, 1.5), 'icupgr' : (2025.25, 1.5), 'juno' : (2023.5, 2.5), 'pingu' : (2031, 4.0), 'orca': (2027.5, 4.25), 't2hk' : (2034.5, 4.5), 'dune' : (2029, 8), 'ino' : (2035, 2.5), 't2hkk' : (2033.5, 8)}
    
    starting_year = {'nova' : 0, 't2ksk' : 0, 'icupgr' : 2023, 'juno' : 2022, 'pingu' : 2028, 'orca': 2024, 't2hk' : 2027, 'dune' : 2026, 'ino' : 2025, 't2hkk' : 2027}

#
# Load
#
    filenames = ['nova', 't2ksk', 'icupgr', 'dune', 'pingu', 'orca', 't2hk', 'juno', 'ino', 't2hkk']
    dtype1 = np.dtype([('year', 'f8'), ('min', 'f8'), ('max', 'f8')])
    exps = []
    for exp in filenames:
        result = np.loadtxt('sens_data/'+exp+'.txt', dtype=dtype1, usecols=(0, 1, 2))
        #print(result)
        low = []
        high = []
        for line in result:
            year, min, max = line
            year_ax=year+starting_year[exp]
            low.append((year_ax, min))
            high.append((year_ax, max))
        this_exp = {'id': exp, 'low_values' : low, 'high_values' : high}
        exps.append(this_exp)
    
    #print(exps)

#
# Figure
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.06, right=0.95, top=0.9, bottom=0.2)
    plt.title('Future Mass Hierarchy sensitivity', pad=20)
    ax.set_xlabel('Year')
    ax.set_ylabel('Sensitivity ($\sigma$)')
    ax.set_xlim(2020, 2040)
    ax.set_ylim(0, 10.0)
    plt.yticks([2.0, 4.0, 6.0, 8.0, 10.0])
    text_qual = dict(boxstyle='round', facecolor='white', alpha=0.3, edgecolor ='white')
    ax.set_yticks([1.0, 3.0, 5.0, 7.0, 9.0], minor=True)

    plt.plot([2020.0, 2040.0], [5.0, 5.0], ls='--', color='grey', alpha=0.5)
    
    for count, exp in enumerate(exps):
        revert_max = exp['high_values'][::-1]
        size = len(revert_max) - 1
        color=colors[exp['id']]
        name=fullnames[exp['id']]
        text_place_x=position[exp['id']][0]
        text_place_y=position[exp['id']][1]
        poly = Polygon(exp['low_values'] + revert_max, facecolor=color, edgecolor=color, alpha=0.3, lw=2)
        ax.add_patch(poly)
        if exp['id'] == 't2hkk' or exp['id'] == 'pingu' or exp['id'] == 'ino':
            poly.set_hatch('/')
        ax.text(text_place_x, text_place_y, name, color=color, bbox=text_qual)
        ax.annotate(name, xy=(starting_year[exp['id']], 0), xycoords='data', xytext=(starting_year[exp['id']], -0.7-count*0.23), textcoords='data', arrowprops=dict(facecolor=color, alpha=0.3), ha='center', size = 14)

        
    #plt.minorticks_on()
    plt.grid()
    x_axis = np.arange(2020, 2042, 2)
    #print(x_axis)
    ax.set_xticks(x_axis)
    ax.set_xticklabels(['\\textbf{2020}', '\\textbf{2022}', '\\textbf{2024}', '\\textbf{2026}', '\\textbf{2028}', '\\textbf{2030}', '\\textbf{2032}', '\\textbf{2034}', '\\textbf{2036}', '\\textbf{2038}', '\\textbf{2040}'])
    ax.tick_params(top=True, right=True)
    ax.yaxis.grid(True, which='minor')
    
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

