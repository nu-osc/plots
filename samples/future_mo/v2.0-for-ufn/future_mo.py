#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle, Polygon
import itertools as it
import yaml
import matplotlib.transforms as transforms

reference =  'v2.0b 2021.09: git.jinr.ru/nu/osc'

def main(args):

    #
    # RC params
    #
    plt.rc('text', usetex=True)
    plt.rcParams['grid.alpha'] = 0.1
    plt.rcParams['grid.linewidth'] = 2
    plt.rcParams.update({'font.size': 24, 'font.family': 'serif'})
    plt.rcParams.update({'legend.fontsize': 18})
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 14
    fig_size[1] = 8
    plt.rcParams["figure.figsize"] = fig_size

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    
    
    names = {
        'IceCube Upgrade': 'IceCube',
        'T2HKK': 'HyperK-Korea',
        'JUNO reactor': r'JUNO',
        'Hyper-Kamiokande': 'HyperK',
        'ESSnuSB': r'ESS$\nu$SB',
        'INO': r'ICAL',
        }

    colors = {'nova' : 'xkcd:bubblegum', 't2k' : 'xkcd:green teal', 'icecube' : 'xkcd:clear blue', 'juno':'xkcd:fire engine red', 'pingu' : 'xkcd:vivid blue', 'orca' : 'xkcd:charcoal grey', 'hyperk' : 'xkcd:green', 'dune':'xkcd:violet', 'ino' : 'xkcd:orange', 'hyperkkorea' : 'xkcd:emerald green', 'ess' : 'xkcd:lilac'}

    position = {'nova' : (2022.5, 3.5), 't2k' : (2020.3, 2.0), 'icecube' : (2025.25, 1.5), 'juno' : (2025.5, 1.5), 'pingu' : (2031, 3.75), 'orca': (2027, 4.25), 'hyperk' : (2034.5, 4.3), 'dune' : (2028.5, 8), 'ino' : (2035, 2.5), 'hyperkkorea' : (2033, 8), 'ess' : (2038, 8)}

    marker_offset = {'nova' : 0, 't2k' : 0, 'icecube' : 0, 'juno' : 0, 'pingu' : 0.05, 'orca': 0, 'hyperk' : 0.05, 'dune' : 0, 'ino' : 0.1, 'hyperkkorea' : 0.05, 'ess' : 0}
    #
    # Load
    #
    exps = []
    for exp in args.inputs:
        with open(exp, 'r') as f:
            file = yaml.load(f, Loader=yaml.Loader)
        #print(file)
        points = file["result"]["mh"]["year"][0]
        name = file["experiment"]
        status = file["status"]
        start = file["starting_year"]
        low = []
        high = []
        for i in range(0, len(points)):
            min = file["result"]["mh"]["low"][0][i]
            max = file["result"]["mh"]["high"][0][i]
            year_v = file["result"]["mh"]["year"][0][i]
            year_ax=year_v+start
            low.append((year_ax, min))
            high.append((year_ax, max))
        this_exp = {'id': exp.rsplit('/',1)[-1].split('_',1)[0].replace('.yaml', ''), 'name' : name, 'start' : start, 'status' : status, 'low_values' : low, 'high_values' : high}
        exps.append(this_exp)

    #
    # Figure
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.06, right=0.96, top=0.9, bottom=0.2)
    plt.title('Future neutrino mass ordering sensitivity', pad=20)
    ax.set_xlabel('Year')
    ax.set_ylabel('Median sensitivity, $\sigma$')
    ax.set_xlim(2020, 2040)
    ax.set_ylim(0, 10.2)
    plt.yticks([1.0, 3.0, 5.0, 7.0, 9.0])
    ax.set_yticks([2.0, 4.0, 6.0, 8.0, 10.0], minor=True)

    text_qual = dict(boxstyle='round', facecolor='white', alpha=0.3, edgecolor ='white')
    text_qual_juno = dict(boxstyle='round, pad = 0.15', facecolor='white', alpha=0.2, edgecolor ='white')
    plt.plot([2020.0, 2040.0], [5.0, 5.0], ls='--', color='black', lw=1,  alpha=0.5)

    for count, exp in enumerate(exps):

        star = ''
        if exp['status'] == 'not clear':
            star = '$^\star$'
        revert_max = exp['high_values'][::-1]
        size = len(revert_max) - 1
        color=colors[exp['id']]
        name = names.get(exp['name'],exp['name'])+star
        text_place_x=position[exp['id']][0]
        text_place_y=position[exp['id']][1]
        start = exp['start']
        sens_year_start = exp['high_values'][0][0]
        sens_max_1year = exp['high_values'][0][1]

        alpha=0.4
        lstyle = '-'
        width=2
        if star != '':
            lstyle = '--'
            alpha = 0.1
            width=0
        if exp['id'] == 'juno':
            alpha=0.5
        poly = Polygon(exp['low_values'] + revert_max, facecolor=color, edgecolor='none', alpha=alpha, lw=width, ls=lstyle)
        ax.add_patch(poly)
        if star != '':
            poly_dub = Polygon(exp['low_values'] + revert_max, facecolor=color, fill=False, edgecolor=color, alpha=0.5, lw=2, ls=lstyle)
            ax.add_patch(poly_dub)

        if exp['id'] != 'orca' and exp['id'] != 'icecube' and exp['id'] != 'juno' and exp['id'] != 'pingu' and exp['id'] != 'ess':
            ax.text(text_place_x, text_place_y, name, color=color, bbox=text_qual)
        if exp['id'] == 'juno':
            ax.text(text_place_x, text_place_y,  name, color=color, bbox=text_qual_juno)
        marker_place_x = start+marker_offset[exp['id']]
        marker_place_y = sens_max_1year

        alpha = 0.5
        ax.plot(marker_place_x, marker_place_y, '>', markeredgecolor=color, markersize=8, markerfacecolor=color, alpha=alpha)
        plt.plot([marker_place_x, sens_year_start], [marker_place_y, marker_place_y], ls='dotted', color=color, alpha=alpha)
        if args.arrows:
            plt.plot([marker_place_x, start], [marker_place_y, 0], ls='dotted', color=color, alpha=alpha)

        oddoffset = 0.95
        fulloffset = 1.3
        isodd = (start % 2)
        arrowprops = dict(transform=ax.transData,
                          facecolor=color, ec=color, alpha=0.4,
                          zorder=-10,
                          width=0.05,
                          head_width=0.20,
                          overhang=0.2,
                          length_includes_head=True,
                          clip_on=False)

        textopts = dict(size = 20, color=color, fontweight='bold', ha='center')
        expid = exp['id']
        if 'hyperk' in expid:
            textopts1 = dict(textopts)
            if expid=='hyperk':
                textopts1['va'] = 'top'
            else:
                textopts1['va'] = 'bottom'
            arrowoffset = fulloffset+oddoffset*0.5
            plt.text(start, -fulloffset-oddoffset, name, **textopts1)
        else:
            arrowoffset = fulloffset+oddoffset*0.75*isodd
            textoffset = -fulloffset-oddoffset*isodd
            va = isodd and 'center' or 'top'
            if exp['id'] == 'ess':
                arrowoffset = fulloffset
                textoffset = -fulloffset
                va = 'top'
            plt.text(start, textoffset, name, va=va, **textopts)

        plt.arrow(start, -arrowoffset+0.12, 0.0, arrowoffset-0.12*2, **arrowprops)


    plt.grid()
    x_axis = np.arange(2020, 2042, 2)
    ax.set_xticks(x_axis)
    ax.set_xticklabels(['\\textbf{2020}', '\\textbf{2022}', '\\textbf{2024}', '\\textbf{2026}', '\\textbf{2028}', '\\textbf{2030}', '\\textbf{2032}', '\\textbf{2034}', '\\textbf{2036}', '\\textbf{2038}', '\\textbf{2040}'])
    ax.tick_params(top=True, right=True)
    ax.yaxis.grid(True, which='minor')
    ax.xaxis.labelpad = 10
    ax.yaxis.labelpad = 15
    ax.tick_params(axis='x', which='major', pad=15)

    labels = ax.get_xticklabels()
    for label in labels:
        label.set_bbox(dict(fc='white', ec='white', alpha=0.5, pad=0.2))

    ax.text(1.0, 0.5, reference, rotation=90, alpha=0.30, transform=fig.transFigure, ha='right', va='center', fontsize='x-small')

    plt.savefig(args.output, dpi=300)
    print('Write output file', args.output)

    if args.show:
        plt.show()


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('inputs', nargs='+', help='files to load')
    parser.add_argument('-o', '--output', help='file to write')
    parser.add_argument('-s', '--show', action='store_true', help='show')
    parser.add_argument('-a', '--arrows', action='store_true', help='show arrows')

    main(parser.parse_args())

