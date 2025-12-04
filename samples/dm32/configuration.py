version='15'
url='git.jinr.ru/nu/osc'
date='2025.11'

axis_label={
	'dm31': r'$|\Delta m^2_{31}|$, $10^{-3}$ eV$^2$',
	'dm32': r'$|\Delta m^2_{32}|$, $10^{-3}$ eV$^2$'
	}
lims={
	'dm32': { 'NO': (1.75, 2.87), 'IO': (1.80, 2.98) },
	'dm31': { 'NO': (1.80, 2.95), 'IO': (1.70, 2.90) }
	}

reference = f'v{version} {date}: {url}'

colors = {
        'reactor':     'xkcd:red',
        'reacsolar':   'xkcd:orange',
        'solar':       'xkcd:saffron',
        'atm':         'xkcd:azure',
        'acc':         'xkcd:green',
        'global':      'xkcd:steel gray',
        'special':     'xkcd:purple'
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
    'nova_1d_rc':      colors['acc'],
    't2k':             colors['acc'],
    'novat2k':         colors['special'],
    'superkt2k':       colors['special'],
    'minos':           colors['acc'],
    'superkamiokande': colors['atm'],
    'superksno':       colors['solar'],
    'sno':             colors['solar'],
    'icecube':         colors['atm'],
    'nufit5.2':        colors['global'],
    'nufit6':        colors['global'],
    'pdg2024':         colors['global'],
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
	    'IceCube Upgrade': 'IceCube Up.',
        'NOvA 1D RC': 'NOvA',
        }

preamble = r'\usepackage{marvosym}\usepackage{relsize}'

def dayabay():
	colors['dayabay_nh'] = 'xkcd:blue'
	colors['dayabay_ngd'] = 'xkcd:blue'

titles = dict(
    NO='Normal mass ordering',
    IO='Inverted mass ordering',
    )
