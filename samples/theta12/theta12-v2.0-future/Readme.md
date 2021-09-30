# $`\sin^2 \theta_{12}`$ measurements comparison, after Neutrino 2020

- Version: **${version_num}${beta}**
- Updates since v${version_prev}:
    * Add JUNO estimation for solar and reactor neutrinos
- [Plotting scripts](samples/theta12/theta12-v${version_num}-future)
- [Data table](theta12_v${version_dash}${beta}.dat)
- References:
    - [KamLAND+SNO+SuperK](data/kamland+sk+sno_2020-07-neutrino2020.yaml)
    - [SNO+SuperK](data/sk+sno_2020-07-neutrino2020.yaml)
    - [KamLAND](data/kamland_2020-07-neutrino2020.yaml)
    - [SNO](data/sno_2020-07-neutrino2020.yaml)
    - [NuFIT 5.0](data/theor_nufit_2020-07-post-neutrino2020.yaml)
    - [Forero et al.](data/theor_forero_2020-06-pre-neutrino2020.yaml)
    - JUNO estimation:
        * [JUNO Yellow Book](data/juno_future_2015-07-reactor.yaml)
        * [JUNO Solar ⁸B](data/juno_future_2020-06-solar.yaml)
- Cross checks by:
    * @ldkolupaeva
    * @maxfl
- Notes:
    * Forero et al. is pre-Neutrino fit
    * $`\tan^2 \theta_{12}`$ to $`\sin^2 \theta_{12}`$ conversion:
        + $`\sin^2 \theta_{12} = 1 - 1/(1+\tan^2 \theta_{12})`$.

##  Including global analyses and future experiments
![sin²θ₁₂](theta12_global_future_v${version_dash}${beta}.png)

## Including global analyses
![sin²θ₁₂](theta12_global_v${version_dash}${beta}.png)

## Experiments only
![sin²θ₁₂](theta12_v${version_dash}${beta}.png)


