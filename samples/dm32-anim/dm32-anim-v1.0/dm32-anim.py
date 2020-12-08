#!/usr/bin/env python

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import itertools as it
from scipy.interpolate import interp1d
from typing import NamedTuple, Dict, types

from style import *

class Animator(object):
    _start = (2011, 9)
    _end   = (2019, 1)
    _mps   = 4.0      # months per second
    _fps   = None     # for a file
    _interval  = None # for the animation
    _framestep = None # for the animation
    _xlim = (0.03, 0.22)
    def __init__(self, opts):
        self._opts = opts

        self._fps = self._mps
        self._interval=1000/self._fps
        frames_per_month = 1.0/self._mps
        self._framestep = 1.0
        print('FPS:', self._fps)
        print('MPS:', self._mps)
        print('Frames per month:', frames_per_month)
        print('Interval: {} ms'.format(self._interval))
        print('Frame step: {} months'.format(self._framestep))

        self.previous = []

        self.init_data()
        self.init_figure()
        self.run()
        self.finalize()

    def gmonth(self, year, month):
        return (year-self._start[0])*12 - self._start[1] + month + 1

    def yearmonth(self, gmonth):
        omonth = gmonth + self._start[1] - 1 - 1
        nyears = omonth//12
        month = (omonth)%12+1

        return self._start[0] + nyears, month

    def init_data(self):
        self._nmonths = self.gmonth(*self._end)
        print(f'N months: {self._nmonths}')
        self._data={}
        for datum in self._opts.inputs:
            self.init_datum(datum)

    def init_datum(self, datum):
        exp = None
        storage = None
        amonth = None
        ordering1=''
        value2, left2, right2 = None, None, None
        def savestorage(name):
            if storage is None:
                return
            lastline = storage[-1]
            value2, left2, right2=lastline['value2'], lastline['left2'], lastline['right2']
            kind = 'previous'
            interp_value = interp1d(amonth, datum['value'], kind=kind, bounds_error=False, fill_value=(0.0, value2))
            interp_left = interp1d(amonth, datum['left'], kind=kind, bounds_error=False, fill_value=(0.0, left2))
            interp_right = interp1d(amonth, datum['right'], kind=kind, bounds_error=False, fill_value=(0.0, right2))

            ordering=list(exp.measurement.keys())[-1]
            print(name, ordering)
            print(storage[:10])
            print(storage[-10:])
            exp.measurement[ordering]=Measurement(ordering, storage, interp_value, interp_left, interp_right)

        def newstorage(name, ordering):
            storage = np.zeros(self._nmonths, dtype=animdata)
            storage['gmonth']=np.arange(1, self._nmonths+1)

            if not name in self._data:
                exp = self._data[name] = Experiment(name, {})

            exp.measurement[ordering] = True

            amonth = np.zeros(len(datum), dtype='i')
            return exp, amonth, storage

        prev = None
        for i, (dline1, dline2) in enumerate(it.zip_longest(datum, datum[1:])):
            _, date1, name, _, _, ordering1, prec1, value1, left1, right1, _, _ = dline1
            if ordering1:
                name+=f' {ordering1}'
            year1, month1 = map(int, date1.split('.')[1:])
            gmonth1 = self.gmonth(year1, month1)

            if dline2 is not None:
                _, date2, name2, _, _, ordering2, prec2, value2, left2, right2, _, _ = dline2
                year2, month2 = map(int, date2.split('.')[1:])
                gmonth2 = self.gmonth(year2, month2)

            assert ordering1==ordering2

            if dline2 is None:
                gmonth2 = self._nmonths

            if not exp or not ordering1 in exp.measurement:
                savestorage(name)
                exp, amonth, storage = newstorage(name, ordering1)

            amonth[i]=gmonth1
            s=slice(gmonth1-1,gmonth2)
            substorage = storage[s]
            substorage['date'] = date1.split('.', 1)[-1]
            substorage['gmonth_p'] = gmonth1
            substorage['value'] = value1
            substorage['left'] = left1
            substorage['right'] = right1
            substorage['value2'] = value2
            substorage['left2'] = left2
            substorage['right2'] = right2
            substorage['precision'] = prec1

        savestorage(name)

        print(list(self._data.keys()))

    def init_figure(self):
        self._fig = plt.figure(figsize=(8, 2.5))
        self._ax = plt.subplot(111, xlabel=xlabel, ylabel='', title='')
        plt.subplots_adjust(left=0.22, right=0.82, bottom=0.25)

        self._yticks_left = ()
        for name in self._data.keys():
            name = '{{{style}{name}}}'.format(style=texstyles.get(name,''), name=name)
            # name = name.replace('NO', r'NO')
            name = name.replace('IO', r'\hspace{2.3mm}IO')
            self._yticks_left+=name,

        yticks = np.arange(len(self._yticks_left))
        self._ax.set_yticks(yticks)
        self._ax.set_yticklabels(self._yticks_left, ha='left')
        self._ax.tick_params(axis='y', length=0,
                             labelleft=True, labelright=False,
                             pad=110)

        self._axr = self._ax.twinx()
        self._yticks_right = ['']*len(self._yticks_left)
        self._axr.set_yticks(yticks)
        self._axr.set_yticklabels(self._yticks_right, ha='left')
        self._axr.tick_params(axis='y', length=0,
                              labelleft=False, labelright=True,
                              # pad=110
                              )

        xticks = np.arange(0.0, 0.23, 0.02)
        self._ax.set_xticks(xticks)
        self._ax.set_xticklabels(f'{x*100:.0f}' for x in xticks)
        self._ax.set_xlim(*self._xlim)
        self._ax.set_ylim(len(self._data)-0.5, -0.5)
        self._axr.set_ylim(len(self._data)-0.5, -0.5)

        self._moviewriters = []
        for ofile in self._opts.output:
            mw = animation.ImageMagickFileWriter(fps=self._fps)
            mw.setup(self._fig, ofile, dpi=150)
            self._moviewriters.append(mw)

        self._digitsmax=0

        self._ax.text(1.0, 0.5, reference, rotation=90, alpha=0.3, transform=self._fig.transFigure,
                      ha='right', va='center', fontsize='x-small')

    def run(self):
        repeat = not bool(self._moviewriters)

        size = self._opts.inputs[0].size
        self._ani=FuncAnimation(self._fig, self.update, init_func=self.init,
                                frames=np.arange(1, self._nmonths+1, self._framestep),
                                repeat=repeat,
                                interval=self._interval)

    def init(self, **kwargs):
        pass

    def update(self, frame, **kwargs):
        for a in self.previous: a.remove()

        iframe = int(np.floor(frame))-1
        year, month = self.yearmonth(iframe+1)
        self._ax.set_title('{}.{}'.format(year, month))

        digitsmax = max(next(iter(d.measurement.values())).table[iframe]['precision'] for d in self._data.values())
        updateall=self._digitsmax!=digitsmax
        self._digitsmax = digitsmax

        xmax, xmin = self._ax.get_xlim()
        lst=[]
        updatevalues=False
        for i, (name, exp) in enumerate(self._data.items()):
            meass = exp.measurement

            if len(meass)>1:
                offsets = np.linspace(-1.0, 1.0, len(meass),dtype='d')*0.2
                markers = { 'NO': '^', 'IO': 'v' }
            else:
                offsets = [0.0]
                markers = {}

            for j, (offset, (ordering, meas)) in enumerate(zip(offsets, meass.items())):
                data = meas.table[iframe]
                if not data['value']:
                    continue

                value = meas.value(frame)
                left = meas.left(frame)
                right = meas.right(frame)
                span = right+left

                # marker = markers.get(meas.type, span>0.015 and 'o' or '|')
                marker='|'
                style = styles.get(name, {})
                eb = self._ax.errorbar(value, i+offset, None, [[left], [right]],
                                       fmt=marker, **style)
                lst.append(eb)

                # xmin, xmax = min(value-left,xmin), max(value+right, xmax)

                if j==0 and (updateall or data['gmonth']==data['gmonth_p']):
                    prec = data['precision']
                    tex = format_latex(prec, value, left, right, digitsmax)
                    self._yticks_right[i] = tex
                    updatevalues=True

        if updatevalues:
            self._axr.set_yticklabels(self._yticks_right, ha='left')

        for mw in self._moviewriters:
            mw.grab_frame()

        self.previous = lst
        return lst

    def finalize(self):
        plt.show()

        for i, mw in enumerate(self._moviewriters):
            mw.finish()
            print('Write output file:', self._opts.output[i])

def format_latex(digits, value, left, right, digits_max, suffix=''):
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

    if suffix:
        ret += f' ({suffix})'

    return ret

class Measurement(NamedTuple):
    type: str
    table: object
    value: types.FunctionType
    left:  types.FunctionType
    right: types.FunctionType

class Experiment(NamedTuple):
    name: str
    measurement: Dict[str, Measurement]

animdata = [ ('date', 'U10'),
             ('gmonth', 'i'), ('gmonth_p', 'i'),
             ('value', 'f'), ('left', 'f'), ('right', 'f'),
             ('value2', 'f'), ('left2', 'f'), ('right2', 'f'),
             ('precision', 'i')
           ]

input_dtype = [
          ('style', 'U20'), ('date', 'U20'), ('name', 'U20'), ('type', 'U20'),
          ('notes', 'U20'), ('ordering', 'U20'),
          ('precision', 'i'), ('value', 'f'),
          ('left', 'f'), ('right', 'f'),
          ('span', 'f'), ('arxiv', 'U50')
        ]

def rts(s):
    return s.rstrip().lstrip()
converters = {i: rts for i,s in enumerate(input_dtype) if s[1][0]=='U'}

def loader(fname):
    return np.loadtxt(fname, dtype=input_dtype, delimiter='\t',
                      converters=converters, skiprows=1, usecols=range(len(input_dtype)))

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('inputs', nargs='+', type=loader, help='input table')
    parser.add_argument('-o', '--output', nargs='+', default=[], help='output file name')
    parser.add_argument('-s', '--show', action='store_true', help='show the animation')

    a = Animator(parser.parse_args())
