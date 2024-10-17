version='13'
url='git.jinr.ru/nu/osc'
date='2024.06'

axis_label={
	'dm31': r'$|\Delta m^2_{31}|$, $10^{-3}$ eV$^2$',
	'dm32': r'$|\Delta m^2_{32}|$, $10^{-3}$ eV$^2$'
	}
lims={
	'dm32': { 'NO': (2.11, 2.83), 'IO': (2.03, 2.93) },
	'dm31': { 'NO': (2.18, 2.90), 'IO': (1.96, 2.86) }
	}

reference = f'v{version} {date}: {url}'

colors = {
        'reactor':     'xkcd:red',
        'reacsolar':   'xkcd:orange',
        'solar':       'xkcd:saffron',
        'atm':         'xkcd:azure',
        'acc':         'xkcd:green',
        'global':      'xkcd:steel gray',
        }

colors = {
    'kamland':         colors['reactor'],
    'reno':            colors['reactor'],
    'dayabay':         colors['reactor'],
    'doublechooz':     colors['reactor'],
    'superchooz':      colors['reactor'],
    'dchooz':          colors['reactor'],
    'kamlandsksno':    colors['reacsolar'],
    'nova':            colors['acc'],
    't2k':             colors['acc'],
    'minos':           colors['acc'],
    'superkamiokande': colors['atm'],
    'superksno':       colors['solar'],
    'sno':             colors['solar'],
    'icecube':         colors['atm'],
    'nufit5.2':        colors['global'],
    'pdg2023':         colors['global'],
    'desalasetal.':    colors['global'],
    'junoreactor':     colors['reactor'],
    'junoreactor_nh':  colors['reactor'],
    'junoreactor_ih':  colors['reactor'],
    'dune':            colors['acc'],
    'orca':            colors['atm'],
    'hyperkamiokande': colors['acc'],
    'ino':             colors['atm'],
    'icecubeupgrade':  colors['atm'],
    'essnusb':         colors['acc'],
    'capozzietal.':    colors['global']
	}

names = {
        'Super-Kamiokande': 'SuperK',
        'JUNO reactor': r'JUNO',
        'Hyper-Kamiokande': 'HyperK',
        'ESSnuSB': r'ESS$\nu$SB',
	'IceCube Upgrade': 'IceCube Up.'
        }

preamble = r'\usepackage{marvosym}\usepackage{relsize}'

def dayabay():
	colors['dayabay_nh'] = 'xkcd:blue'
	colors['dayabay_ngd'] = 'xkcd:blue'

titles = dict(
    NO='Normal mass ordering',
    IO='Inverted mass ordering',
    )
