#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle
import itertools as it

from style import colors, names, titles
from reference import reference, variable, lims
dtype1 = np.dtype([('id', 'U20'), ('exp', 'U20'), ('notes', 'U30'), ('ordering', 'U4'), ('oct', 'U20'), ('digits', 'i1'), ('value', 'f8'), ('left', 'f8'), ('right', 'f8'), ('span', 'f8')])
def main(args):
    if args.nmo=='auto':
        if 'NO' in args.output:
            assert not 'IO' in args.output
            args.nmo='NO'
        elif 'IO' in args.output:
            args.nmo='IO'
        else:
            raise Exception('Unable to determine ordering')

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
    nitems = len(result)
    digits_max = result['digits'].max()

    #
    # Figure
    #
    singleheight = 0.25
    fracbottom = 2.4
    fractop    = 1.8
    fracax     = 1.
    figheight  = (nitems+fractop+fracbottom+fracax)*singleheight
    axtop      = 1.0-fractop*singleheight/figheight
    fig = plt.figure(figsize=(8,figheight))
    ax = fig.add_subplot(111)
    ax.minorticks_on()
    ax.set_xlabel(variable)
    ax.set_ylim(1.0-fracax*0.5, nitems+fracax*0.5-1)
    ax.set_xlim(lims)
    ax.tick_params(axis='x', which='both', top=True)
    ax.xaxis.grid(True)
    padleft=80
    plt.subplots_adjust(left=0.16, right=0.84, top=axtop, bottom=fracbottom*singleheight/figheight)

    plt.title(titles.get(args.nmo, '???'), pad=15)
    plt.plot([0.5, 0.5], [0.5, 7.5], ls='--', color='grey', alpha=0.5)

    #
    # Iterate data
    #
    exp_name = []
    latex_text = []
    latex_lo_text = []
    for count, exp in enumerate(result):
        id, name, _, _, oct, digits, value, left, right, _ = exp
        name = name.replace('_', ' ')

        latex = format_latex(digits, value, left, right, digits_max)

        name = names.get(name, name)
        if name in exp_name:
            counter=exp_name.index(name)
            plt.errorbar(value, counter+1, xerr=np.array([[left, right]]).T, color=colors[id], capsize = 2)
            latex_lo_text[counter] = latex
            if oct != 'LO':
                plt.plot(value, counter+1, 'o', markerfacecolor=colors[id], markeredgecolor=colors[id])
        else:
            exp_name.append(name)
            latex_text.append(latex)
            counter=exp_name.index(name)
            latex_lo_text.append('')
            plt.errorbar(value, counter+1, xerr=np.array([[left, right]]).T, color=colors[id], capsize = 2)
            if oct != 'LO':
                plt.plot(value, counter+1, 'o', markerfacecolor=colors[id], markeredgecolor=colors[id])

    #
    # Setup ticks and labels
    #
    ticklabeloffset_right = 0.07
    ticklabeloffset_left = 0.04

    # Left: experiment names
    yticks = np.arange(1, len(exp_name)+1)
    ax.set_yticks(yticks)
    ax.set_yticklabels(exp_name, ha='left')
    ax.tick_params(axis='y', direction='out', labelleft=True, labelright=False,  pad=padleft)

    # Right: values
    double_y = ax.twinx()
    double_y.set_ylim(ax.get_ylim())
    double_y.set_yticks(yticks+ticklabeloffset_right)
    double_y.set_yticklabels(latex_text, ha='left')

    # Left: extra values
    triple_y =  ax.twinx()
    triple_y.tick_params(axis='y', direction='in')
    triple_y.set_ylim(0.5,7.5)
    triple_y.set_yticks(yticks+ticklabeloffset_left)
    triple_y.set_yticklabels(latex_lo_text, ha='left', va='center_baseline')
    labels = triple_y.get_yticklabels()
    for label in labels:
        label.set_bbox(dict(fc='white', ec='white'))

    ax.tick_params(      axis='y', which='both', left=False, right=False)
    double_y.tick_params(axis='y', which='both', left=False, right=False, direction='out', labelleft=False, labelright=True,  pad=5)
    triple_y.tick_params(axis='y', which='both', left=False, right=False, direction='in',  labelleft=True,  labelright=False, pad=-4, labelcolor='grey', labelsize='small')

    ax.text(1.0, axtop, reference, rotation=90, alpha=0.3, transform=fig.transFigure, ha='right', va='top', fontsize='x-small')

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
    parser.add_argument('--nmo', choices=('NO', 'IO', 'auto'), default='auto', help='ordering')
    parser.add_argument('-o', '--output', help='file to write')
    parser.add_argument('-s', '--show', action='store_true', help='show')

    main(parser.parse_args())

