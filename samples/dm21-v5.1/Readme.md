# DRAFT: $`\Delta m^2_{21}`$ measurements comparison

- Version: **${version_num}${beta}**
- Updates since v${version_prev}:
    * Add PDG and update to NuFIT 5.2
- [Plotting scripts](samples/${variable}/${variable}-v${version_num}-${suffix})
- Data tables:
    * [published](${variable}_v${version_dash}${beta}_published.dat)
    * [latest](${variable}_v${version_dash}${beta}_latest.dat)
- Cross checks by:
    * @ldkolupaeva
    * @maxfl
- Notes:
    * Forero et al. is pre-Neutrino fit

## Plots

### Including global analyses and future experiments

![Δm²₂₁](png/latest/${variable}_v${version_dash}${beta}_latest_global_future.png)

### Including global analyses

![Δm²₂₁](png/latest/${variable}_v${version_dash}${beta}_latest_global.png)

### Experiments only

![Δm²₂₁](png/latest/${variable}_v${version_dash}${beta}_latest.png)

## References

| Measurement        |                                                            Published |                                                            Latest |
|--------------------|---------------------------------------------------------------------:|------------------------------------------------------------------:|
| Capozzi et al.     |                 [hep-ph/2107.00532](data/theor_capozzi_2021-07.yaml) |                                                                   |
| DUNE               |                  [hep-ph/1808.08232](data/dune_future_2018_sol.yaml) |                                                                   |
| de Salas et al.      | [hep-ph/2006.11237](data/theor_forero_2020-06-pre-neutrino2020.yaml) |                                                                   |
| HyperK             |                                                                      |                     [ICHEP2020](data/hyperk_future_2020_sol.yaml) |
| JUNO               |           [hep-ex/2204.13249](data/juno_future_2022-04-reactor.yaml) | [Neutrino 2022](data/juno_future_2022-06-solar-neutrino2022.yaml) |
| KamLAND            |          [hep-ex/1606.07538](data/kamland_2020-07-neutrino2020.yaml) |                                                                   |
| NuFIT 5.2          |                       [NuFIT 5.2](data/theor_nufit_5_2_2022-11.yaml) |                                                                   |
| PDG                |                       [PDG](data/theor_pdg_2022.yaml) |                                                                   |
| SNO                |               [hep-ex/1109.0763](data/sno_2020-07-neutrino2020.yaml) |                                                                   |
| SuperK+SNO         |                        [hep-ex/1606.07538](data/sk+sno_2016-06.yaml) |            [Neutrino 2022](data/sk+sno_2022-06-neutrino2022.yaml) |
| SuperK+SNO+KamLAND |                [hep-ex/1606.07538](data/kamland+sk+sno_2016-06.yaml) |    [Neutrino 2022](data/kamland+sk+sno_2022-06-neutrino2022.yaml) |
