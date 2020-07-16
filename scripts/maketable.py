#!/usr/bin/env python

import yaml
from tabulate import tabulate
import numpy as np
from pylib.converters import convert

def main(args):
    data = collect(args.inputs)

    data = sorted(data, key=lambda x: x[5])
    data = map(filter, data)

    header = [ 'experiment', 'comment', 'value', 'left', 'right', 'span', 'tex', 'arxiv', 'conf' ]
    print(tabulate(data, header))

def filter(word):
    if isinstance(word, (tuple, list)):
        return map(filter, word)

    if isinstance(word, str) and ' ' in word:
        return f'{{{word}}}'

    return word

def collect(data):
    ret = []
    for entry in data:
        if not isinstance(entry, list):
            entry = [entry]

        for entry in entry:
            collect_entry(entry, ret)

    return ret

def merge_leftright(unc):
    left, right = unc['left'], unc['right']
    return 0.5*(left+right)

def get_uncertainty(val, unc):
    if isinstance(unc, float):
        return val-unc, val+unc
    elif isinstance(unc, (list, tuple)):
        left, right = unc
        return val-left, val+right
    elif not isinstance(unc, dict):
        raise Exception('Invalid uncertainty: '+str(unc))

    try:
        left, right = unc['left'], unc['right']
    except KeyError:
        pass
    else:
        return val-left, val+right

    try:
        left, right = unc['left'], unc['right']
    except KeyError:
        pass
    else:
        return val-left, val+right

    try:
        val_left, val_right = unc['interval']
    except KeyError:
        pass
    else:
        return val_left, val_right

    try:
        stat, syst = unc['stat'], unc['syst']
    except KeyError:
        pass
    else:
        if isinstance(stat, dict) and isinstance(syst, dict):
            stat, syst = merge_leftright(stat), merge_leftright(syst)
        if not isinstance(stat, float) or not isinstance(syst, float):
            raise Exception(f'Invalid stat/syst uncertainties: {stat!s}, {syst!s}')

        unc = (stat**2 + syst**2)**0.5
        return val-unc, val+unc

    print('Not supported uncertainty: '+str(unc))

def collect_result(var, entry):
    results = entry.get('result', {}).get(var, {})
    if not results:
        return

    if not isinstance(results, list):
        results = [results]

    for res in results:
        mode = res['mode']

        val = res['value']
        val_left, val_right = get_uncertainty(val, res['uncertainty'])
        val_left, val, val_right = convert(var, mode, val_left, val, val_right)
        unc_left = val - val_left
        unc_right = val_right - val

        span = val_right - val_left

        precision = res['precision']

        s_val   = f'{val:.{precision}f}'
        s_left  = f'{unc_left:.{precision}f}'
        s_right = f'{unc_right:.{precision}f}'

        target = [s_val, s_left, s_right, span]

        if s_left==s_right:
            target.append(f'${s_val}\\pm{s_left}$')
        else:
            target.append(f'${s_val}^{{+{s_right}}}_{{-{s_left}}}$')

        yield target

def collect_entry(entry, target):
    before = [entry['experiment']]
    if entry.get('type')=='reactor':
        before.append(entry['target'])
    else:
        before.append('')
    ref = entry.get('reference', {})
    after = [ref.get('arxiv', ''), ref.get('conf')]

    for res in collect_result('amplitude13', entry):
        target.append(before+res+after)

def load(filename):
    with open(filename, 'r') as f:
        return yaml.load(f, Loader=yaml.Loader)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('inputs', nargs='+', type=load, help='files to load')
    parser.add_argument('-o', '--output', help='file to write')

    main( parser.parse_args() )
