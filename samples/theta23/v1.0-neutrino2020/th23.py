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
    fig_size = plt.rcParams['figure.figsize']
    fig_size[0] = 8
    fig_size[1] = 4
    plt.rcParams['figure.figsize'] = fig_size
    plt.rcParams['axes.spines.left'] = False
    plt.rcParams['axes.spines.right'] = False

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    colors = {'nova' : 'xkcd:green', 't2k' : 'xkcd:green', 'minos' : 'xkcd:green',
              'superkamiokande' : 'xkcd:azure', 'icecube' : 'xkcd:azure',
              'nufit5.0' : 'xkcd:steel grey', 'foreroetal.' : 'xkcd:steel grey'}

#
# Load
#
    filename = 'amplitude23_NO.dat'
    if args.input:
        filename = args.input
    dtype1 = np.dtype([('id', 'U20'), ('exp', 'U20'), ('oct', 'U20'), ('cv', 'f8'), ('left', 'f8'), ('right', 'f8'), ('latex', 'U30')])
    result = np.loadtxt(filename, dtype=dtype1, skiprows=1, usecols=(0, 1, 4, 5, 6, 7, 9))
    print(result)
    rev_arr = result[::-1]
#
# Figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('$\sin^2 \\theta_{23}$')
    if args.nmo == 'NO':
        plt.title('Normal mass ordering', pad=15)
    if args.nmo == 'IO':
        plt.title('Inverted mass ordering', pad=15)
    plt.subplots_adjust(left=0.25, right=0.8, top=0.9, bottom=0.15)
    ax.set_xlim(0.3,0.7)
    ax.set_ylim(0.5, 7.5)
    plt.plot([0.5, 0.5], [0.5, 7.5], ls='--', color='grey', alpha=0.5)
    
    exp_name = []
    latex_text = []
    latex_lo_text = []
    
    #
    # Iterate data
    #
    
    for count, exp in enumerate(rev_arr):
        id, name, oct, cv, left, right, latex = exp
        name = name.replace('_', ' ')
        if name in exp_name:
            counter=exp_name.index(name)
            plt.errorbar(cv, counter+1, xerr=np.array([[left, right]]).T, color=colors[id], capsize = 2)
            latex_lo_text[counter] = latex
            if oct != 'LO':
                plt.plot(cv, counter+1, 'o', markerfacecolor=colors[id], markeredgecolor=colors[id])
        else:
            exp_name.append(name)
            latex_text.append(latex)
            counter=exp_name.index(name)
            latex_lo_text.append('')
            plt.errorbar(cv, counter+1, xerr=np.array([[left, right]]).T, color=colors[id], capsize = 2)
            if oct != 'LO':
                plt.plot(cv, counter+1, 'o', markerfacecolor=colors[id], markeredgecolor=colors[id])

        
    y_axis = np.arange(1, 8, 1)
    y_axis_2 = np.arange(1.07, 8.07, 1)
    ax.set_yticks(y_axis)
    ax.set_yticklabels(exp_name, ha='left')
    ax.tick_params(axis='y', direction='out', labelleft=True, labelright=False,  pad=120)
    
    double_y = ax.twinx()
    double_y.set_ylim(0.5,7.5)
    double_y.tick_params(axis='y', direction='out', labelleft=False, labelright=True, pad=5)
    double_y.set_yticks(y_axis_2)
    double_y.set_yticklabels(latex_text, ha='left')
    
    triple_y =  ax.twinx()
    triple_y.tick_params(axis='y', direction='in')
    triple_y.set_ylim(0.5,7.5)
    triple_y.tick_params(axis='y', direction='in', labelleft=True, labelright=False, pad=-4,  labelcolor='grey', labelsize=13)
    triple_y.set_yticks(y_axis_2)
    triple_y.set_yticklabels(latex_lo_text, ha='left')
    labels = triple_y.get_yticklabels()
    for label in labels:
        label.set_bbox(dict(fc='white', ec='white'))
    
    ax.set_xticks([0.35, 0.45, 0.55, 0.65], minor=True)
    ax.xaxis.grid(True, which='minor')
    ax.xaxis.grid(True)
    ax.tick_params(axis="x", which="minor", top=True)
    ax.tick_params(top=True, left = False)
    double_y.tick_params(right=False)
    triple_y.tick_params(right=False)
    
    ax.text(0.975, 0.4, 'v1.0 2020.08: git.jinr.ru/nu/osc', rotation=90, color='xkcd:greyish', transform=fig.transFigure, fontsize=11)
    
    outfilename='plot.png'
    if args.output:
        outfilename = args.output
    plt.savefig(outfilename, dpi=300)
    plt.show()
    

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--input', help='file to load')
    parser.add_argument('--nmo', choices=('NO', 'IO'), help='ordering')
    parser.add_argument('--output', help='file to write')

    main(parser.parse_args())

