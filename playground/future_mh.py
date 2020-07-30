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
    colors = {'nova' : 'xkcd:warm purple', 't2ksk' : 'xkcd:azure', 't2k' : 'xkcd:green', 'icupgr' : 'grey', 'juno':'red', 'pingu' : 'blue', 'orca' : 'violet', 't2hk' : 'green', 'dune':'gold'}
    fullnames = {'nova' : 'NOvA', 't2ksk' : 'T2K+SuperK', 'icupgr' : 'IceCube Upgrade', 'juno' : 'JUNO', 'pingu' : 'PINGU', 'orca': 'KM3NeT/ORCA', 't2hk' : 'T2HK', 'dune' : 'DUNE'}

#
# Load
#
    filenames = ['nova', 't2ksk', 'icupgr', 'juno', 'pingu', 'orca', 't2hk', 'dune']
    dtype1 = np.dtype([('year', 'f8'), ('min', 'f8'), ('max', 'f8')])
    exps = []
    for exp in filenames:
        result = np.loadtxt('sens_data/'+exp+'.txt', dtype=dtype1, usecols=(0, 1, 2))
        print(result)
        low = []
        high = []
        for line in result:
            year, min, max = line
            low.append((year, min))
            high.append((year, max))
        this_exp = {'id': exp, 'low_values' : low, 'high_values' : high}
        exps.append(this_exp)
    
    print(exps)

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
        text_place_x=exp['low_values'][0][0]+(revert_max[0][0]-exp['low_values'][0][0])/4
        text_place_y=revert_max[0][1] - 0.2
        poly = Polygon(exp['low_values'] + revert_max, facecolor=color, edgecolor=color, alpha=0.3)
        ax.add_patch(poly)
        ax.text(text_place_x, text_place_y, name, color=color)
        

        
    #print(hie_values)
    #y_axis = np.arange(1, 4, 1)
    #plt.barh(y_axis, hie_values)
    #barlist=plt.barh(y_axis, hie_values)
    #barlist[0].set_color(colors[order_id[0]])
    #barlist[1].set_color(colors[order_id[1]])
    #barlist[2].set_color(colors[order_id[2]])
    #plt.yticks(y_axis, text_itself)
    
    #double_y = plt.twinx()
    #double_y.set_ylim(0.5,3.5)
    #double_y.tick_params(axis='y', direction='in', labelleft=True, labelright=False, pad= -25)
    #double_y.set_yticks(y_axis)
    #double_y.set_yticklabels(hie_values)
    
    #plt.minorticks_on()
    plt.grid()
    
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

