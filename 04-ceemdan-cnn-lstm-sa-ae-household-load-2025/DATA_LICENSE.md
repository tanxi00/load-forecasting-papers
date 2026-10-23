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

`data/eia_pjm_hourly_demand.csv` is derived from the U.S. Energy Information
Administration's EIA-930 Hourly Electric Grid Monitor:
https://www.eia.gov/electricity/gridmonitor/

The source is U.S. government public-domain data. Missing hourly values were
linearly filled and identified with `is_imputed`.
