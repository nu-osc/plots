version='5'
url='git.jinr.ru/nu/osc'
date='2022.06'
variable=r'$\Delta m^2_{21}$, $10^{-5}$ eV$^2$'
lims = { 'left': 3.9 }

reference = f'v{version} {date}: {url}'

colors = {
        'junoreactor':     'xkcd:red',
        'junoreactor_nh':  'xkcd:red',
        'junoreactor_ih':  'xkcd:red',
        'junosolar':       'xkcd:saffron',
        'kamland':         'xkcd:red',
        'kamlandsksno':    'xkcd:orange',
        'nova':            'xkcd:green',
        't2k':             'xkcd:green',
        'minos':           'xkcd:green',
        'superksno':       'xkcd:saffron',
        'sno':             'xkcd:saffron',
        'icecube':         'xkcd:azure',
        'nufit5.1':        'xkcd:steel grey',
        'foreroetal.':     'xkcd:steel grey',
        'hyperkamiokande': 'xkcd:saffron',
        'dune':            'xkcd:saffron',
        'capozzietal.':    'xkcd:steel grey'
    }

names = {
        'Super-Kamiokande': 'SuperK+SNO',
        # 'JUNO solar':   r'JUNO {\relscale{0.75}\SunshineOpenCircled} + SNO(NC)',
        'JUNO solar':   r'JUNO {\relscale{0.75}\SunshineOpenCircled}',
        'JUNO reactor': r'JUNO \Radioactivity{}',
        'Hyper-Kamiokande': 'HyperK+SNO+SK',
        }

preamble = r'\usepackage{bbding}\let\Cross\undefined\usepackage{marvosym}\usepackage{relsize}'
