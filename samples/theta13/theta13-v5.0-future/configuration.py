version='5.0'
url='git.jinr.ru/nu/osc'
date='2021.11'
variable=r'$\sin^2 2\theta_{13}$'
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
		}

colors = {
    'kamland':         colors['reactor'],
    'reno':            colors['reactor'],
    'junoreactor':     colors['reactor'],
    'dayabay':         colors['reactor'],
    'doublechooz':     colors['reactor'],
    'dchooz':          colors['reactor'],
    'kamlandsksno':    colors['reacsolar'],
    'nova':            colors['acc'],
    't2k':             colors['acc'],
    'minos':           colors['acc'],
    'superkamiokande': colors['solar'],
    'superksno':       colors['solar'],
    'sno':             colors['solar'],
    'icecube':         colors['atm'],
    'nufit5.1':        colors['global'],
    'foreroetal.':     colors['global'],
    'dune':            colors['acc'],
    'capozzietal.':     colors['global']
	}

names = {
	'JUNO reactor': r'JUNO'
		}

titles = {}

def dayabay():
	colors['dayabay_nh'] = 'xkcd:blue'
	colors['dayabay_ngd'] = 'xkcd:blue'

preamble = r'\usepackage{xcolor}\usepackage{bbding}\let\Cross\undefined\usepackage{marvosym}\usepackage{relsize}'
