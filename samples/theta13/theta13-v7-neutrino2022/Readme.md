# DRAFT: $`\sin^22\theta_{13}`$ measurements comparison

- Version: **${version_num}${beta}**
- Updates since v${version_prev}:
    * Add Neutrino 2022 results:
        + Daya Bay
    * Add RENO nH as published result as well
- [Plotting scripts](samples/${variable}/${variable}-v${version_num}-${suffix})
- Data tables:
    * [published](${variable}_v${version_dash}${beta}_published.dat)
    * [latest](${variable}_v${version_dash}${beta}_latest.dat)
- Cross checks by:
    * @ldkolupaeva
    * @maxfl
- Notes:
    * Forero et al. is pre-Neutrino fit
    * dashed grey bar in theoretical entry means IO

## Latest results

###  Including global analyses and future experiments
![sin²2θ₁₃](png/latest/${variable}_v${version_dash}${beta}_latest_global_future.png)

### Experiments only
![sin²2θ₁₃](png/latest/${variable}_v${version_dash}${beta}_latest.png)

## References

| Measurement    |                                                   Published |                                                   Latest |                                                                 Both |
|----------------|------------------------------------------------------------:|---------------------------------------------------------:|---------------------------------------------------------------------:|
| Capozzi et al. |                                                             |                                                          |                 [hep-ph/2107.00532](data/theor_capozzi_2021-07.yaml) |
| DUNE           |                                                             |                                                          |                  [hep-ex/2006.16043](data/dune_future_2020_acc.yaml) |
| Daya Bay nGd   | [hep-ex/1809.02261](data/dayabay_2018-06-neutrino2018.yaml) |  [Neutrino 2022](data/dayabay_2022-06-neutrino2022.yaml) |                                                                      |
| Daya Bay nH    |                                                             |                                                          |          [hep-ex/1603.03549](data/dayabay_2016-07-neutrino2016.yaml) |
| Double CHOOZ   |               [hep-ex/1901.09445](data/dchooz_2019-01.yaml) |   [Neutrino 2020](data/dchooz_2020-07-neutrino2020.yaml) |                                                                      |
| Forero et al.  |                                                             |                                                          | [hep-ph/2006.11237](data/theor_forero_2020-06-pre-neutrino2020.yaml) |
| JUNO           |                                                             |                                                          |           [hep-ex/2204.13249](data/juno_future_2022-04-reactor.yaml) |
| NuFIT 5.0      |                                                             |                                                          |         [NuFIT 5.0](data/theor_nufit_2020-07-post-neutrino2020.yaml) |
| RENO nGd       |                 [hep-ex/1806.00248](data/reno_2018-06.yaml) | [Neutrino 2020](data/reno_2020-07-nGd-neutrino2020.yaml) |                                                                      |
| RENO nH        |                                                             |                                                          |                       [hep-ex/1911.04601](data/reno_2019-11_nh.yaml) |
| T2K            |                  [hep-ex/2101.03779](data/t2k_2021-01.yaml) |      [Neutrino 2020](data/t2k_2020-07-neutrino2020.yaml) |                                                                      |
