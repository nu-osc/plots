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
dtype1 = np.dtype([('id', 'U20'), ('exp', 'U20'), ('type', 'U50'), ('notes', 'U20'), ('ordering', 'U2'), ('octant', 'U2'), ('digits', 'i1'), ('value', 'f8'), ('left', 'f8'), ('right', 'f8'), ('span', 'f8')])

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
        mask   = [args.exclude not in res['type'] for res in result]
        result = result[mask]
    nitems = len(result)
    digits_max = result['digits'].max()

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
    padleft = 75
    namewidth = '38mm'
    plt.subplots_adjust(left=0.16, right=0.84, top=axtop, bottom=fracbottom*singleheight/figheight)

    #
    # Iterate data
    #
    exp_name = []
    latex_text = []
    for count, exp in enumerate(result):
        id, name, typ, notes, ordering, _, digits, value, left, right, _ = exp

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

        latex = format_latex(digits, value, left, right, digits_max)
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

def format_latex(digits, value, left, right, digits_max):
    if digits<digits_max:
        extra = '0'*(digits_max-digits)
        extra = f'\\phantom{{{extra}}}'
    else:
        extra = ''

    value = f'{value:.{digits}f}'
    left = f'{left:.{digits}f}'
    right = f'{right:.{digits}f}'
    if left==right:
        ret = f'${value}{extra}{{\\scriptstyle\\pm{left}}}$'
    else:
        ret = f'${value}{extra}^{{+{right}}}_{{-{left}}}$'

    return ret

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

