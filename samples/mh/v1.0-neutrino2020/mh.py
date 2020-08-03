#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle
import itertools as it
import yaml

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
    colors = {'minos_2020-07-neutrino2020' : 'green', 'nova_2020-07-neutrino2020' : 'green', 't2k_2020-07-neutrino2020' : 'green', 'superk_2020-07-neutrino2020' : 'xkcd:azure', 'theor_forero_2020-06-pre-neutrino2020' : 'grey', 'theor_nufit_2020-07-post-neutrino2020' : 'grey'}

#
# Load
#

    filenames = ['minos_2020-07-neutrino2020', 'nova_2020-07-neutrino2020', 't2k_2020-07-neutrino2020', 'superk_2020-07-neutrino2020', 'theor_nufit_2020-07-post-neutrino2020',  'theor_forero_2020-06-pre-neutrino2020']
    exps = []
    for exp in filenames:
        with open('data/'+exp+'.yaml', 'r') as f:
            file = yaml.load(f)
        name = file["experiment"]
        hie = file["result"]["hier"]["value"]
        proj = file["result"]["hier"]["proj"]
        this_exp = {'id': exp, 'name' : name, 'hie' : hie, 'proj' : proj}
        exps.append(this_exp)

#
# Figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Another hierarchy rejection', pad=15)
    ax.set_xlabel('Standard deviations')
    plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.15)
    ax.set_xlim(0,7.0)
    ax.set_ylim(0.5,6.5)
    plt.plot([5.0, 5.0], [0, 8.0], ls='--', dashes=(5, 5), color='grey', alpha=0.35)
    
    text_itself = []
    hie_values = []
    hie_proj = []
    order_id = []
    axis_text_1 = []
    axis_text_2 = []
#
# Iterate data
#
    styles, labels = [], []
    for count, exp in enumerate(exps):
        text_itself.append(exp['name'])
        hie_values.append(exp['hie'])
        hie_proj.append(exp['proj'])
        order_id.append(exp['id'])
        axis_text_1.append('\\textbf{'+str(exp['hie'])+'}')
        if exp['proj'] >0:
            axis_text_2.append(str(exp['proj']))
        else:
            axis_text_2.append(' ')
        eb=plt.errorbar(exp['proj'], count+1, yerr=0.4, ls='--', color = colors[exp['id']])
        eb[-1][0].set_linestyle('--')
        
    y_axis = np.arange(1, 7, 1)
    plt.barh(y_axis, hie_values)
    barlist=plt.barh(y_axis, hie_values)
    barlist[0].set_color(colors[order_id[0]])
    barlist[1].set_color(colors[order_id[1]])
    barlist[2].set_color(colors[order_id[2]])
    barlist[3].set_color(colors[order_id[3]])
    barlist[4].set_color(colors[order_id[4]])
    barlist[5].set_color(colors[order_id[5]])
    ax.set_yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5], minor=True)
    ax.set_yticks(y_axis)
    ax.set_yticklabels(text_itself, ha='left')
    ax.tick_params(axis='y', direction='out', labelleft=True, labelright=False,  pad=120)
    
    double_y = ax.twinx()
    double_y.set_ylim(0.5,6.5)
    double_y.tick_params(axis='y', direction='in', labelleft=False, labelright=True, pad=-10)
    double_y.set_yticks(y_axis)
    double_y.set_yticklabels(axis_text_1, ha='right')
    
    triple_y =  ax.twinx()
    triple_y.tick_params(axis='y', direction='out')
    triple_y.set_ylim(0.5,6.5)
    triple_y.tick_params(axis='y', direction='out', labelleft=False, labelright=True, pad=10,  labelcolor='grey')
    triple_y.set_yticks(y_axis)
    triple_y.set_yticklabels(axis_text_2)
    
    ax.yaxis.grid(True, which='minor')
    ax.tick_params(top=True)
    ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], minor=True)
    
    outfilename='plots/mh_exp_plot.pdf'
    if args.output:
        outfilename = args.output
    plt.savefig(outfilename, dpi=300)
    plt.show()
    

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--output', help='file to write')

    main(parser.parse_args())

