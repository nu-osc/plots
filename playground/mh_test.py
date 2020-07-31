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
    ax = fig.add_subplot(111)
    ax.set_title('Another hierarchy rejection', pad=15)
    ax.set_xlabel('Sigma')
    plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.15)
    ax.set_xlim(0,7.0)
    ax.set_ylim(0.5,3.5)
    plt.plot([5.0, 5.0], [0, 5.0], ls='--', color='grey', alpha=0.5)
    
    text_itself = []
    text_color = []
    hie_values = []
    hie_proj = []
    order_id = []
    axis_text_1 = []
    axis_text_2 = []
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
        axis_text_1.append('\\textbf{'+str(hie)+'}')
        axis_text_2.append(str(proj))
        eb=plt.errorbar(proj, count+1, yerr=0.4, ls='--', color=colors[id])
        eb[-1][0].set_linestyle('--')
        
    print(hie_values)
    y_axis = np.arange(1, 4, 1)
    #plt.barh(y_axis, hie_values)
    barlist=plt.barh(y_axis, hie_values)
    barlist[0].set_color(colors[order_id[0]])
    barlist[1].set_color(colors[order_id[1]])
    barlist[2].set_color(colors[order_id[2]])
    plt.yticks(y_axis, text_itself)
    ax.set_yticks([1.5, 2.5, 3.5], minor=True)
    
    double_y = ax.twinx()
    double_y.set_ylim(0.5,3.5)
    double_y.tick_params(axis='y', direction='in', labelleft=False, labelright=True, pad=-10)
    double_y.set_yticks(y_axis)
    double_y.set_yticklabels(axis_text_1, ha='right')
    
    triple_y =  ax.twinx()
    triple_y.tick_params(axis='y', direction='out')
    triple_y.set_ylim(0.5,3.5)
    triple_y.tick_params(axis='y', direction='out', labelleft=False, labelright=True, pad=10,  labelcolor='grey')
    triple_y.set_yticks(y_axis)
    triple_y.set_yticklabels(axis_text_2)
    
    ax.yaxis.grid(True, which='minor')
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

