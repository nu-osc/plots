#!/usr/bin/env python

unity = lambda val, **kwargs: val

def amplitude_single_double(single2, **kwrgs):
    return 4.0*single2*(1.0-single2)

def dm32_from_ee(dmee, context):
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    sinSqTheta12 = context['sinSqTheta12']
    cosSqTheta12 = 1.0 - sinSqTheta12
    dm32 = dmee - ordering * cosSqTheta12 * dmSq21
    return dm32

def dm32_from_avg(dmavg, context):
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    dm32 = dmavg - 0.5 * ordering * dmSq21
    return dm32

def dm32_from_31(dm31, context):
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    dm32 = dm31 - ordering * dmSq21
    return dm32

def dm32_from_32NO(dm32NO, context):
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    if ordering==1.0:
        return dm32NO

    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    dm32IO = dm32NO + 2.0*dmSq21
    return dm32IO

def dm32_from_32NO_31IO(dm32NO_31IO, context):
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    if ordering==1.0:
        return dm32NO_31IO

    return dm32_from_31(dm32NO_31IO, context)

def dm31_from_32(dm32, context):
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    dm31 = dm32 + ordering * dmSq21
    return dm31

converters = dict(
        amplitude13=dict(single=amplitude_single_double, double=unity),
        amplitude23=dict(single=amplitude_single_double, double=unity),
        dm32={
            '32': unity,
            '32NO': dm32_from_32NO,
            '32NO/31IO': dm32_from_32NO_31IO,
            'ee': dm32_from_ee,
            '31': dm32_from_31,
            'avg' : dm32_from_avg
        },
        dm31={
            '31': unity,
            # '32NO': dm32_from_32NO,
            # '32NO/31IO': dm32_from_32NO_31IO,
            # 'ee': dm32_from_ee,
            '32': dm31_from_32,
            # 'avg' : dm32_from_avg
        }
        )

def convert(var, mode, *vals, **kwargs):
    try:
        fcn = converters[var][mode]
    except KeyError:
        raise Exception(f'Do not know how to convert {var} {mode}')

    def converter(val):
        return fcn(val, **kwargs)

    return map(converter, vals)

