#!/usr/bin/env python

import yaml
from tabulate import tabulate
import numpy as np

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
        if isinstance(entry, list):
            for entry in entry:
                collect_entry(entry, ret)
        else:
            collect_entry(entry, ret)

    return ret

def get_uncertainty(val, unc):
    if isinstance(unc, float):
        return val-unc, val+unc, unc, unc
    elif isinstance(unc, (list, tuple)):
        left, right = unc
        return val-left, val+right, left, right
    elif not isinstance(unc, dict):
        raise Exception('Invalid uncertainty: '+str(unc))

    try:
        left, right = unc['left'], unc['right']
    except KeyError:
        pass
    else:
        return val-left, val+right, left, right

    try:
        left, right = unc['left'], unc['right']
    except KeyError:
        pass
    else:
        return val-left, val+right, left, right

    try:
        val_left, var_right = unc['interval']
    except KeyError:
        pass
    else:
        left = val - val_left
        right = val_right - val
        return val_left, val_right, left, right

    try:
        stat, syst = unc['stat'], unc['syst']
    except KeyError:
        pass
    else:
        unc = (stat**2 + syst**2)**0.5
        return val-unc, val+unc, unc, unc

    print('Not supported uncertainty: '+str(unc))

def collect_result(var, entry, target):
    res = entry.get('result', {}).get(var, {})
    if not res:
        return False

    val = res['value']
    val_left, val_right, unc_left, unc_right = get_uncertainty(val, res['uncertainty'])
    span = val_right - val_left

    precision = res['precision']

    s_val   = f'{val:.{precision}f}'
    s_left  = f'{unc_left:.{precision}f}'
    s_right = f'{unc_right:.{precision}f}'

    target.append(s_val)
    target.append(s_left)
    target.append(s_right)
    target.append(span)

    if s_left==s_right:
        target.append(f'${s_val}\\pm{s_left}$')
    else:
        target.append(f'${s_val}^{{+{s_right}}}_{{-{s_left}}}$')

    return True

def collect_entry(entry, target):
    ret = [entry['experiment']]

    if entry.get('type')=='reactor':
        ret.append(entry['target'])
    else:
        ret.append('')

    if not collect_result('amplitude13', entry, ret):
        return

    ref = entry.get('reference', {})
    ret.append(ref.get('arxiv', ''))
    ret.append(ref.get('conf'))

    target.append(ret)

def load(filename):
    with open(filename, 'r') as f:
        return yaml.load(f, Loader=yaml.Loader)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('inputs', nargs='+', type=load, help='files to load')
    parser.add_argument('-o', '--output', help='file to write')

    main( parser.parse_args() )
