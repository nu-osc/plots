# $`\sin^2 \theta_{12}`$ measurements comparison

## Table of contents

- [Summary](<#summary>)
- [Plots](<#plots>)
    * [Experiments only](<#experiments-only>)
    * [Including global analyses and future experiments](<#including-global-analyses-and-future-experiments>)
    * [Including global analyses](<#including-global-analyses>)
- [References](<#references>)

## Summary

- Version: **8**
- Updates since v7:
    * Add NuFIT-6.1
- [Plotting scripts](samples/theta12/theta12-v8-)
- Data tables:
    * [published](theta12_v8_published.dat)
    * [latest](theta12_v8_latest.dat)
- Cross checks by:
    * @ldkolupaeva
    * @maxfl
- Notes:
    * de Salas et al. and Capozzi et al. are pre-Neutrino 2024 fits
    * $`\tan^2 \theta_{12}`$ to $`\sin^2 \theta_{12}`$ conversion:
        + $`\sin^2 \theta_{12} = 1 - 1/(1+\tan^2 \theta_{12})`$.

## Plots

### Experiments only

![sin²θ₁₂](png/latest/theta12_v8_latest.png)

###  Including global analyses and future experiments

![sin²θ₁₂](png/latest/theta12_v8_latest_global_future.png)

### Including global analyses

![sin²θ₁₂](png/latest/theta12_v8_latest_global.png)

## References

| Measurement       |                                                                                                            Published |                                                  Latest |
|-------------------|---------------------------------------------------------------------------------------------------------------------:|--------------------------------------------------------:|
| Capozzi et al.    |                                                                 [hep-ph/2107.00532](data/theor_capozzi_2021-07.yaml) |                                                         |
| DUNE              |                                                                  [hep-ph/1808.08232](data/dune_future_2018_sol.yaml) |                                                         |
| de Salas et al.   |                                                 [hep-ph/2006.11237](data/theor_forero_2020-06-pre-neutrino2020.yaml) |                                                         |
| HyperK            |                                                                                                                      |           [ICHEP2020](data/hyperk_future_2020_sol.yaml) |
| JUNO              |                                                                                                                      |             [hep-ex/2511.14593](data/juno_2025-11.yaml) |
| JUNO sensitivity  | [hep-ex/2204.13249](data/juno_future_2022-04-reactor.yaml), [hep-ex/2210.08437](data/juno_future_2022-10-solar.yaml) |                                                         |
| KamLAND           |                                                          [hep-ex/1606.07538](data/kamland_2020-07-neutrino2020.yaml) |                                                         |
| NuFIT 6.1         |                                                                       [NuFIT 6.1](data/theor_nufit_6-1_2025-12.yaml) |                                                         |
| PDG 2024          |                                                                                      [PDG](data/theor_pdg_2024.yaml) |                                                         |
| SNO               |                                                               [hep-ex/1109.0763](data/sno_2020-07-neutrino2020.yaml) |                                                         |
| SNO+, constrained |                                                              [hep-ex/2505.04469](data/snoplus_2025-05_combined.yaml) | [hep-ex/2511.11856](data/snoplus_2025-11_combined.yaml) |
| Solar global      |                                                                [hep-ex/2312.12907](data/kamland+sk+sno_2023-12.yaml) |                                                         |
| Solar+KamLAND     |                                                                [hep-ex/2312.12907](data/kamland+sk+sno_2023-12.yaml) |                                                         |
