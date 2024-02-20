#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle
import itertools as it
import yaml

titles = dict(
        NO = 'Normal Ordering',
        IO = 'Inverted Ordering'
        )
colors = dict(
        nova='xkcd:green',
        superkamiokande='xkcd:azure',
        t2k='xkcd:green',
        desalasetal='xkcd:steel grey',
        nufit52='xkcd:steel gray',
        novat2k='xkcd:purple',
        superkt2k='xkcd:dark cyan'
        )

def main(args):
    #
    # Arguments
    #
    if args.ordering=='auto':
        if 'NO' in args.output[0]:
            assert not 'IO' in args.output[0]
            args.ordering='NO'
        elif 'IO' in args.output[0]:
            args.ordering='IO'
        else:
            raise Exception('Unable to determine ordering for: '+args.output[0])
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
    plt.rcParams['text.latex.preamble']+=r'\usepackage{marvosym}\usepackage{relsize}'

    #
    # Load
    #
    dtype1 = np.dtype([('id', 'U20'), ('exp', 'U20'), ('type', 'U50'), ('value', 'f8'), ('left', 'f8'), ('right', 'f8')])
    result = np.loadtxt(args.input, dtype=dtype1, skiprows=1, usecols=(0, 1, 2, 6, 7, 8))
    result = np.sort(result, axis=- 1, kind=None, order=("type"))
    rev_arr = result[::-1]
    digits_leading_max = 1
    # print(result)

        #
    # Figure
    #
    singleheight = 0.3
    fracbottom = 2.3
    fractop    = 1.2
    fracax     = 1.
    nitems = len(result)
    figheight  = (nitems+fractop+fracbottom+fracax)*singleheight
    axtop      = 1.0-fractop*singleheight/figheight
    fig = plt.figure(figsize=(8,figheight))
    ax = fig.add_subplot(111)
    ax.minorticks_on()
    xtitle = r'$\delta_{\scriptscriptstyle\mathrm{CP}}, \pi$'
    ax.set_xlabel(xtitle)
    ax.set_ylim(1.0-fracax*0.5, nitems+fracax*0.5)
    ax.set_xlim(-1, 1)
    ax.set_title(titles[args.ordering])
    #if xlims:=cfg.lims[args.variable].get(ordering):
    #    ax.set_xlim(xlims)
    ax.tick_params(axis='x', which='both', top=True)
    ax.xaxis.grid(True)
    padleft = 90
    # namewidth = '40mm'
    namewidth = '37mm'
    plt.subplots_adjust(left=0.165, right=0.825, top=axtop, bottom=fracbottom*singleheight/figheight)

        #
    # Iterate data
    #
    exp_name = []
    latex_text = []
    for count, exp in enumerate(rev_arr):
        id, name, type, value, left, right = exp

        digits = 3
        digits_decimal_max = 3
        sigma = 0.5*(right+left)
        
        color = colors.get(id, 'black')
        
        if value<-1.0:
            value = 2+value
            
        if value>1.0:
            value = value - 2
        
            
        kwargs=dict()
        plt.errorbar(value, count+1, xerr=np.array([[left, right]]).T, color=colors[id], capsize = 2, **kwargs)
        plt.plot(value, count+1, 'o', markerfacecolor=colors[id], markeredgecolor=colors[id])
        if (value - abs(left)) < -1.0:
            plt.errorbar(value+2.0, count+1, xerr=np.array([[abs(left), 0]]).T, color=colors[id], capsize = 2, **kwargs)
        if (value + right) > 1.0:
            plt.errorbar(value-2.0, count+1, xerr=np.array([[0, (right)]]).T, color=colors[id], capsize = 2, **kwargs)

        name = name.replace('_', ' ')
        if name == 'Super-Kamiokande':
            name = name.replace('Super-Kamiokande', r'SuperK')

        font=r'\slshape{}'

        name = f'\\makebox[{namewidth}]{{{{{font}{name}}}}}'

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
    ax_right_right.tick_params(
        axis='y',
        which='both',
        direction='out',
        left=False,
        labelleft=False,
        right=False,
        labelright=True,
        pad=75
    )
    ax_right_right.set_yticks(yticks)
    ax_right_right.set_yticklabels(latex_text, ha='right')

    ax.text(1.0, 0.5, 'v1 2023.12: git.jinr.ru/nu/osc', rotation=90, alpha=0.3, transform=fig.transFigure, ha='right', va='center', fontsize='x-small')

    legend = r'\noindent'
    legend += r'{\slshape{}Preliminary}'
    ax.text(0.03, 0.05, legend, alpha=0.3, transform=fig.dpi_scale_trans, ha='left', va='bottom', fontsize='x-small')

    for out in  args.output:
        plt.savefig(out, dpi=300)
        print('Save output file:', out)


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
    #return extra
    #return f'{{\color{{red}}{extra}}}'
    return f'\phantom{{{extra}}}'

def format_latex(digits_decimal, value, left, right, digits_leading_max, digits_decimal_max):
    digits_leading = 1 #int(ceil_from_zero(np.log10(value)))

    zeros_leading = phantom_zeros(digits_leading, digits_leading_max)
    if value > 0 :
        zeros_leading = f'\phantom{"-"}'
    zeros_decimal = phantom_zeros(digits_decimal, digits_decimal_max)

    #print(f'{value=:.6f} {digits_decimal=} {digits_leading=} {digits_leading_max=} {digits_decimal_max=} {zeros_leading=} {zeros_decimal=}')

    span = right+left
    relsigma = abs(100*0.5*span/value)

    value = f'{value:.{digits_decimal}f}'
    left = f'{left:.{digits_decimal}f}'
    right = f'{right:.{digits_decimal}f}'

    the_value = f'{zeros_leading}{value}{zeros_decimal}'
        
    if left==right:
        the_error = f'{{\\scriptstyle\\pm{left}{zeros_decimal}}}'
    else:
        the_error = f'^{{+{right}{zeros_decimal}}}_{{-{left}{zeros_decimal}}}'

    width1_rel='25mm'
    width2_rel='15mm'
    ret = [
            f'\\makebox[{width1_rel}]{{\\hspace*{{\\fill}}${the_value}{the_error}$}}',
            #f'\\makebox[{width2_rel}]{{\\hspace*{{\\fill}}\\relsize{{-1}}{relsigma:.1f}\\%}}'
          ]

    # return ''.join(f'\\fbox{{{s}}}' for s in ret)
    return ''.join(ret)



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('input', help='file to load')
    parser.add_argument('--ordering', default='auto', choices=('auto', 'NO', 'IO'), help='ordering')
    parser.add_argument('-o', '--output', nargs='+', default=(), help='file to write')
    parser.add_argument('-s', '--show', action='store_true', help='file to write')

    main(parser.parse_args())

