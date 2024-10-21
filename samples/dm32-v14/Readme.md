# |Δm²₃₂|/|Δm²₃₁| measurements comparison

- Version: **${version_num}${beta}**
- Updates since v${version_prev}:
    * Daya Bay results are published
- [Plotting scripts](samples/${variable}/${variable}-v${version_num}-${suffix})
- Conversions:
    * Effective mass splitting $`|\Delta m^2_\mathrm{ee}|`$ conversion (RENO):
        + $`|\Delta m^2_{31}| = |\Delta m^2_\mathrm{ee}| + \alpha \sin^2\theta_{12} \Delta m^2_{21}`$.
        + $`|\Delta m^2_{32}| = |\Delta m^2_\mathrm{ee}| - \alpha \cos^2\theta_{12} \Delta m^2_{21}`$.
    * $`|\Delta m^2_\mathrm{31}|`$ to $`|\Delta m^2_\mathrm{32}|`$ conversion:
        + $`|\Delta m^2_{32}| = |\Delta m^2_\mathrm{31}| - \alpha |\Delta m^2_\mathrm{21}|`$.
    * $`\alpha`$ is +1/-1 for NO/IO.
    * PDG 2020 values:
        + $`\sin^2\theta_{12} = 0.307`$
        + $`\Delta m^2_{21} = 7.53\cdot10^{-5}\text{ eV}^2`$
    * Asymmetric syst/stat errors conversion: quadratically sum left and right part of each (stat/syst) contribution independently
- Cross checks by:
    * @ldkolupaeva
    * @maxfl
- Notes:
    * Forero et al. is pre-Neutrino fit
    * [IceCube](data/icecube_2023-04.yaml): NO value and uncertainty are used for the IO

[TOC]

## Latest results

### |Δm²₃₂|

#### Including global analyses and future experiments

![\|Δm²₃₂\| NO](png/NO/latest/dm32/dm32_v${version_dash}${beta}_NO_latest_global_future.png)

![\|Δm²₃₂\| IO](png/IO/latest/dm32/dm32_v${version_dash}${beta}_IO_latest_global_future.png)

#### Including global analyses

![\|Δm²₃₂\| NO](png/NO/latest/dm32/dm32_v${version_dash}${beta}_NO_latest_global.png)

![\|Δm²₃₂\| IO](png/IO/latest/dm32/dm32_v${version_dash}${beta}_IO_latest_global.png)

#### Experiments only

![\|Δm²₃₂\| NO](png/NO/latest/dm32/dm32_v${version_dash}${beta}_NO_latest.png)

![\|Δm²₃₂\| IO](png/IO/latest/dm32/dm32_v${version_dash}${beta}_IO_latest.png)

### |Δm²₃₁|

#### Including global analyses and future experiments

![\|Δm²₃₁\| NO](png/NO/latest/dm31/dm31_v${version_dash}${beta}_NO_latest_global_future.png)

![\|Δm²₃₁\| IO](png/IO/latest/dm31/dm31_v${version_dash}${beta}_IO_latest_global_future.png)

#### Including global analyses

![\|Δm²₃₁\| NO](png/NO/latest/dm31/dm31_v${version_dash}${beta}_NO_latest_global.png)

![\|Δm²₃₁\| IO](png/IO/latest/dm31/dm31_v${version_dash}${beta}_IO_latest_global.png)

#### Experiments only

![\|Δm²₃₁\| NO](png/NO/latest/dm31/dm31_v${version_dash}${beta}_NO_latest.png)

![\|Δm²₃₁\| IO](png/IO/latest/dm31/dm31_v${version_dash}${beta}_IO_latest.png)

## References

| Measurement     |                                                            Published |                                                     Latest |
|-----------------|---------------------------------------------------------------------:|-----------------------------------------------------------:|
| Capozzi et al.  |                 [hep-ph/2107.00532](data/theor_capozzi_2021-07.yaml) |                                                            |
| DUNE            |                  [hep-ex/2006.16043](data/dune_future_2020_acc.yaml) |                                                            |
| Daya Bay nGd    |                   [hep-ex/2211.14988](data/dayabay_2022-11-nGd.yaml) |                                                            |
| Daya Bay nH     |                    [hep-ex/2406.01007](data/dayabay_2024-06-nH.yaml) |                                                            |
| ESSνSB          |                       [hep-ex/2107.07585](data/ess_future_2021.yaml) |                                                            |
| de Salas et al. | [hep-ph/2006.11237](data/theor_forero_2020-06-pre-neutrino2020.yaml) |                                                            |
| HyperK          |            [hep-ex/1805.04163](data/hyperk_future_2018_acc_atm.yaml) |                                                            |
| IceCube         |                       [hep-ex/2304.12236](data/icecube_2023-04.yaml) |                                                            |
| IceCube future  |                   [hep-ex/1911.06745](data/icecube_future_2019.yaml) |                                                            |
| INO             |              [physics.ins-det/1505.07380](data/ino_future_2015.yaml) |                                                            |
| JUNO            |           [hep-ex/2204.13249](data/juno_future_2022-04-reactor.yaml) |                                                            |
| MINOS+          |            [hep-ex/2006.15208](data/minos_2020-07-neutrino2020.yaml) |                                                            |
| NOvA            |             [hep-ex/2108.08219](data/nova_2020-07-neutrino2020.yaml) |                                                            |
| NuFIT           |                       [NuFIT 5.2](data/theor_nufit_5_2_2022-11.yaml) |                 [NuFIT 6](data/theor_nufit_6_2024-10.yaml) |
| PDG             |                                      [PDG](data/theor_pdg_2022.yaml) |                                                            |
| ORCA            |                      [hep-ex/2103.09885](data/orca_future_2021.yaml) |                                                            |
| RENO            |                          [hep-ex/1806.00248](data/reno_2018-06.yaml) |       [Neutrino 2020](data/reno_2020-07-neutrino2020.yaml) |
| SuperCHOOZ      |                                                                      | [CERN seminar 2022](https://indico.cern.ch/event/1215214/) |
| SuperK          |                        [hep-ex/1901.03230](data/superk_2019-01.yaml) |     [Neutrino 2020](data/superk_2020-07-neutrino2020.yaml) |
| T2K             |                           [hep-ex/2101.03779](data/t2k_2021-01.yaml) |        [Neutrino 2020](data/t2k_2020-07-neutrino2020.yaml) |

