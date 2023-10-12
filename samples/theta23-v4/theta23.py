#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle
import matplotlib as mpl
import itertools as it
from argparse import ArgumentParser

# mpl.use('pgf')

import configuration as cfg
dtype1 = np.dtype([
    ('id', 'U20'), ('exp', 'U20'), ('type', 'U50'),
    ('notes', 'U30'), ('measurement', 'U20'), ('dataset', 'U40'),
    ('ordering', 'U4'), ('oct', 'U20'), ('preferred', 'bool'),
    ('digits', 'i1'),
    ('value', 'f8'), ('left', 'f8'), ('right', 'f8'), ('span', 'f8'),
    ('preliminary', 'bool')
])
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
    plt.rcParams['pgf.texsystem']='pdflatex'
    plt.rcParams['pgf.preamble']+=cfg.preamble
    plt.rcParams['text.latex.preamble']+=cfg.preamble

    #
    # Load
    #
    result = np.loadtxt(args.input, dtype=dtype1, skiprows=1, usecols=range(15))
    if args.exclude:
        mask = [all(pattern not in res[source] for source in ('type', 'notes', 'measurement') for pattern in args.exclude) for res in result]
        result = result[mask]
    result = np.sort(result, axis=- 1, kind=None, order=("measurement", "span"))
    result = result[::-1]
    nitems = len(result)
    digits_decimal_max = result['digits'].max()
    line_place = sum(item['measurement'] == 'estimation' for item in result)

    names_unique = np.unique(result['exp'])
    nitems_unique = len(names_unique)

    logs10 = ceil_from_zero(np.log10(result['value']))
    digits_leading_max = int(max(1.0, *logs10))

    ordering=args.nmo
    title = cfg.titles.get(ordering)
    #
    # Figure
    #
    singleheight = 0.25
    fracbottom = 2.4
    fractop    = 1.8
    fracax     = 1.
    figheight  = (nitems_unique+fractop+fracbottom+fracax)*singleheight
    axtop      = 1.0-fractop*singleheight/figheight
    fig = plt.figure(figsize=(10,figheight))
    ax = fig.add_subplot(111)
    ax.minorticks_on()
    ax.set_xlabel(cfg.variable)
    ax.set_ylim(1.0-fracax*0.5, nitems_unique+fracax*0.5)
    if cfg.lims:
        ax.set_xlim(cfg.lims)
    if title:
        ax.set_title(title)
    ax.tick_params(axis='x', which='both', top=True)
    ax.xaxis.grid(True)
    if 'estimation' in args.exclude:
        if 'theor' in args.exclude:
            padleft=60
            left=0.10
        else:
            padleft=86
            left=0.14
    else:
        padleft=120
        left=0.18
    plt.subplots_adjust(left=left, right=0.82, top=axtop, bottom=fracbottom*singleheight/figheight)

    plt.axvline(0.5, ls='--', color='grey', alpha=0.5)

    #
    # Iterate data
    #
    exp_name = []
    latex_text = []
    latex_left_text = []
    latex_right_text = []
    haspreliminary = False
    for count, exp in enumerate(result):
        id, name, _, note, measurement, dataset, _, oct, preferred, digits, value, left, right, _, preliminary = exp
        sigma = 0.5*(right+left)
        haspreliminary|=preliminary

        name = name.replace('_', ' ')
        name = cfg.names.get(name, name)
        note = note.replace('_', ' ')

        font=''
        if preliminary:
            font=r'\slshape{}'
        name = f'{{{font}{name}}}'

        dataset = dataset.replace('_', ' ')
        if measurement == 'estimation':
            if note and note!='{}':
                name =  f'{name} {{\\relsize{{-1}}({dataset}) {note}}}'
            else:
                name = f'{name} {{\\relsize{{-1}}({dataset})}}'

        name = name.replace("'" , "")
        latex      = format_latex(digits, value, left, right, digits_leading_max, digits_decimal_max, addspaces=True, percentage=True)
        latex_secondary = format_latex(digits, value, left, right, digits_leading_max, digits_decimal_max, addspaces=False, percentage=False)

        if name not in exp_name:
            exp_name.append(name)
            latex_text.append('')
            latex_left_text.append('')
            latex_right_text.append('')

        counter=exp_name.index(name)

        if preferred:
            latex_text[counter]=latex
        else:
            continue
            if oct=='LO':
                latex_left_text[counter] = latex_secondary
            else:
                latex_right_text[counter] = latex_secondary

        plt.errorbar(value, counter+1, xerr=np.array([[left, right]]).T, color=cfg.colors[id], capsize = 2)
        fcolor = preferred and cfg.colors[id] or 'white'
        plt.plot(value, counter+1, 'o', markerfacecolor=fcolor, markeredgecolor=cfg.colors[id])

    #
    # Setup ticks and labels
    #
    ticklabeloffset_right = 0.07
    ticklabeloffset_left = 0.04
    ticklabeloffset_right2 = 0.04

    # Left: experiment cfg.names
    yticks = np.arange(1, len(exp_name)+1)
    ax.set_yticks(yticks)
    ax.set_yticklabels(exp_name, ha='left')
    ax.tick_params(axis='y', direction='out', labelleft=True, labelright=False, pad=padleft)

    # Right: values
    ax_right_right = ax.twinx()
    ax_right_right.set_ylim(ax.get_ylim())
    ax_right_right.tick_params(axis='y', which='both', direction='out', left=False, labelleft=False, right=False, labelright=True, pad=-100)
    ax_right_right.set_yticks(yticks+ticklabeloffset_right)
    ax_right_right.set_yticklabels(latex_text, ha='left')

    # Left: extra values
    triple_y =  ax.twinx()
    triple_y.tick_params(axis='y', direction='in')
    triple_y.set_ylim(ax.get_ylim())
    triple_y.set_yticks(yticks+ticklabeloffset_left)
    triple_y.set_yticklabels(latex_left_text, ha='left', va='center_baseline')
    triple_y.tick_params(axis='y', which='both', left=False, right=False, direction='in',  labelleft=True,  labelright=False, pad=-4, labelcolor='grey', labelsize='small')
    for label in triple_y.get_yticklabels():
        label.set_backgroundcolor('white')
        bbox = label.get_bbox_patch()
        bbox.set_alpha(0.8)

    # Left: extra values
    fourth_y =  ax.twinx()
    fourth_y.tick_params(axis='y', direction='in')
    fourth_y.set_ylim(ax.get_ylim())
    fourth_y.set_yticks(yticks+ticklabeloffset_right2)
    fourth_y.set_yticklabels(latex_right_text, ha='right', va='center_baseline')
    fourth_y.tick_params(axis='y', which='both', left=False, right=False, direction='in',  labelleft=False,  labelright=True, pad=-4, labelcolor='grey', labelsize='small')
    for label in fourth_y.get_yticklabels():
        label.set_backgroundcolor('white')
        bbox = label.get_bbox_patch()
        bbox.set_alpha(0.8)

    ax.tick_params(axis='y', which='both', left=False, right=False)
    ax_right_right.tick_params(axis='y', which='both', left=False, right=False, direction='out', labelleft=False, labelright=True,  pad=5)

    ax.text(1.0, 0.5, cfg.reference, rotation=90, alpha=0.3, transform=fig.transFigure, ha='right', va='center', fontsize='x-small')
    legend = r'\noindent'
    if haspreliminary:
        legend += r'{\slshape{}Preliminary}'
    legend += r'\\Published'
    ax.text(0.03, 0.05, legend, alpha=0.3, transform=fig.dpi_scale_trans, ha='left', va='bottom', fontsize='x-small')

    if line_place > 0:
        plt.axhline(nitems_unique-line_place+0.5, ls='--', color='grey', linewidth=1, alpha=0.5)

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

def format_latex(digits_decimal, value, left, right, digits_leading_max, digits_decimal_max, *, addspaces=True, percentage=False):
    digits_leading = max(0, int(ceil_from_zero(np.log10(value))))

    if addspaces:
        zeros_leading = phantom_zeros(digits_leading, digits_leading_max)
        zeros_decimal = phantom_zeros(digits_decimal, digits_decimal_max)
    else:
        zeros_leading = ''
        zeros_decimal = ''

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
    width2_rel='14mm'
    ret = [
            f'\\makebox[{width1_rel}]{{\\hspace*{{\\fill}}${the_value}{the_error}$}}',
        ]

    if percentage:
        ret.append(f'\\makebox[{width2_rel}]{{\\hspace*{{\\fill}}{{\\relsize{{-1}}{relsigma:.1f}\\%}}}}')

    ret = ''.join(ret)
    # print(ret)
    # return ''.join(f'\\fbox{{{s}}}' for s in ret)
    return ret

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input', help='file to load')
    parser.add_argument('--nmo', choices=('NO', 'IO', 'auto'), default='auto', help='ordering')
    parser.add_argument('-o', '--output', help='file to write')
    parser.add_argument('-s', '--show', action='store_true', help='show')
    parser.add_argument('-e', '--exclude', nargs='+', default=(), help='types mask to exclude (tested with contains)')

    main(parser.parse_args())

