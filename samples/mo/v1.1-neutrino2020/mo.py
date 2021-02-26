#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle
import itertools as it
import yaml

reference =  'v1.1 2021.02: git.jinr.ru/nu/osc'

def main(args):

    #
    # RC params
    #
    plt.rc('text', usetex=True)
    plt.rcParams['grid.alpha'] = 0.1
    plt.rcParams['grid.linewidth'] = 2
    plt.rcParams.update({'font.size': 15})
    plt.rcParams.update({'legend.fontsize': 18})
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 8
    fig_size[1] = 4
    plt.rcParams["figure.figsize"] = fig_size

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    colors = {'minos_2020-07-neutrino2020' : 'xkcd:green', 'nova_2020-07-neutrino2020' : 'xkcd:green', 't2k_2020-07-neutrino2020' : 'xkcd:green', 'superk_2020-07-neutrino2020' : 'xkcd:azure', 'theor_forero_2020-06-pre-neutrino2020' : 'xkcd:steel grey', 'theor_nufit_2020-07-post-neutrino2020' : 'xkcd:steel grey'}

    #
    # Load
    #

    exps = []
    for exp in args.inputs:
        with open(exp, 'r') as f:
            file = yaml.load(f, Loader=yaml.Loader)
        name = file["experiment"]
        hie = file["result"]["hier"]["value"]
        proj = file["result"]["hier"]['proj']
        if isinstance(proj, dict):
            proj_max = proj["max"]
            proj_min = proj["min"]
        else:
            proj_max, proj_min = proj, proj
        this_exp = {'id': exp.rsplit('/',1)[-1].replace('.yaml',''), 'name' : name, 'hie' : hie,
                    'proj_min' : proj_min, 'proj_max' : proj_max}
        exps.append(this_exp)

    #
    # Figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Inverted ordering rejection', pad=10)
    ax.set_xlabel('Standard deviations')
    plt.subplots_adjust(left=0.24, right=0.83, top=0.9, bottom=0.15)
    ax.set_xlim(0,6.0)
    ax.set_ylim(0.5,6.5)
    plt.plot([5.0, 5.0], [0, 8.0], ls='dotted', color='grey', alpha=0.35, lw=1)

    text_itself = []
    hie_values = []
    hie_proj_min = []
    hie_proj_max = []
    order_id = []
    axis_text_1 = []
    axis_text_2 = []

    #
    # Iterate data
    #
    exps_sorted = sorted(exps, key=lambda k: k['hie'])

    styles, labels = [], []
    for count, exp in enumerate(exps_sorted):
        text_itself.append(exp['name'])
        hie_values.append(exp['hie'])
        hie_proj_min.append(exp['proj_min'])
        hie_proj_max.append(exp['proj_max'])
        order_id.append(exp['id'])
        axis_text_1.append('\\textbf{'+str(exp['hie'])+'}')
#        if exp['proj_max'] >0:
#            axis_text_2.append(str(exp['proj_max']))
#        else:
#            axis_text_2.append(' ')
        #eb=plt.errorbar(exp['proj'], count+1, yerr=0.4, ls='--', color = colors[exp['id']])
        #eb[-1][0].set_linestyle('--')
    proj_ids = np.array([1,2,3])
    barlist_proj = plt.barh(proj_ids+1,
                                 np.array(hie_proj_max)[proj_ids] - np.array(hie_proj_min)[proj_ids],
                            left=np.array(hie_proj_min)[proj_ids], alpha=0.3, height=0.95)
    for i,proj_i in zip(range(len(proj_ids)),proj_ids):
        barlist_proj[i].set_color(colors[order_id[proj_i]])
    plt.annotate(r"$\}$",fontsize=48, color='gray', ha='left', va='center',
                 xy=(6.05, 3.5), annotation_clip=False)
#            xy=(0.915, 0.485), xycoords='figure fraction')
    plt.annotate(r'1.5$-$3.5'+'\n'+r'$(\sqrt{\Delta \chi^2})$',fontsize=16, color='gray', ha='left', va='center',
                 xy=(6.45, 3.5), annotation_clip=False)
    plt.annotate(r'0.5$-$5.0',fontsize=16, color='gray', ha='left', va='center',
                 xy=(6.45, 2.0), annotation_clip=False)

    y_axis = np.arange(1, 7, 1)
    #plt.barh(y_axis, hie_values)  # seems to be not needed
    barlist=plt.barh(y_axis, hie_values)
    barlist[0].set_color(colors[order_id[0]])
    barlist[1].set_color(colors[order_id[1]])
    barlist[2].set_color(colors[order_id[2]])
    barlist[3].set_color(colors[order_id[3]])
    barlist[4].set_color(colors[order_id[4]])
    barlist[5].set_color(colors[order_id[5]])
    ax.set_yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5], minor=False)
    ax.set_yticks(y_axis)
    ax.set_yticklabels(text_itself, ha='left')
    ax.tick_params(axis='y', direction='out', labelleft=True, labelright=False, pad=120)

    double_y = ax.twinx()
    double_y.set_ylim(0.5,6.5)
    double_y.tick_params(axis='y', direction='in', labelleft=False, labelright=True, pad=-40)
    double_y.set_yticks(y_axis)
    double_y.set_yticklabels(axis_text_1, ha='left')

    triple_y =  ax.twinx()
    triple_y.tick_params(axis='y', direction='out')
    triple_y.set_ylim(0.5,6.5)
    triple_y.tick_params(axis='y', direction='out', labelleft=False, labelright=True, pad=8)
    triple_y.set_yticks(y_axis)
    triple_y.set_yticklabels(axis_text_2)
    for t in triple_y.get_yticklabels():
        t.set_alpha(0.6)

    # ax.xaxis.grid(True, which='minor')
    ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5], minor=True)
    ax.tick_params(top=True)

    ax.text(1.0, 0.5, reference, rotation=90, alpha=0.25, transform=fig.transFigure, ha='right', va='center', fontsize='x-small')

    outfilename='plots/mo_exp_plot.png'
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

