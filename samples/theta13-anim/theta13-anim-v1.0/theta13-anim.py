#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

plt.rc('text', usetex=True)
plt.rc('grid', alpha=0.1, linewidth=2)
plt.rc('font', size=15, family='serif')
# plt.rc('legend', fontsize=18)
plt.rc('axes', grid=True)
plt.rc('axes.grid', axis='x')
plt.rc('axes.spines', left=False, right=False)
plt.rc('xtick.minor', visible=True)
plt.rc('ytick', left=False, labelleft=False)

class Animator(object):
    def __init__(self, opts):
        self._opts = opts

        self.previous = []

        self.init_figure()
        self.run()
        self.finalize()

    def init_figure(self):
        self._fig = plt.figure(figsize=(6, 3))
        self._ax = plt.subplot(111, xlabel='', ylabel='', title='')
        plt.subplots_adjust(left=0.3)
        self._ax.set_xlim(0.0, 0.2)

    def run(self):
        size = self._opts.input.size
        self._ani=FuncAnimation(self._fig, self.update, frames=range(size))

    def update(self, frame, **kwargs):
        data = self._opts.input[::-1][frame]
        style, name, type, target, _, precision, value, left, right, span, _ = data

        for a in self.previous: a.remove()

        eb = self._ax.errorbar(value, 1, None, [[left], [right]])

        self.previous=[eb]
        return eb

    def finalize(self):
        plt.show()

dtype = [
          ('style', 'U20'), ('name', 'U20'), ('type', 'U20'),
          ('notes', 'U20'), ('ordering', 'U20'),
          ('precision', 'i'), ('value', 'f'),
          ('left', 'f'), ('right', 'f'),
          ('span', 'f'), ('arxiv', 'U50')
        ]

def rts(s):
    return s.rstrip().lstrip()
converters = {i: rts for i,s in enumerate(dtype) if s[1][0]=='U'}
print(converters)

def loader(fname):
    return np.loadtxt(fname, dtype=dtype, delimiter='\t',
                      converters=converters, skiprows=1, usecols=range(len(dtype)))

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('input', type=loader, help='input table')

    a = Animator(parser.parse_args())
