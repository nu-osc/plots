version='6'
url='git.jinr.ru/nu/osc'
date='2024.10'
variable=r'$\sin^2 \theta_{12}$'
lims = (2.65, 3.55)
scale = 10.0

reference = f'v{version} {date}: {url}'

colors = {
        'junoreactor':     'xkcd:red',
        'junoreactor_ih':  'xkcd:red',
        'junoreactor_nh':  'xkcd:red',
        'junosolar':       'xkcd:saffron',
        'kamland':         'xkcd:red',
        'kamlandsksno':    'xkcd:orange',
        'nova':            'xkcd:green',
        't2k':             'xkcd:green',
        'minos':           'xkcd:green',
        'superksno':       'xkcd:saffron',
        'sno':             'xkcd:saffron',
        'icecube':         'xkcd:azure',
        'nufit6':          'xkcd:steel grey',
        'pdg2023':         'xkcd:steel grey',
        'desalasetal.':    'xkcd:steel grey',
        'hyperkamiokande': 'xkcd:saffron',
        'dune':            'xkcd:saffron',
        'capozzietal.':    'xkcd:steel grey'
    }

names = {
        'Super-Kamiokande': r'SuperK\texttt{+}SNO',
        # 'JUNO solar':   r'JUNO {\relscale{0.75}\SunshineOpenCircled} \texttt{+} SNO(NC)',
        'JUNO solar':   r'JUNO {\relscale{0.75}\SunshineOpenCircled}',
        'JUNO reactor': r'JUNO \Radioactivity{}',
        'SNO+ reactor': r'SNO\texttt{+} \Radioactivity{}',
        'Hyper-Kamiokande': r'HyperK\texttt{+}SNO\texttt{+}SK',
        "SuperK+SNO": r"SuperK\texttt{+}SNO",
        "KamLAND+SK+SNO": r"KamLAND\texttt{+}SK\texttt{+}SNO"
        }

preamble = r'\usepackage{bbding}\let\Cross\undefined\usepackage{marvosym}\usepackage{relsize}'
