#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle
import itertools as it
import re
from argparse import ArgumentParser

from style import colors, names, preamble, dayabay, titles
from reference import reference, variable, lims

dtype1 = np.dtype([('id', 'U20'), ('exp', 'U20'), ('type', 'U50'), ('measurement', 'U20'), ('dataset', 'U20'), ('notes', 'U20'), ('ordering', 'U2'), ('octant', 'U2'), ('digits', 'i1'), ('value', 'f8'), ('left', 'f8'), ('right', 'f8'), ('span', 'f8')])

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
    plt.rcParams['text.latex.preamble']+=preamble

    #
    # Load
    #
    result = np.loadtxt(args.input, dtype=dtype1, skiprows=1, usecols=range(13))
    if args.exclude:
        mask = [all(pattern not in res['type'] and pattern not in res['measurement'] for pattern in args.exclude) for res in result]
        result = result[mask]
    result = np.sort(result, axis=- 1, kind=None, order=("measurement", "span"))
    result = result[::-1]
    nitems = len(result)
    digits_decimal_max = result['digits'].max()
    line_place = sum(item['measurement'] == 'estimation' for item in result)

    logs10 = ceil_from_zero(np.log10(result['value']))
    digits_leading_max = int(max(1.0, *logs10))

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
    fig = plt.figure(figsize=(9,figheight))
    ax = fig.add_subplot(111)
    ax.minorticks_on()
    ax.set_xlabel(variable)
    ax.set_ylim(1.0-fracax*0.5, nitems+fracax*0.5)
    if title:
        ax.set_title(title)
    if xlims:=lims.get(ordering):
        ax.set_xlim(xlims)
    ax.tick_params(axis='x', which='both', top=True)
    ax.xaxis.grid(True)
    padleft = 95
    # namewidth = '40mm'
    namewidth = '37mm'
    plt.subplots_adjust(left=0.16, right=0.795, top=axtop, bottom=fracbottom*singleheight/figheight)

    #
    # Iterate data
    #
    exp_name = []
    latex_text = []
    for count, exp in enumerate(result):
        id, name, typ, measurement, dataset, notes, ordering, _, digits, value, left, right, _ = exp

        sigma = 0.5*(right+left)

        kwargs=dict()
        if args.dayabay and 'Daya_Bay' in name:
            kwargs['elinewidth'] = 2.0
        plt.errorbar(value, count+1, xerr=np.array([[left, right]]).T, color=colors[id], capsize = 2, **kwargs)

        marker='o'
        if sigma/value<0.01:
            marker='|'
        plt.plot(value, count+1, marker, markerfacecolor=colors[id], markeredgecolor=colors[id])

        name = name.replace('_', ' ')
        notes = notes.replace('_', ' ')
        dataset = dataset.replace('_', ' ')


        if args.dayabay:
            name = name.replace('Daya Bay', r'\textbf{Daya Bay}')

        name = names.get(name, name)

        if measurement == 'estimation':
            name = f'\\makebox[{namewidth}]{{{name} {{\\relsize{{-1}}({dataset}) {notes}}}'
        else:
            name = f'\\makebox[{namewidth}]{{{name} \\hfill{{}}{notes}}}'

        exp_name.append(name)

        latex = format_latex(digits, value, left, right, digits_leading_max, digits_decimal_max)
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
    ax_right_right.tick_params(axis='y', which='both', direction='out', left=False, labelleft=False, right=False, labelright=True, pad=5)
    ax_right_right.set_yticks(yticks)
    ax_right_right.set_yticklabels(latex_text, ha='left')

    if not args.dayabay:
        ax.text(1.0, 0.5, reference, rotation=90, alpha=0.3, transform=fig.transFigure, ha='right', va='center', fontsize='x-small')

    if line_place > 0:
        plt.axhline(nitems-line_place+0.5, ls='--', color='grey', linewidth=1, alpha=0.5)

    if args.output:
        plt.savefig(args.output, dpi=300)
        print('Write output file', args.output)

    if args.show:
        plt.show()

def ceil_from_zero(nums):
    nums = np.asanyarray(nums)
    nums[nums<0] = np.floor(nums[nums<0])
    nums[nums>0] = np.ceil(nums[nums>0])
    return nums

def phantom_zeros(num, num_max):
    if num>=num_max:
        return ''

    extra = '0'*(num_max-num)
    # return extra
    # return f'{{\color{{red}}{extra}}}'
    return f'\phantom{{{extra}}}'

def format_latex(digits_decimal, value, left, right, digits_leading_max, digits_decimal_max):
    digits_leading = int(ceil_from_zero(np.log10(value)))

    zeros_leading = phantom_zeros(digits_leading, digits_leading_max)
    zeros_decimal = phantom_zeros(digits_decimal, digits_decimal_max)

    #print(f'{value=:.6f} {digits_decimal=} {digits_leading=} {digits_leading_max=} {digits_decimal_max=} {zeros_leading=} {zeros_decimal=}')

    span = right+left
    relsigma = 100*0.5*span/value

    value = f'{value:.{digits_decimal}f}'
    left = f'{left:.{digits_decimal}f}'
    right = f'{right:.{digits_decimal}f}'

    the_value = f'{zeros_leading}{value}{zeros_decimal}'
    if left==right:
        the_error = f'{{\\scriptstyle\\pm{left}{zeros_decimal}}}'
    else:
        the_error = f'^{{+{right}{zeros_decimal}}}_{{-{left}{zeros_decimal}}}'

    width1_rel='24mm'
    width2_rel='13mm'
    ret = [
            f'\\makebox[{width1_rel}]{{\\hspace*{{\\fill}}${the_value}{the_error}$}}',
            f'\\makebox[{width2_rel}]{{\\hspace*{{\\fill}}\\relsize{{-1}}{relsigma:.1f}\\%}}'
          ]

    # return ''.join(f'\\fbox{{{s}}}' for s in ret)
    return ''.join(ret)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input', help='file to load')
    parser.add_argument('-o', '--output', help='file to write')
    parser.add_argument('-s', '--show', action='store_true', help='show')
    parser.add_argument('-e', '--exclude', nargs='+', help='types mask to exclude (tested with contains)')
    parser.add_argument('--dayabay', action='store_true', help='style for Daya Bay')

    main(parser.parse_args())

