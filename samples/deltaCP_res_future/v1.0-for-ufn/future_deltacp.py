#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from matplotlib.patches import Arc, Rectangle, Polygon
import itertools as it
import yaml
import matplotlib.transforms as transforms
from scipy.interpolate import interp1d, pchip_interpolate
from matplotlib import text as mtext
from matplotlib.ticker import MultipleLocator
import math

reference =  'v1.0b 2021.09: git.jinr.ru/nu/osc'

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
    fig_size[0] = 8
    fig_size[1] = 8
    plt.rcParams["figure.figsize"] = fig_size

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    
    
    names = {
        'Hyper-Kamiokande': 'HyperK'
        }

    colors = {'hyperk' : 'xkcd:green', 'dune':'xkcd:violet'}

    position = {'hyperk' : (2033, 15), 'dune' : (2029, 45)}

    #
    # Load
    #
    exps = []
    for exp in args.inputs:
        with open(exp, 'r') as f:
            file = yaml.load(f, Loader=yaml.Loader)
        points = file["result"]["dcp_res"]["year"][0]
        name = file["experiment"]
        status = file["status"]
        start = file["starting_year"]
        low_0 = []
        high_0 = []
        low_3_2 = []
        high_3_2 = []
        line_0 = []
        line_3_2 = []
        years = []
        for i in range(0, len(points)):
            year_v = file["result"]["dcp_res"]["year"][0][i]
            line_v_0 = file["result"]["dcp_res"]["line_0"][0][i]
            line_v_3_2 = file["result"]["dcp_res"]["line_3_2"][0][i]
            year_ax=year_v+start
            line_0.append(line_v_0)
            line_3_2.append(line_v_3_2)
            years.append(year_ax)
            if file["result"]["dcp_res"]["low_0"]:
                min_0 = file["result"]["dcp_res"]["low_0"][0][i]
                low_0.append(min_0)
                min_3_2 = file["result"]["dcp_res"]["low_3_2"][0][i]
                low_3_2.append(min_3_2)
            if file["result"]["dcp_res"]["high_0"]:
                max_0 = file["result"]["dcp_res"]["high_0"][0][i]
                high_0.append(max_0)
                max_3_2 = file["result"]["dcp_res"]["high_3_2"][0][i]
                high_3_2.append(max_3_2)
        this_exp = {'id': exp.rsplit('/',1)[-1].split('_',1)[0].replace('.yaml', ''), 'name' : name, 'start' : start, 'status' : status, 'low_values_0' : low_0, 'high_values_0' : high_0, 'line_0' : line_0, 'low_values_3_2' : low_3_2, 'high_values_3_2' : high_3_2, 'line_3_2' : line_3_2, 'years' : years}
        exps.append(this_exp)

    #
    # Figure
    fig, ax = plt.subplots()
    plt.minorticks_on()
    plt.subplots_adjust(left=0.11, right=0.96, top=0.95, bottom=0.13)
    plt.title('', pad=20)
    ax.set_xlabel('Year')
    ax.set_ylabel('$\delta_{\\rm CP}$ resolution, degrees')
    ax.set_xlim(2025, 2040)
    ax.set_ylim(0, 50)
    plt.yticks([10, 20, 30, 40, 50])

    text_qual = dict(boxstyle='round', facecolor='white', alpha=0.3, edgecolor ='white')

    leg_styles = []
    leg_text = []
    for count, exp in enumerate(exps):

        star = ''
        if exp['status'] == 'not clear':
            star = '$^\star$'
        color=colors[exp['id']]
        name = names.get(exp['name'],exp['name'])+star
        text_place_x=position[exp['id']][0]
        text_place_y=position[exp['id']][1]
        start = exp['start']

        #smoothing
        orig_len = len(exp['years'])
        new_num = np.linspace(exp['years'][0], exp['years'][-1], 1 * orig_len)
        years_sm = pchip_interpolate(np.array(exp['years']), exp['years'], new_num)
        line_sm_0 = pchip_interpolate(np.array(exp['years']), exp['line_0'], new_num)
        line_sm_3_2 = pchip_interpolate(np.array(exp['years']), exp['line_3_2'], new_num)
        alpha=0.4
        width=2
        if exp['low_values_0']:
            low_sm_0 = pchip_interpolate(np.array(exp['years']), exp['low_values_0'], new_num)
            high_sm_0 = pchip_interpolate(np.array(exp['years']), exp['high_values_0'], new_num)
            poly_0 = Polygon(list(zip(years_sm.tolist()+years_sm[::-1].tolist(), low_sm_0.tolist()+high_sm_0[::-1].tolist())), facecolor=color, edgecolor=color, alpha=alpha, lw=width, ls='-')
            ax.add_patch(poly_0)
            leg_styles.append(poly_0)
            leg_text.append("HyperK syst. cases")
            low_sm_3_2 = pchip_interpolate(np.array(exp['years']), exp['low_values_3_2'], new_num)
            high_sm_3_2 = pchip_interpolate(np.array(exp['years']), exp['high_values_3_2'], new_num)
            poly_3_2 = Polygon(list(zip(years_sm.tolist()+years_sm[::-1].tolist(), low_sm_3_2.tolist()+high_sm_3_2[::-1].tolist())), facecolor=color, edgecolor=color, alpha=alpha, lw=width, ls='--')
            ax.add_patch(poly_3_2)

        ax.plot(years_sm, line_sm_0, color=color, linewidth=2, ls='-')
        ax.plot(years_sm, line_sm_3_2, color=color, linewidth=2, ls='--')

        ax.text(text_place_x, text_place_y, name, color=color)

        alpha = 0.5
        if args.arrows:
            plt.plot([marker_place_x, start], [marker_place_y, 0], ls='dotted', color=color, alpha=alpha)
        
        
        marker_place_x = start
        marker_place_y_0 = exp['line_0'][0]
        marker_place_y_3_2 = exp['line_3_2'][0]
        if exp['id']!='dune':
            ax.plot(marker_place_x, marker_place_y_0, '>', markeredgecolor=color, markersize=8, markerfacecolor=color, alpha=alpha)
            plt.plot([marker_place_x, exp['years'][0]], [marker_place_y_0, marker_place_y_0], ls='dotted', color=color, alpha=alpha)
            
        ax.plot(marker_place_x, marker_place_y_3_2, '>', markeredgecolor=color, markersize=8, markerfacecolor=color, alpha=alpha)
        plt.plot([marker_place_x, exp['years'][0]], [marker_place_y_3_2, marker_place_y_3_2], ls='dotted', color=color, alpha=alpha)
        
        kwargs = dict(color='xkcd:slate grey', fontsize=19)
        if exp['id']=='hyperk':
            text = CurvedText( x = years_sm[1:-1], y = line_sm_0[1:-1]-0.5, text='stat. only', va = 'top', axes = ax, **kwargs)
            text2 = CurvedText( x = years_sm[1:-1], y = line_sm_3_2[1:-1]-0.5, text='stat. only', va = 'top', axes = ax, **kwargs)


    plt.grid()
    x_axis = np.arange(2025, 2040, 2)
    ax.yaxis.set_minor_locator(MultipleLocator(5))
    ax.set_xticks(x_axis)
    ax.tick_params(top=True, right=True)
    ax.yaxis.grid(True, which='minor')
    ax.xaxis.grid(True, which='minor')
    ax.set_xticks([2026, 2028, 2030, 2032, 2034, 2036, 2038, 2040], minor=True)
    ax.xaxis.labelpad = 10
    ax.yaxis.labelpad = 7
    ax.tick_params(axis='x', which='major', pad=15)
    
    
    line_0 = plt.Line2D((0,1),(0,0), color='k')
    line_3_2 = plt.Line2D((0,1),(0,0), color='k', ls='--')
    fig.legend(leg_styles + [line_0, line_3_2], leg_text + ['$\delta_{\\rm CP}$ = 0', '$\delta_{\\rm CP} = 3\pi/2$'], loc='upper right', bbox_to_anchor=(0.93, 0.92))

    labels = ax.get_xticklabels()

    ax.text(1.0, 0.5, reference, rotation=90, alpha=0.30, transform=fig.transFigure, ha='right', va='center', fontsize='x-small')

    plt.savefig(args.output, dpi=300)
    print('Write output file', args.output)

    if args.show:
        plt.show()



class CurvedText(mtext.Text):
    """
    A text object that follows an arbitrary curve.
    """
    def __init__(self, x, y, text, axes, **kwargs):
        super(CurvedText, self).__init__(x[0],y[0],' ', **kwargs)

        axes.add_artist(self)

        ##saving the curve:
        self.__x = x
        self.__y = y
        self.__zorder = self.get_zorder()

        ##creating the text objects
        self.__Characters = []
        for c in text:
            if c == ' ':
                ##make this an invisible 'a':
                t = mtext.Text(0,0,'a')
                t.set_alpha(0.0)
            else:
                t = mtext.Text(0,0,c, **kwargs)

            #resetting unnecessary arguments
            t.set_ha('center')
            t.set_rotation(0)
            t.set_zorder(self.__zorder +1)

            self.__Characters.append((c,t))
            axes.add_artist(t)


    ##overloading some member functions, to assure correct functionality
    ##on update
    def set_zorder(self, zorder):
        super(CurvedText, self).set_zorder(zorder)
        self.__zorder = self.get_zorder()
        for c,t in self.__Characters:
            t.set_zorder(self.__zorder+1)

    def draw(self, renderer, *args, **kwargs):
        """
        Overload of the Text.draw() function. Do not do
        do any drawing, but update the positions and rotation
        angles of self.__Characters.
        """
        self.update_positions(renderer)

    def update_positions(self,renderer):
        """
        Update positions and rotations of the individual text elements.
        """

        #preparations

        ##determining the aspect ratio:
        ##from https://stackoverflow.com/a/42014041/2454357

        ##data limits
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()
        ## Axis size on figure
        figW, figH = self.axes.get_figure().get_size_inches()
        ## Ratio of display units
        _, _, w, h = self.axes.get_position().bounds
        ##final aspect ratio
        aspect = ((figW * w)/(figH * h))*(ylim[1]-ylim[0])/(xlim[1]-xlim[0])

        #points of the curve in figure coordinates:
        x_fig,y_fig = (
            np.array(l) for l in zip(*self.axes.transData.transform([
            (i,j) for i,j in zip(self.__x,self.__y)
            ]))
        )

        #point distances in figure coordinates
        x_fig_dist = (x_fig[1:]-x_fig[:-1])
        y_fig_dist = (y_fig[1:]-y_fig[:-1])
        r_fig_dist = np.sqrt(x_fig_dist**2+y_fig_dist**2)

        #arc length in figure coordinates
        l_fig = np.insert(np.cumsum(r_fig_dist),0,0)

        #angles in figure coordinates
        rads = np.arctan2((y_fig[1:] - y_fig[:-1]),(x_fig[1:] - x_fig[:-1]))
        degs = np.rad2deg(rads)


        rel_pos = 10
        for c,t in self.__Characters:
            #finding the width of c:
            t.set_rotation(0)
            t.set_va('center')
            bbox1  = t.get_window_extent(renderer=renderer)
            w = bbox1.width
            h = bbox1.height

            #ignore all letters that don't fit:
            if rel_pos+w/2 > l_fig[-1]:
                t.set_alpha(0.0)
                rel_pos += w
                continue

            elif c != ' ':
                t.set_alpha(1.0)

            #finding the two data points between which the horizontal
            #center point of the character will be situated
            #left and right indices:
            il = np.where(rel_pos+w/2 >= l_fig)[0][-1]
            ir = np.where(rel_pos+w/2 <= l_fig)[0][0]

            #if we exactly hit a data point:
            if ir == il:
                ir += 1

            #how much of the letter width was needed to find il:
            used = l_fig[il]-rel_pos
            rel_pos = l_fig[il]

            #relative distance between il and ir where the center
            #of the character will be
            fraction = (w/2-used)/r_fig_dist[il]

            ##setting the character position in data coordinates:
            ##interpolate between the two points:
            x = self.__x[il]+fraction*(self.__x[ir]-self.__x[il])
            y = self.__y[il]+fraction*(self.__y[ir]-self.__y[il])

            #getting the offset when setting correct vertical alignment
            #in data coordinates
            t.set_va(self.get_va())
            bbox2  = t.get_window_extent(renderer=renderer)

            bbox1d = self.axes.transData.inverted().transform(bbox1)
            bbox2d = self.axes.transData.inverted().transform(bbox2)
            dr = np.array(bbox2d[0]-bbox1d[0])

            #the rotation/stretch matrix
            rad = rads[il]
            rot_mat = np.array([
                [math.cos(rad), math.sin(rad)*aspect],
                [-math.sin(rad)/aspect, math.cos(rad)]
            ])

            ##computing the offset vector of the rotated character
            drp = np.dot(dr,rot_mat)

            #setting final position and rotation:
            t.set_position(np.array([x,y])+drp)
            t.set_rotation(degs[il])

            t.set_va('center')
            t.set_ha('center')

            #updating rel_pos to right edge of character
            rel_pos += w-used





if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('inputs', nargs='+', help='files to load')
    parser.add_argument('-o', '--output', help='file to write')
    parser.add_argument('-s', '--show', action='store_true', help='show')
    parser.add_argument('-a', '--arrows', action='store_true', help='show arrows')

    main(parser.parse_args())

