# WPuQ Household Load

## Source

This data is derived from the WPuQ v2.0 dataset:

- Schlemminger, M., Ohrdes, T., Schneider, E., and Knoop, M.
- WPuQ household and heat pump electric load profiles
- DOI: `10.5281/zenodo.4719835`
- License: CC-BY-4.0
- Location: Hamelin, Germany

Raw files used:

```text
2019_data_60min.hdf5
2020_data_60min.hdf5
```

## Processing

1. Read `NO_PV/<household>/HOUSEHOLD/table:P_TOT` for 2019 and 2020.
2. Keep households present in both annual files.
3. Keep households with zero missing hourly observations.
4. Sum the selected household loads at each timestamp.
5. Convert aggregate active power from W to kW.
6. Store UTC timestamps as `date`.

Selected households:

```text
SFH3, SFH4, SFH5, SFH7, SFH9, SFH12, SFH14, SFH16, SFH18,
SFH19, SFH20, SFH21, SFH22, SFH27, SFH28, SFH29, SFH30,
SFH32, SFH34, SFH36, SFH38, SFH39
```

## Files

- `wpuq_household_hourly.csv`: model-ready aggregate household load.
- `wpuq_household_inventory.csv`: missing-hour statistics for all households.

Model-ready columns:

```text
date,load_kw
```

## Validation

- Selected households: 22
- Rows: 17,544
- Range: 2019-01-01 00:00:00 to 2020-12-31 23:00:00
- Frequency: hourly
- Missing values: 0
- Aggregate load range: 2.957437777815925 to 20.11640735346477 kW

The aggregate matches the authors' published WPuQ forecasting aggregate with
a maximum absolute difference of approximately `1.1e-14 kW`.

## Attribution

When using this derived file, cite the WPuQ dataset and:

Semmelmann, L., Hertel, M., Kircher, K. J., Mikut, R., Hagenmeyer, V.,
and Weinhardt, C. (2024). The impact of heat pumps on day-ahead energy
community load forecasting. Applied Energy, 368, 123364.
