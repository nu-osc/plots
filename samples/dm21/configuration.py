version = "12"
url = "github.com/nu-osc/plots"
date = "2026.06"
variable = r"$\Delta m^2_{21}$, $10^{-5}$ eV$^2$"
lims = {"left": 3.9}

reference = f"v{version} {date} {url}"

colors = {
    "junoreactor": "xkcd:red",
    "junoreactor_nh": "xkcd:red",
    "junoreactor_ih": "xkcd:red",
    "junosolar": "xkcd:saffron",
    "kamland": "xkcd:red",
    "solarkamland": "xkcd:orange",
    "nova": "xkcd:green",
    "t2k": "xkcd:green",
    "minos": "xkcd:green",
    "solarglobal": "xkcd:saffron",
    "sno": "xkcd:saffron",
    "snoreactor": "xkcd:red",
    "snoreactorconstraint": "xkcd:orange",
    "icecube": "xkcd:azure",
    "nufit5.2": "xkcd:steel grey",
    "nufit6": "xkcd:steel grey",
    "nufit6.1": "xkcd:steel grey",
    "pdg2024": "xkcd:steel grey",
    "desalasetal.": "xkcd:steel grey",
    "hyperkamiokande": "xkcd:saffron",
    "dune": "xkcd:saffron",
    "capozzietal.": "xkcd:steel grey",
}

names = {
    "Super-Kamiokande": r"SuperK\texttt{+}SNO",
    # 'JUNO solar':   r'JUNO {\relscale{0.75}\SunshineOpenCircled} \texttt{+} SNO(NC)',
    "JUNO solar": r"JUNO {\relscale{0.75}\SunshineOpenCircled}",
    "JUNO reactor": r"JUNO \Radioactivity{}",
    "SNO+ reactor": r"SNO\texttt{+} \Radioactivity{}",
    "SNO+ reactor + constraints": r"SNO\texttt{+} \Radioactivity{}, constrained",
    "Hyper-Kamiokande": r"HyperK\texttt{+}SNO\texttt{+}SK",
    "SuperK+SNO": r"SuperK\texttt{+}SNO",
    "KamLAND+SK+SNO": r"KamLAND\texttt{+}SK\texttt{+}SNO",
}

preamble = (
    r"\usepackage{bbding}\let\Cross\undefined\usepackage{marvosym}\usepackage{relsize}"
)
