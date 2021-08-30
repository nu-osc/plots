#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle
import itertools as it
import re
from argparse import ArgumentParser

import configuration as cfg
dtype1 = np.dtype([('id', 'U20'), ('exp', 'U20'), ('type', 'U50'), ('notes', 'U20'), ('ordering', 'U2'), ('digits', 'i1'), ('value', 'f8'), ('left', 'f8'), ('right', 'f8'), ('span', 'f8')])

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
    # plt.rcParams['text.latex.preamble']+=preamble

    #
    # Load
    #
    result = np.loadtxt(args.input, dtype=dtype1, skiprows=1, usecols=range(10))
    result = result[::-1]
    if args.exclude:
        mask = [args.exclude not in res['type'] for res in result]
        result = result[mask]
    uniqnames = dict(zip(*np.unique(np.core.defchararray.add(result['exp'],result['notes']), return_counts=True)))
    nitems = len(uniqnames)
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
    ax.set_xlabel(cfg.variable)
    ax.set_ylim(1.0-fracax*0.5, nitems+fracax*0.5)
    if cfg.lims:
        ax.set_xlim(cfg.lims)
    ax.tick_params(axis='x', which='both', top=True)
    ax.xaxis.grid(True)
    padleft = 110
    namewidth = '38mm'
    right = digits_max>4 and 0.76 or 0.78
    plt.subplots_adjust(left=0.22, right=right, top=axtop, bottom=fracbottom*singleheight/figheight)

    #
    # Iterate data
    #
    exp_name = []
    latex_text = []
    duplicates = {}
    occurances = {}
    offset=0
    for i, exp in enumerate(result):
        id, name, typ, notes, ordering, digits, value, left, right, _ = exp
        count=i-offset
        sigma = 0.5*(right+left)

        uname = name+notes
        try:
            count=duplicates[uname]
            duplicate=True
            offset+=1
            occurances[uname]+=1
            occurance = occurances[uname]
        except KeyError:
            duplicates[uname]=count
            duplicate=False
            occurances[uname], occurance=0, 0

        voffset = occurance/(uniqnames[uname]-1)-0.5 if uniqnames[uname]>1 else 0.0
        vpos = count+1 + voffset*0.2

        ekwargs=dict(capsize=2, color=cfg.colors[id])
        pkwargs=dict(marker='o', color=cfg.colors[id])
        if sigma/value<0.01:
            pkwargs['marker']='|'

        name = name.replace('_', ' ')
        if args.dayabay and 'Daya Bay' in name:
            ekwargs['elinewidth'] = 2.0
        if ordering=='IO':
            ekwargs['alpha'] = 0.4
            pkwargs['alpha'] = 0.4
            pkwargs['marker'] = '|'

        if args.dayabay:
            name = name.replace('Daya Bay', r'\textbf{Daya Bay}')

        elines = plt.errorbar(value, vpos, xerr=np.array([[left, right]]).T, **ekwargs)

        plt.plot(value, vpos, **pkwargs)

        if ordering=='IO':
            elines[-1][0].set_linestyle('dashed')
            continue

        name = cfg.names.get(name, name)
        name = f'\\parbox{{{namewidth}}}{{{name}\\hfill{{}}{notes}{ordering}}}'
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
    ax_right_right = ax.twinx()
    ax_right_right.set_ylim(ax.get_ylim())
    ax.tick_params(axis='y', which='both', left=False)
    ax_right_right.tick_params(axis='y', which='both', direction='out', left=False, labelleft=False, right=False, labelright=True, pad=0)
    ax_right_right.set_yticks(yticks)
    ax_right_right.set_yticklabels(latex_text, ha='left')

    ax.text(1.0, 0.5, cfg.reference, rotation=90, alpha=0.3, transform=fig.transFigure, ha='right', va='center', fontsize='x-small')

    if args.output:
        plt.savefig(args.output, dpi=300)
        print('Write output file', args.output)

    if args.show:
        plt.show()

def format_latex(digits, value, left, right, digits_max):
    value*=100
    left*=100
    right*=100
    digits-=2
    digits_max-=2

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

    width1_rel='27mm'
    width2_rel='11mm'
    box1 = f'\\makebox[{width1_rel}]{{', r'\hfill}'
    box2 = f'\\makebox[{width2_rel}]{{', r'\hfill}'

    ret=''
    if left==right:
        ret = f'{box1[0]}${value}{extra}{{\\scriptstyle\\pm{left}}}${box1[1]}'
    else:
        ret = f'{box1[0]}${value}{extra}^{{+{right}}}_{{-{left}}}${box1[1]}'

    ret+=f'{box2[0]}\\hspace{{\\fill}}\\small{relsigma:.1f}\\%{box2[1]}'

    return ret

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input', help='file to load')
    parser.add_argument('-o', '--output', help='file to write')
    parser.add_argument('-s', '--show', action='store_true', help='show')
    parser.add_argument('-e', '--exclude', help='types mask to exclude (tested with contains)')
    parser.add_argument('--dayabay', action='store_true', help='style for Daya Bay')

    main(parser.parse_args())

