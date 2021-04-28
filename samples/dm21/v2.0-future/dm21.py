#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle
import itertools as it
import re
from argparse import ArgumentParser, Namespace

from style import colors, names
from reference import reference, variable, lims
dtype1 = np.dtype([('id', 'U20'), ('exp', 'U20'), ('type', 'U50'), ('notes', 'U20'), ('digits', 'i1'), ('value', 'f8'), ('left', 'f8'), ('right', 'f8'), ('span', 'f8')])

args = Namespace()

def main():
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
    result = np.loadtxt(args.input, dtype=dtype1, skiprows=1, usecols=range(9))
    result = result[::-1]
    if args.exclude:
        mask = [args.exclude not in res['type'] for res in result]
        result = result[mask]
    nitems = len(result)
    digits_max = result['digits'].max()

    #
    # Figure
    #
    singleheight = 0.3
    fracbottom = 2.3
    fractop    = 0.5
    fracax     = 1.
    figheight  = (nitems+fractop+fracbottom+fracax)*singleheight
    axtop      = 1.0-fractop*singleheight/figheight
    fig = plt.figure(figsize=(8,figheight))
    ax = fig.add_subplot(111)
    ax.minorticks_on()
    ax.set_xlabel(variable)
    ax.set_ylim(1.0-fracax*0.5, nitems+fracax*0.5)
    if lims:
        ax.set_xlim(lims)
    ax.tick_params(axis='x', which='both', top=True)
    ax.xaxis.grid(True)
    plt.subplots_adjust(left=0.30, right=0.81, top=axtop, bottom=fracbottom*singleheight/figheight)

    #
    # Iterate data
    #
    exp_name = []
    latex_text = []
    for count, exp in enumerate(result):
        id, name, _, typ, digits, value, left, right, _ = exp
        sigma = 0.5*(right+left)

        plt.errorbar(value, count+1, xerr=np.array([[left, right]]).T, color=colors[id], capsize = 2)
        marker='o'
        if sigma<0.1:
            marker='|'
        plt.plot(value, count+1, marker, markerfacecolor=colors[id], markeredgecolor=colors[id])

        name = name.replace('_', ' ')
        exp_name.append(names.get(name, name))

        latex = format_latex(digits, value, left, right, digits_max)
        latex_text.append(latex)

    #
    # Setup ticks and labels
    #
    # Left: experiment names
    yticks = np.arange(1, len(exp_name)+1)
    ax.set_yticks(yticks)
    ax.set_yticklabels(exp_name, ha='left')
    ax.tick_params(axis='y', direction='out', labelleft=True, labelright=False, pad=150)

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

    span = right+left
    relsigma = 100*0.5*span/value

    value = f'{value:.{digits}f}'
    left = f'{left:.{digits}f}'
    right = f'{right:.{digits}f}'

    width1_rel='22mm'
    width2_rel='9mm'
    box1 = f'\\makebox[{width1_rel}]{{', '}'
    box2 = f'\\makebox[{width2_rel}]{{', '}'

    if left==right:
        ret = f'{box1[0]}${value}{extra}{{\\scriptstyle\\pm{left}}}${box1[1]}'
    else:
        ret = f'{box1[0]}${value}{extra}^{{+{right}}}_{{-{left}}}${box1[1]}'

    ret+=f' {box2[0]}\\hspace*{{\\fill}}\\small{relsigma:.1f}\\%{box2[1]}'

    return ret

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input', help='file to load')
    parser.add_argument('-o', '--output', help='file to write')
    parser.add_argument('-s', '--show', action='store_true', help='show')
    parser.add_argument('-e', '--exclude', help='types mask to exclude (tested with contains)')
    parser.parse_args(namespace=args)

    main()

