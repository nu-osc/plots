#!/usr/bin/env python

context = dict()

import yaml
from tabulate import tabulate
import numpy as np
from pylib.converters import convert

def main(args):
    global context
    if args.variable.startswith('theta'):
        args.variable = args.variable.replace('theta', 'amplitude')

    var = args.variable
    # if args.ordering=='auto':
        # if 'NO' in args.output:
            # assert not 'IO' in args.output
            # args.ordering='NO'
        # elif 'IO' in args.output:
            # args.ordering='IO'
        # else:
            # raise Exception('Unable to determine ordering')

    # context['ordering']=args.ordering

    data = collect(args.inputs, var=var)

    data = sorted(data, key=lambda item: item['span'])
    data = postprocess(data, var)
    data = list(map(filter_data, data))

    header = [ 'style', 'name', 'type', 'notes', 'measurement', 'dataset', 'ordering', 'precision', 'value', 'left', 'right', 'span', 'preliminary', 'arxiv', 'conf' ]
    data = select_columns(data, header)
    result = tabulate(data, header, tablefmt='plain')

    print(result)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
            print('Write output file:', args.output)

def postprocess(data, var):
    postprocessor = postprocessors.get(var)
    if not var or not postprocessor:
        return data

    return list(map(postprocessor, data))

def postprocess_amplitude13(entry):
    if entry['name']=='Double CHOOZ':
        entry['notes']=''

    slist = [ entry['name'].lower().replace(' ', '').replace('-', '').replace('+', '') ]
    #if entry['notes']:
    #    slist.append(entry['notes'].lower())
    entry['style']='_'.join(slist)
    return entry

def postprocess_splitting_large(entry):
    if entry['name']=='Double CHOOZ':
        entry['notes']=''

    slist = [ entry['name'].lower().replace(' ', '').replace('-', '').replace('+', '') ]
    if entry['notes']:
        slist.append(entry['notes'].lower())
    entry['style']='_'.join(slist)
    return entry

def postprocess_deltaCP(entry):
    name= entry['name'].lower()
    for c in " -+,'.":
        name=name.replace(c,'')
    slist = [name]
    if entry['notes']:
        slist.append(entry['notes'].lower())
    entry['style']='_'.join(slist)
    return entry

def postprocess_amplitude23(entry):
    slist = [ entry['name'].lower().replace(' ', '').replace('-', '').replace('+', '') ]
    if entry['notes']:
        slist.append(entry['notes'].lower())
    entry['style']='_'.join(slist)
    return entry

def postprocess_amplitude12(entry):
    slist = [ entry['name'].lower().replace(' ', '').replace('-', '').replace('+', '') ]
    if entry['notes']:
        slist.append(entry['notes'].lower())
    entry['style']='_'.join(slist)
    return entry

def postprocess_splitting_small(entry):
    slist = [ entry['name'].lower().replace(' ', '').replace('-', '').replace('+', '') ]
    if entry['notes']:
        slist.append(entry['notes'].lower())
    entry['style']='_'.join(slist)
    return entry

postprocessors=dict(
        amplitude12     = postprocess_amplitude12,
        amplitude13     = postprocess_amplitude13,
        splitting_large = postprocess_splitting_large,
        deltaCP         = postprocess_deltaCP,
        amplitude23     = postprocess_amplitude23,
        splitting_small = postprocess_splitting_small
        )

def select_columns(data, columns):
    return [list(datum[c] for c in columns) for datum in data]

def filter_data(entry):
    return dict(map(filter_entry, entry.items()))

def filter_entry(args):
    key, word = args

    if word is None:
        return key, '{}'

    if not isinstance(word, str):
        return key, word

    if ' ' in word:
        word = word.replace(' ', '_')
    elif not word:
        word='{}'

    return key, word

def collect(data, var):
    ret = []
    for entry in data:
        if not isinstance(entry, list):
            entry = [entry]

        for entry in entry:
            collect_experiment(entry, ret, var=var)

    return ret

def collect_experiment(entry, target, var):
    before = { 'name': entry['experiment'], 'type': entry.get('type', '') }

    if entry.get('type')=='reactor':
        before['notes'] = entry.get('target', '')
    else:
        before['notes'] = ''

    ref = entry.get('reference', {})
    preliminary = ref.get('preliminary', not ref.get('arxiv'))
    after = {
        'arxiv': ref.get('arxiv', ''),
        'conf': ref.get('conf'),
        'preliminary': int(preliminary)
    }

    for res in collect_result(var, entry):
        item = dict(before)
        item.update(res)
        item.update(after)
        target.append(item)

def collect_result(var, experiment):
    parameter = experiment.get('result', {}).get(var, {})
    if not parameter:
        return

    if 'results' in parameter:
        results = parameter['results']
    else:
        results = [parameter]

    for res in results:
        mode = res.get('mode', parameter.get('mode'))
        precision = res.get('precision', parameter['precision'])

        if 'ordering' in context:
            if 'ordering' in res:
                if context['ordering']!=res['ordering']:
                    continue
            else:
                res['ordering'] = context['ordering']

        val = res['value']
        val_left, val_right = get_uncertainty(val, res['uncertainty'])
        if mode:
            val_left, val, val_right = convert(var, mode, val_left, val, val_right)
        unc_left = val - val_left
        unc_right = val_right - val

        span = val_right - val_left

        s_val   = f'{val:.{precision}f}'
        s_left  = f'{unc_left:.{precision}f}'
        s_right = f'{unc_right:.{precision}f}'

        target = {'value': s_val, 'left': s_left, 'right': s_right, 'span': span}
        target['precision'] = precision

        target['ordering']=res.get('ordering')
        target['octant']=res.get('octant')
        target['measurement']=experiment.get('measurement')

        target['dataset']=experiment.get('dataset')
        if experiment.get('measurement') != 'estimation':
            target['dataset']=''

        yield target

def merge_leftright(unc):
    left, right = unc['left'], unc['right']
    return 0.5*(left+right)

def merge_statsyst(stat, syst, leftright):
    stat, syst = stat[leftright], syst[leftright]
    return (stat**2 + syst**2)**0.5

def get_uncertainty(val, unc):
    if isinstance(unc, float):
        return val-unc, val+unc
    elif isinstance(unc, (list, tuple)):
        left, right = unc
        return val-left, val+right
    elif not isinstance(unc, dict):
        raise Exception('Invalid uncertainty: '+str(unc))

    # Symmetric, relative, percent
    try:
        relsigma = unc['percent']*0.01
    except KeyError:
        pass
    else:
        return val*(1-relsigma), val*(1+relsigma)

    # Asymmetric, absolute
    try:
        left, right = unc['left'], unc['right']
    except KeyError:
        pass
    else:
        return val-left, val+right

    # Absolute, interval
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
            left = merge_statsyst(stat, syst, 'left')
            right = merge_statsyst(stat, syst, 'right')
            return val-left, val+right

        unc = (stat**2 + syst**2)**0.5
        return val-unc, val+unc

    print('Not supported uncertainty: '+str(unc))

def load(filename):
    with open(filename, 'r') as f:
        return yaml.load(f, Loader=yaml.Loader)

if __name__ == '__main__':
    from argparse import ArgumentParser
    variables = [ 'theta13', 'splitting_large', 'deltaCP', 'theta23', 'theta12', 'splitting_small' ]
    parser = ArgumentParser()
    parser.add_argument('inputs', nargs='+', type=load, help='files to load')
    parser.add_argument('-v', '--variable', choices=variables, required=True, help='variable to read')
    # parser.add_argument('--ordering', '--nmo', default='auto', choices=('NO', 'IO', 'auto'), help='ordering')
    parser.add_argument('-o', '--output', default='', help='file to write')

    main(parser.parse_args())
