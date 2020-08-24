#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle
import itertools as it
import re

from style import colors, names, dayabay, titles
from reference import reference, variable, lims
dtype1 = np.dtype([('id', 'U20'), ('exp', 'U20'), ('type', 'U50'), ('notes', 'U20'), ('ordering', 'U2'), ('octant', 'U2'),  ('value', 'f8'), ('left', 'f8'), ('right', 'f8'), ('span', 'f8'), ('result', 'U30')])

def main(args):
    #
    # Extra style
    #
    if args.dayabay:
        dayabay()

    #
    # RC params
    #
    plt.rc('text', usetex=True)
    plt.rcParams['grid.alpha'] = 0.1
    plt.rcParams['grid.linewidth'] = 2
    plt.rcParams.update({'font.size': 15, 'font.family': 'serif'})
    plt.rcParams.update({'legend.fontsize': 18})
    plt.rcParams['axes.spines.left'] = False
    plt.rcParams['axes.spines.right'] = False

    #
    # Load
    #
    result = np.loadtxt(args.input, dtype=dtype1, skiprows=1, usecols=range(11))
    result = result[::-1]
    if args.exclude:
        result = [res for res in result if args.exclude not in res['type']]
    nitems = len(result)

    ordering = result[0]['ordering']
    title = titles.get(ordering)

    #
    # Figure
    #
    singleheight = 0.3
    fracbottom = 2.3
    fractop    = 1.2
    fracax     = 1.
    figheight  = (nitems+fractop+fracbottom+fracax)*singleheight
    axtop      = 1.0-fractop*singleheight/figheight
    fig = plt.figure(figsize=(8,figheight))
    ax = fig.add_subplot(111)
    ax.minorticks_on()
    ax.set_xlabel(variable)
    ax.set_ylim(1.0-fracax*0.5, nitems+fracax*0.5)
    if title:
        ax.set_title(title)
    if lims:
        ax.set_xlim(lims)
    ax.tick_params(axis='x', which='both', top=True)
    ax.xaxis.grid(True)
    padleft = 80
    namewidth = '38mm'
    plt.subplots_adjust(left=0.18, right=0.82, top=axtop, bottom=fracbottom*singleheight/figheight)

    #
    # Iterate data
    #
    exp_name = []
    latex_text = []
    offset=0
    for count, exp in enumerate(result):
        id, name, typ, _, ordering, _, value, left, right, _, latex = exp

        kwargs=dict()
        if args.dayabay and 'Daya_Bay' in name:
            kwargs['elinewidth'] = 2.0
        plt.errorbar(value, count+1, xerr=np.array([[left, right]]).T, color=colors[id], capsize = 2, **kwargs)
        plt.plot(value, count+1, 'o', markerfacecolor=colors[id], markeredgecolor=colors[id])

        name = name.replace('_', ' ')
        if args.dayabay:
            name = name.replace('Daya Bay', r'\textbf{Daya Bay}')

        name = names.get(name, name)
        name = f'\\parbox{{{namewidth}}}{{{name}\\hfill{{}}{notes}}}'
        exp_name.append(name)

        latex=re.sub(r'\.(\d\d\d)\\pm', r'.\1{\\phantom{0}}\\pm', latex)
        if args.sym:
            latex=re.subn(r'(\\pm([0-9]\.)?[0-9]+)', r'{\\scriptstyle\1}', latex)[0]

        latex_text.append(latex)

    #
    # Setup ticks and labels
    #
    # Left: experiment names
    yticks = np.arange(1, len(exp_name)+1)
    ax.set_yticks(yticks)
    ax.set_yticklabels(exp_name, ha='left')
    ax.tick_params(axis='y', direction='out', labelleft=True, labelright=False, pad=padleft)

    # Right: values
    double_y = ax.twinx()
    double_y.set_ylim(ax.get_ylim())
    ax.tick_params(axis='y', which='both', left=False)
    double_y.tick_params(axis='y', which='both', direction='out', left=False, labelleft=False, right=False, labelright=True, pad=5)
    double_y.set_yticks(yticks)
    double_y.set_yticklabels(latex_text, ha='left')

    ax.text(1.0, 0.5, reference, rotation=90, alpha=0.3, transform=fig.transFigure, ha='right', va='center', fontsize='x-small')

    if args.output:
        plt.savefig(args.output, dpi=300)
        print('Write output file', args.output)

    if args.show:
        plt.show()

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('input', help='file to load')
    parser.add_argument('-o', '--output', help='file to write')
    parser.add_argument('-s', '--show', action='store_true', help='show')
    parser.add_argument('-e', '--exclude', help='types mask to exclude (tested with contains)')
    parser.add_argument('--sym', default=True, action='store_true', help='make symmetric error smaller')
    parser.add_argument('--no-sym', action='store_false', dest='sym', help='do not make make symmetric error smaller')
    parser.add_argument('--dayabay', action='store_true', help='style for Daya Bay')

    main(parser.parse_args())

