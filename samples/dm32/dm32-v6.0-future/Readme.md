# $`|\Delta m^2_{32}|`$ measurements comparison

- Version: **${version_num}${beta}**
- Updates since v${version_prev}:
    * Add future sensitivities
- [Plotting scripts](samples/dm32/dm32-v${version_num}-future)
- Data tables:
    * [NO table](dm32_NO_v${version_dash}${beta}.dat)
    * [IO table](dm32_IO_v${version_dash}${beta}.dat)
- Conversions:
    * Effective mass splitting $`|\Delta m^2_\mathrm{ee}|`$ conversion (RENO):
        + $`|\Delta m^2_{32}| = |\Delta m^2_\mathrm{ee}| - \alpha \cos^2\theta_{12} \Delta m^2_{21}`$.
    * $`|\Delta m^2_\mathrm{31}|`$ to $`|\Delta m^2_\mathrm{32}|`$ conversion:
        + $`|\Delta m^2_{32}| = |\Delta m^2_\mathrm{31}| - \alpha |\Delta m^2_\mathrm{21}| `$.
    * $`\alpha`$ is +1/-1 for NO/IO.
    * PDG 2020 values:
        + $`\sin^2\theta_{12} = 0.307`$
        + $`\Delta m^2_{21} = 7.53\cdot10^{-5}\text{ eV}^2`$
    * Asymmetric syst/stat errors conversion: quadratically sum left and right part of each (stat/syst) contribution independently
- Cross checks by:
    * @ldkolupaeva
    * Bedrich Roskovec
    * @maxfl
- Notes:
    * Forero et al. is pre-Neutrino fit

## Latest results

### Including global analyses and future experiments

![\|Δm²₃₂\| NO](dm32_NO_global_future_v${version_dash}${beta}.png)

![\|Δm²₃₂\| IO](dm32_IO_global_future_v${version_dash}${beta}.png)

### Including global analyses

![\|Δm²₃₂\| NO](dm32_NO_global_v${version_dash}${beta}.png)

![\|Δm²₃₂\| IO](dm32_IO_global_v${version_dash}${beta}.png)

### Experiments only

![\|Δm²₃₂\| NO](dm32_NO_v${version_dash}${beta}.png)

![\|Δm²₃₂\| IO](dm32_IO_v${version_dash}${beta}.png)

## References

| Measurement    |                                                               Latest |
|----------------|---------------------------------------------------------------------:|
| Capozzi et al. |                 [hep-ph/2107.00532](data/theor_capozzi_2021-07.yaml) |
| DUNE           |                  [hep-ex/2006.16043](data/dune_future_2020_acc.yaml) |
| Daya Bay nGd   |              [Neutrino 2022](data/dayabay_2022-06-neutrino2022.yaml) |
| Forero et al.  | [hep-ph/2006.11237](data/theor_forero_2020-06-pre-neutrino2020.yaml) |
| IceCube        |          [hep-ex/1707.07081](data/icecube_2020-07-neutrino2020.yaml) |
| JUNO           |           [hep-ex/1507.05613](data/juno_future_2015-07-reactor.yaml) |
| MINOS+         |            [hep-ex/2006.15208](data/minos_2020-07-neutrino2020.yaml) |
| NOvA           |             [hep-ex/2108.08219](data/nova_2020-07-neutrino2020.yaml) |
| NuFIT 5.1      |                       [NuFIT 5.1](data/theor_nufit_5_1_2021-10.yaml) |
| RENO           |                 [Neutrino 2020](data/reno_2020-07-neutrino2020.yaml) |
| RENO nH        |                 [Neutrino 2018](data/reno_2018-06-neutrino2018.yaml) |
| SuperK         |               [Neutrino 2020](data/superk_2020-07-neutrino2020.yaml) |
| T2K            |                  [Neutrino 2020](data/t2k_2020-07-neutrino2020.yaml) |

