#!/usr/bin/env python

unity = lambda val, **kwargs: val

def amplitude_single_double(single2, **kwrgs):
    return 4.0*single2*(1.0-single2)

def splitting_large_ee(dmee, context):
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    sinSqTheta12 = context['sinSqTheta12']
    cosSqTheta12 = 1.0 - sinSqTheta12
    dm32 = dmee - ordering * cosSqTheta12 * dmSq21
    return dm32
    
def splitting_large_avg(dmavg, context):
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    dm32 = dmavg - 0.5 * dmSq21
    return dm32

def splitting_large_31(dm31, context):
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    dm32 = dm31 - ordering * dmSq21
    return dm32

converters = dict(
        amplitude13=dict(single=amplitude_single_double, double=unity),
        amplitude23=dict(single=amplitude_single_double, double=unity),
        splitting_large={'32': unity, 'ee': splitting_large_ee, '31': splitting_large_31, 'avg' : splitting_large_avg}
        )

def convert(var, mode, *vals, **kwargs):
    try:
        fcn = converters[var][mode]
    except KeyError:
        raise Exception(f'Do not know how to convert {var} {mode}')

    def converter(val):
        return fcn(val, **kwargs)

    return map(converter, vals)

