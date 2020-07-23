# $`\Delta m^2_{32}`$ measurements comparison, updated after Neutrino 2020

- Version: 4.0
- [Plotting scripts](samples/dm32/v4.0-neutrino2020)
- Data tables:
    * [NO table](samples/dm32/v4.0-neutrino2020/dm32_NO.dat)
    * [IO table](samples/dm32/v4.0-neutrino2020/dm32_IO.dat)
- References:
    * [Daya Bay nGd](data/dayabay_2018-06-neutrino2018.yaml)
    * [RENO](data/reno_2020-06-neutrino2020.yaml)
    * [RENO nH](data/reno_2018-06-neutrino2018.yaml)
    * [T2K](data/t2k_2020-06-neutrino2020.yaml)
    * [MINOS](data/minos_2020-06-neutrino2020.yaml)
    * [IceCube](data/icecube_2020-06-neutrino2020.yaml)
- Conversions:
    * Effective mass splitting $`\Delta m^2_\mathrm{ee}`$ conversion (RENO):
        + $`\Delta m^2_{32} = \Delta m^2_\mathrm{ee} - \alpha \cos^2\theta_{12} \Delta m^2_{21}`$
        + PDG 2020 values:
            + $`\sin^2\theta_{13} = 0.307`$
            + $`\Delta m^2_{21} = 7.53\cdot10^{-5}\text{ eV}^2`$
    * Asymmetric syst/stat errors conversion: quadratically sum left and right part of each (stat/syst) contribution independently
- Cross checks by:
    * Liudmila
    * Beda

![Δm²₃₂ NO](plots/dm32/v4.0-neutrino2020/dm32_NO_v4-0.png)
![Δm²₃₂ IO](plots/dm32/v4.0-neutrino2020/dm32_IO_v4-0.png)

