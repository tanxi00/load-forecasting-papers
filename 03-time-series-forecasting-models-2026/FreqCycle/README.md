# FreqCycle
## Model Implementation

We propose FreqCycle, a novel framework integrating: (i) a Filter-Enhanced Cycle Forecasting (FECF) module to extract low-frequency features by explicitly learning shared periodic patterns in the time domain, and (ii) a Segmented Frequency-domain Pattern Learning (SFPL) module to enhance mid to high frequency energy proportion via learnable filters and adaptive weighting. The core implementation code of FreqCycle is available at:

```
models/FreqCycle.py
```

For the FECF part, To identify the relative position of each sample within the recurrent cycles, we need to generate cycle index (i.e., **_t_ mod _W_** ) additionally for each data sample. The code for this part is available at:

```
data_provider/data_loader.py
```
For the SFPL part, The specific implementation code of SFPL :
```python
class Time_seg(nn.Module):
```
We have two segmentation strategies for x:
Sliding window-based segmentation
Uniform segmentation into 2**s parts (where s is a given input)



## Getting Started

### Environment Requirements

To get started, ensure you have Conda installed on your system and follow these steps to set up the environment:

```
conda create -n FreqCycle python=3.10
conda activate FreqCycle
pip install -r requirements.txt
```

### Data Preparation

All the datasets needed for FreqCycle can be obtained from previous works such as Autoformer and SCINet. 
Create a separate folder named ```./data``` and place all the CSV files in this directory. 

### Training Example

You can easily reproduce the results from the paper by running the provided script command. For instance:

```
bash scripts/FreqCycle/etth1.sh

bash scripts/MFreqCycle/etth2.sh
```

### WPuQ household load experiment

This experiment replaces the Plegma household series with the aggregate
household load derived from the raw WPuQ 2019 and 2020 hourly HDF5 files.
The preparation script selects households present in both years with zero
missing hourly observations, aggregates their active power, and converts the
result from W to kW.

Input data:

```text
data/wpuq_household/wpuq_household_hourly.csv
```

Run on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_wpuq_household.ps1
```

The default experiment keeps the FreqCycle paper protocol: 8 past hours
predict the next hour, the first 80% is used for training, the last 20% is
used for testing, Adam uses a constant learning rate of 0.001, MSE is the
loss, and training runs for 100 epochs.

See `data/wpuq_household/README.md` for data provenance and processing details.
