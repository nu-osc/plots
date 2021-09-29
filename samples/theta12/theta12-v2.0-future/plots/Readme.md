# $`\sin^2 \theta_{12}`$ measurements comparison, after Neutrino 2020

- Version: **2.0b**
- [Plotting scripts](samples/theta12/theta12-v2.0-future)
- [Data table](theta12_v2-0b.dat)
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
- Updates:
    * Add JUNO estimation for solar and reactor neutrinos
- Cross checks by:
    * @maxfl
    * @ldkolupaeva
- Notes:
    * Forero et al. is pre-Neutrino fit
    * $`\tan^2 \theta_{12}`$ to $`\sin^2 \theta_{12}`$ conversion:
        + $`\sin^2 \theta_{12} = 1 - 1/(1+\tan^2 \theta_{12})`$.

| Experiments only              | Including global                     | Including global and future                 |
|-------------------------------|--------------------------------------|---------------------------------------------|
| ![sin²θ₁₂](theta12_v2-0b.png) | ![sin²θ₁₂](theta12_global_v2-0b.png) | ![sin²θ₁₂](theta12_global_future_v2-0b.png) |

