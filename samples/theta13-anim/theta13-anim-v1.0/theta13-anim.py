#!/usr/bin/env python

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import itertools as it
from scipy.interpolate import interp1d
from typing import NamedTuple, types

from style import *

class Animator(object):
    _start = (2012, 1)
    _end   = (2019, 12)
    _fps   = 25
    _interval = None
    _step = None
    def __init__(self, opts):
        self._opts = opts

        self._interval=1000/self._fps
        self._framestep=self._interval/80
        print('Step', self._framestep)

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
        name = datum[0]['name']

        storage = np.zeros(self._nmonths, dtype=animdata)
        storage['gmonth']=np.arange(1, self._nmonths+1)

        storage['color']='red'

        amonth = np.zeros(len(datum), dtype='i')
        prev = None
        for i, (dline1, dline2) in enumerate(it.zip_longest(datum, datum[1:])):
            _, date1, name, _, _, _, prec1, value1, left1, right1, _, _ = dline1

            year1, month1 = map(int, date1.split('.')[1:])
            gmonth1 = self.gmonth(year1, month1)

            if dline2 is None:
                gmonth2 = self._nmonths
            else:
                _, date2, name, _, _, _, prec2, value2, left2, right2, _, _ = dline2
                year2, month2 = map(int, date2.split('.')[1:])
                gmonth2 = self.gmonth(year2, month2)

            amonth[i]=gmonth1

            s=slice(gmonth1-1,gmonth2)
            substorage = storage[s]
            substorage['gmonth_p'] = gmonth1
            substorage['value'] = value1
            substorage['left'] = left1
            substorage['right'] = right1
            substorage['precision'] = prec1

        interp_value = interp1d(amonth, datum['value'], kind='linear', bounds_error=False, fill_value=(0.0, value2))
        interp_left = interp1d(amonth, datum['left'], kind='linear', bounds_error=False, fill_value=(0.0, left2))
        interp_right = interp1d(amonth, datum['right'], kind='linear', bounds_error=False, fill_value=(0.0, right2))

        print(name)
        print(substorage)

        exp = Experiment(name, storage, interp_value, interp_left, interp_right)
        self._data[name]=exp

        # print(storage)

    def init_figure(self):
        self._fig = plt.figure(figsize=(7, 2.5))
        self._ax = plt.subplot(111, xlabel=xlabel, ylabel='', title='')
        plt.subplots_adjust(left=0.3, right=0.8, bottom=0.25)

        self._yticks_left = list('{{{style}{name}}}'.format(style=texstyles.get(name,''), name=name) for name in self._data.keys())
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

        self._ax.set_xlim(0.0, 0.2)
        self._ax.set_ylim(len(self._data)-0.5, -0.5)
        self._axr.set_ylim(len(self._data)-0.5, -0.5)

        if self._opts.output:
            self._moviewriter = animation.ImageMagickFileWriter(fps=self._fps)
            self._moviewriter.setup(self._fig, self._opts.output, dpi=150)
        else:
            self._moviewriter = None

    def run(self):
        repeat = not bool(self._moviewriter)

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

        xmax, xmin = self._ax.get_xlim()
        lst=[]
        updatevalues=False
        for i, (name, exp) in enumerate(self._data.items()):
            data = exp.table[iframe]
            color=data['color']
            if not data['value']:
                continue

            value = exp.value(frame)
            left = exp.left(frame)
            right = exp.right(frame)
            span = right+left
            marker = span>0.015 and 'o' or '|'
            style = styles.get(name, {})
            eb = self._ax.errorbar(value, i, None, [[left], [right]],
                                   fmt=marker, **style)
            lst.append(eb)

            # xmin, xmax = min(value-left,xmin), max(value+right, xmax)

            if data['gmonth']==data['gmonth_p']:
                prec = data['precision']
                tex = format_latex(prec, value, left, right, 4)
                self._yticks_right[i] = tex
                updatevalues=True

        if updatevalues:
            self._axr.set_yticklabels(self._yticks_right, ha='left')

        if self._moviewriter:
            self._moviewriter.grab_frame()

        self.previous = lst
        return lst

    def finalize(self):
        plt.show()

        if self._moviewriter:
            self._moviewriter.finish()
            print('Write output file:', self._opts.output)

def format_latex(digits, value, left, right, digits_max):
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

    return ret

class Experiment(NamedTuple):
    name: str
    table: object
    value: types.FunctionType
    left:  types.FunctionType
    right: types.FunctionType

animdata = [ ('color', 'U10'),
             ('gmonth', 'i'), ('gmonth_p', 'i'),
             ('value', 'f'), ('left', 'f'), ('right', 'f'),
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
    parser.add_argument('-o', '--output', help='output file name')

    a = Animator(parser.parse_args())
