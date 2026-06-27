version='15'
url='git.jinr.ru/nu/osc'
date='2025.12'
variables= {
		"single": r'$\sin^2 \theta_{13}$',
		"double": r'$\sin^2 2\theta_{13}$'
}
lims = None
scale = 100.0

reference = f'v{version} {date}: {url}'

colors = {
		'reactor':   'xkcd:red',
		'reacsolar': 'xkcd:orange',
		'solar':     'xkcd:saffron',
		'atm':       'xkcd:azure',
		'acc':       'xkcd:green',
		'global':    'xkcd:steel gray',
                'special':     'xkcd:purple',
                'superkt2k':   'xkcd:dark cyan'
		}

colors = {
    'kamland':         colors['reactor'],
    'reno':            colors['reactor'],
    'junoreactor':     colors['reactor'],
    'dayabay':         colors['reactor'],
    'doublechooz':     colors['reactor'],
    'superchooz':      colors['reactor'],
    'dchooz':          colors['reactor'],
    'schooz':          colors['reactor'],
    'kamlandsksno':    colors['reacsolar'],
    'nova':            colors['acc'],
    'nova_1d_rc':      colors['acc'],
    't2k':             colors['acc'],
    'novat2k':         colors['special'],
    'superkt2k':       colors['superkt2k'],
    'minos':           colors['acc'],
    'superkamiokande': colors['solar'],
    'superksno':       colors['solar'],
    'sno':             colors['solar'],
    'icecube':         colors['atm'],
    'desalasetal.':    colors['global'],
    'nufit5.2':        colors['global'],
    'nufit6':        colors['global'],
    'nufit6.1':        colors['global'],
    'pdg2024':         colors['global'],
    'dune':            colors['acc'],
    'capozzietal.':    colors['global']
	}

names = {
	'JUNO reactor': r'JUNO',
        'NOvA 1D RC': r'NOvA',
	'Super-Kamiokande': r'SuperK',
		}

titles = {}

def dayabay():
	colors['dayabay_nh'] = 'xkcd:blue'
	colors['dayabay_ngd'] = 'xkcd:blue'

preamble = r'\usepackage{xcolor}\usepackage{bbding}\let\Cross\undefined\usepackage{marvosym}\usepackage{relsize}'
