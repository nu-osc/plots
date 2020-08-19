#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle, Polygon
import itertools as it
import yaml

def main(args):

#
# RC params
#
    plt.rc('text', usetex=True)
    plt.rcParams['grid.alpha'] = 0.1
    plt.rcParams['grid.linewidth'] = 2
    plt.rcParams.update({'font.size': 24})
    plt.rcParams.update({'legend.fontsize': 18})
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 14
    fig_size[1] = 8
    plt.rcParams["figure.figsize"] = fig_size

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    colors = {'nova' : 'xkcd:bubblegum', 't2ksk' : 'xkcd:green teal', 'icupgr' : 'xkcd:clear blue', 'juno':'xkcd:fire engine red', 'pingu' : 'xkcd:vivid blue', 'orca' : 'xkcd:charcoal grey', 't2hk' : 'xkcd:green', 'dune':'xkcd:violet', 'ino' : 'xkcd:orange', 't2hkk' : 'xkcd:emerald green'}

    position = {'nova' : (2022.5, 3.5), 't2ksk' : (2020.5, 2.0), 'icupgr' : (2025.25, 1.5), 'juno' : (2023.5, 2.5), 'pingu' : (2031, 3.75), 'orca': (2027, 4.25), 't2hk' : (2034.5, 4.3), 'dune' : (2028.5, 8), 'ino' : (2035, 2.5), 't2hkk' : (2033.5, 8)}

    marker_offset = {'nova' : 0, 't2ksk' : 0, 'icupgr' : 0, 'juno' : 0, 'pingu' : 0.05, 'orca': 0, 't2hk' : 0.05, 'dune' : 0, 'ino' : 0.05, 't2hkk' : 0.05}
#
# Load
#
    exps = []
    for exp in args.inputs:
        with open(exp, 'r') as f:
            file = yaml.load(f, Loader=yaml.Loader)
        #print(file)
        points = file["sensitivity"]["mh"]["year"][0]
        name = file["experiment"]
        status = file["status"]
        start = file["starting_year"]
        low = []
        high = []
        for i in range(0, len(points)):
            min = file["sensitivity"]["mh"]["low"][0][i]
            max = file["sensitivity"]["mh"]["high"][0][i]
            year_v = file["sensitivity"]["mh"]["year"][0][i]
            year_ax=year_v+start
            low.append((year_ax, min))
            high.append((year_ax, max))
        this_exp = {'id': exp.rsplit('/',1)[-1].split('_',1)[0].replace('.yaml', ''), 'name' : name, 'start' : start, 'status' : status, 'low_values' : low, 'high_values' : high}
        exps.append(this_exp)

#
# Figure
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.06, right=0.95, top=0.9, bottom=0.2)
    plt.title('Future Neutrino mass ordering sensitivity', pad=20)
    ax.set_xlabel('Year')
    ax.set_ylabel('Median sensitivity, $\sigma$')
    ax.set_xlim(2020, 2040)
    ax.set_ylim(0, 10.2)
    plt.yticks([1.0, 3.0, 5.0, 7.0, 9.0])
    ax.set_yticks([2.0, 4.0, 6.0, 8.0, 10.0], minor=True)

    text_qual = dict(boxstyle='round', facecolor='white', alpha=0.3, edgecolor ='white')
    plt.plot([2020.0, 2040.0], [5.0, 5.0], ls='--', color='black', lw=1,  alpha=0.5)

    for count, exp in enumerate(exps):

        star = ''
        if exp['status'] == 'not clear':
            star = '$^\star$'
        revert_max = exp['high_values'][::-1]
        size = len(revert_max) - 1
        color=colors[exp['id']]
        name=exp['name']+star
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
        poly = Polygon(exp['low_values'] + revert_max, facecolor=color, edgecolor=color, alpha=alpha, lw=width, ls=lstyle)
        ax.add_patch(poly)
        if star != '':
            poly_dub = Polygon(exp['low_values'] + revert_max, facecolor=color, fill=False, edgecolor=color, alpha=0.5, lw=2, ls=lstyle)
            ax.add_patch(poly_dub)

        if exp['id'] != 'orca' and exp['id'] != 'icupgr' and exp['id'] != 'juno' and exp['id'] != 'pingu':
            ax.text(text_place_x, text_place_y, name, color=color, bbox=text_qual)
        ax.annotate('', xy=(start, 0), xycoords='data', xytext=(start, -1.5), textcoords='data', arrowprops=dict(facecolor=color, ec=color, width = 2, alpha=0.4), ha='center', size = 14, zorder=-10)
        marker_place_x = start+marker_offset[exp['id']]
        marker_place_y = sens_max_1year
        ax.plot(marker_place_x, marker_place_y, '>', markeredgecolor=color, markersize=8, markerfacecolor=color, alpha=0.8)
        plt.plot([marker_place_x, sens_year_start], [marker_place_y, marker_place_y], ls='dotted', color=color)
        plt.plot([marker_place_x, start], [marker_place_y, 0], ls='dotted', color=color)
        if exp['id'] == 't2hkk':
            plt.text(start-0.4, -2-0.37, name, size = 20, color=color, fontweight='bold')
        else:
            plt.text(start-0.4, -1.95-0.8*(start % 2), name, size = 20, color=color, fontweight='bold')


    plt.grid()
    x_axis = np.arange(2020, 2042, 2)
    ax.set_xticks(x_axis)
    ax.set_xticklabels(['\\textbf{2020}', '\\textbf{2022}', '\\textbf{2024}', '\\textbf{2026}', '\\textbf{2028}', '\\textbf{2030}', '\\textbf{2032}', '\\textbf{2034}', '\\textbf{2036}', '\\textbf{2038}', '\\textbf{2040}'])
    ax.tick_params(top=True, right=True)
    ax.yaxis.grid(True, which='minor')
    ax.xaxis.labelpad = 10
    ax.tick_params(axis='x', which='major', pad=15)

    labels = ax.get_xticklabels()
    for label in labels:
        label.set_bbox(dict(fc='white', ec='white', alpha=0.2))

    ax.text(0.97, 0.55, 'v1.0 2020.08: git.jinr.ru/nu/osc', rotation=90, color='xkcd:greyish', transform=fig.transFigure, fontsize=15)

    outfilename='plots/future_nmo_plot.pdf'
    if args.output:
        outfilename = args.output
    plt.savefig(outfilename, dpi=300)
    print('Write output file', outfilename)

    if args.show:
        plt.show()


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('inputs', nargs='+', help='files to load')
    parser.add_argument('-o', '--output', help='file to write')
    parser.add_argument('-s', '--show', action='store_true', help='show')

    main(parser.parse_args())

