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
    colors = {'nova' : 'xkcd:warm purple', 'superkamiokande' : 'xkcd:azure', 't2k' : 'xkcd:green'}

#
# Load
#
    filename = ''
    if args.input:
        filename = args.input
    dtype1 = np.dtype([('id', '|U20'), ('exp', '|U20'), ('hie', 'f8'), ('proj', 'f8')])
    result = np.loadtxt(filename, dtype=dtype1, usecols=(0, 1, 2, 3))
    print(result)

#
# Figure
    fig = plt.figure()
    plt.title('Another hierarchy rejection', pad=15)
    plt.xlabel('Sigma')
    plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.15)
    plt.xlim(0,6.0)
    plt.ylim(0.5,3.5)
    
    text_itself = []
    text_color = []
    hie_values = []
    hie_proj = []
    order_id = []
        
    #
    # Iterate data
    #
    styles, labels = [], []
    for count, exp in enumerate(result):
        id, name, hie, proj = exp
        text_itself.append(name)
        text_color.append(colors[id])
        hie_values.append(hie)
        hie_proj.append(proj)
        order_id.append(id)
        #plt.plot(hie, count+1, 'o', markeredgecolor=colors[id], markersize=8, markerfacecolor=colors[id])
        #plt.plot(prog, count+1, 'o', markeredgecolor=colors[id], markersize=8, markerfacecolor='white')
        eb=plt.errorbar(proj, count+1, yerr=0.4, ls='--', color=colors[id])
        eb[-1][0].set_linestyle('--')
        
    print(hie_values)
    y_axis = np.arange(1, 4, 1)
    plt.barh(y_axis, hie_values)
    barlist=plt.barh(y_axis, hie_values)
    barlist[0].set_color(colors[order_id[0]])
    barlist[1].set_color(colors[order_id[1]])
    barlist[2].set_color(colors[order_id[2]])
    plt.yticks(y_axis, text_itself)
    
    double_y = plt.twinx()
    double_y.set_ylim(0.5,3.5)
    double_y.tick_params(axis='y', direction='in', labelleft=True, labelright=False, pad= -25)
    double_y.set_yticks(y_axis)
    double_y.set_yticklabels(hie_values)
    
    
    plt.minorticks_on()
    plt.grid()
    
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

