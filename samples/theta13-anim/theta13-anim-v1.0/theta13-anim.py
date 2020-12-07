#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import itertools as it
from scipy.interpolate import interp1d
from typing import NamedTuple, types

class Experiment(NamedTuple):
    name: str
    table: object
    value: types.FunctionType
    left:  types.FunctionType
    right: types.FunctionType

animdata = [ ('color', 'U10'),
             ('gmonth', 'i'), ('gmonth_p', 'i'),
             ('value_i', 'f'), ('left_i', 'f'), ('right_i', 'f'),
             ('value_p', 'f'), ('left_p', 'f'), ('right_p', 'f'),
             ('value_n', 'f'), ('left_n', 'f'), ('right_n', 'f'),
           ]

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
            substorage['value_p'] = value1
            substorage['left_p'] = left1
            substorage['right_p'] = right1
            substorage['value_n'] = value2
            substorage['left_n'] = left2
            substorage['right_n'] = right2

        interp_value = interp1d(amonth, datum['value'], kind='linear', bounds_error=False, fill_value=(0.0, value2))
        interp_left = interp1d(amonth, datum['left'], kind='linear', bounds_error=False, fill_value=(0.0, left2))
        interp_right = interp1d(amonth, datum['right'], kind='linear', bounds_error=False, fill_value=(0.0, right2))

        storage['value_i'] = interp_value(storage['gmonth'])
        storage['left_i'] = interp_left(storage['gmonth'])
        storage['right_i'] = interp_right(storage['gmonth'])

        exp = Experiment(name, storage, interp_value, interp_left, interp_right)
        self._data[name]=exp

        # print(storage)

    def init_figure(self):
        self._fig = plt.figure(figsize=(6, 3))
        self._ax = plt.subplot(111, xlabel='', ylabel='', title='')
        plt.subplots_adjust(left=0.3)

        names = list(self._data.keys())
        yticks = np.arange(1, len(names)+1)
        self._ax.set_yticks(yticks)
        self._ax.set_yticklabels(names, ha='left')

        self._ax.set_xlim(0.0, 0.2)
        self._ax.set_ylim(-0.5, len(self._data)+1)

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

        lst=[]
        for i, (name, exp) in enumerate(self._data.items()):
            data = exp.table[iframe]
            color=data['color']
            if not data['value_p']:
                continue

            value = exp.value(frame)
            left = exp.left(frame)
            right = exp.right(frame)
            eb = self._ax.errorbar(value, i, None, [[left], [right]],
                                   color=color, fmt='o')

            lst.append(eb)

        if self._moviewriter:
            self._moviewriter.grab_frame()

        self.previous = lst
        return lst

    def finalize(self):
        plt.show()

        if self._moviewriter:
            self._moviewriter.finish()
            print('Write output file:', self._opts.output)

plt.rc('text', usetex=True)
plt.rc('grid', alpha=0.1, linewidth=2)
plt.rc('font', size=15, family='serif')
# plt.rc('legend', fontsize=18)
plt.rc('axes', grid=True)
plt.rc('axes.grid', axis='x')
plt.rc('axes.spines', left=False, right=False)
plt.rc('xtick.minor', visible=True)
plt.rc('ytick', left=False, labelleft=True)
plt.rc('errorbar', capsize=2)

dtype = [
          ('style', 'U20'), ('date', 'U20'), ('name', 'U20'), ('type', 'U20'),
          ('notes', 'U20'), ('ordering', 'U20'),
          ('precision', 'i'), ('value', 'f'),
          ('left', 'f'), ('right', 'f'),
          ('span', 'f'), ('arxiv', 'U50')
        ]

def rts(s):
    return s.rstrip().lstrip()
converters = {i: rts for i,s in enumerate(dtype) if s[1][0]=='U'}

def loader(fname):
    return np.loadtxt(fname, dtype=dtype, delimiter='\t',
                      converters=converters, skiprows=1, usecols=range(len(dtype)))

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('inputs', nargs='+', type=loader, help='input table')
    parser.add_argument('-o', '--output', help='output file name')

    a = Animator(parser.parse_args())
