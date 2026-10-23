# Data license and attribution

`data/plegma_house01_15min.csv` and
`data/plegma_all_households_15min.csv` are derived from the Plegma Dataset:

> Athanasoulias, S. et al. Plegma Dataset. University of Strathclyde.
> https://doi.org/10.15129/3b01a6c6-2efd-424a-b8b8-5fe7fa445ded

The Plegma Dataset is licensed under the Creative Commons Attribution 4.0
International license:
https://creativecommons.org/licenses/by/4.0/

The derived files retain that license and attribution. Changes made here:
selected the 2022-07 to 2023-09 period, aggregated 10-second aggregate
active power to 15-minute means, converted power to 15-minute energy,
linearly filled missing intervals, and added coverage/imputation flags.

`data/pjm_deok_hourly_2022_2026.csv` is derived from PJM Data Miner 2:
https://dataminer2.pjm.com/feed/hrl_load_metered

The series is the DEOK transmission zone and remains subject to PJM's terms
of use. Missing hourly values were linearly filled and identified with
`is_imputed`.
