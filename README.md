# 负荷预测论文代码与数据合集

个人整理的电力/能源负荷预测**期刊论文**配套代码与数据，按研究主题分目录存放。

## 分类索引

| 目录 | 类别 | 论文 | 期刊 / 年份 | DOI | 上游仓库 | 许可 |
|---|---|---|---|---|---|---|
| `01-energy-community-heatpump-load-forecasting` | 居民与能源社区负荷预测 | The impact of heat pumps on day-ahead energy community load forecasting | Applied Energy, 368 (2024) | [10.1016/j.apenergy.2024.123364](https://doi.org/10.1016/j.apenergy.2024.123364) | [leloq/load-forecasting-with-heatpumps](https://github.com/leloq/load-forecasting-with-heatpumps) @ `6b76f0d` | MIT |
| `02-midterm-hourly-load-forecasting-gam` | 系统级中短期负荷预测 | Efficient mid-term forecasting of hourly electricity load using generalized additive models | Applied Energy, 388 (2025) | [10.1016/j.apenergy.2025.125444](https://doi.org/10.1016/j.apenergy.2025.125444) | [MonikaZimmermann/load-forecasting](https://github.com/MonikaZimmermann/load-forecasting) @ `758414d` | GPL-3.0 |
| `03-time-series-forecasting-models-2026` | 时序预测模型合集（2026 顶会） | Dynamic TMoE / FreqCycle / SiGMA | ICML 2026 / AAAI 2026 / ICML 2026 | — | [andone-07/Dynamic-TMoE](https://github.com/andone-07/Dynamic-TMoE) 等 3 个（见目录内 README） | SiGMA 为 MIT，其余未声明 |
| `04-ceemdan-cnn-lstm-sa-ae-household-load-2025` | 家庭与系统级负荷预测 | A novel CNN-LSTM-based forecasting model for household electricity load by merging mode decomposition, self-attention and autoencoder | Energy, 330 (2025) | [10.1016/j.energy.2025.136883](https://doi.org/10.1016/j.energy.2025.136883) | 作者未公开代码；提供近年替代数据与处理脚本 | Plegma CC BY 4.0；EIA 公共领域 |

## 目录说明

### 01-energy-community-heatpump-load-forecasting

- 作者：Leo Semmelmann, Matthias Hertel, Kevin J. Kircher, Ralf Mikut, Veit Hagenmeyer, Christof Weinhardt
- 内容：含热泵的能源社区日前负荷预测。发布预测方法、基准流水线、特征工程与筛选后的数据、最终结果
- 数据：`data/`、`results/`，另附 XGBoost 与 Transformer 两套实现
- 环境：Jupyter Notebook / Python（`requirements.txt`）

### 02-midterm-hourly-load-forecasting-gam

- 作者：Monika Zimmermann, Florian Ziel
- 内容：用广义可加模型（GAM）做小时级中期电力负荷预测，示例覆盖法国与德国
- 数据：24 个欧洲国家 2015-01 至 2024-02 的预处理数据（负荷、气温、节假日、季节模式）
- 环境：R

### 03-time-series-forecasting-models-2026

- 内容：2026 年顶会主赛道的时序预测模型官方实现，用于论文A 的对比实验
- 收录：Dynamic TMoE（ICML 2026）、FreqCycle（AAAI 2026）、SiGMA（ICML 2026）
- 环境：Python 3.8–3.10 / PyTorch（基于 Time-Series-Library 框架，`--seq_len 48 --pred_len 24` 对应论文A 口径）

### 04-ceemdan-cnn-lstm-sa-ae-household-load-2025

- 论文：Chun Li, Jiarong Shi. *Energy* 330 (2025) 136883
- 原数据：Sceaux 单户 2006-12 至 2010-11（实验仅取前 10,000 条）；Kentucky/PJM 2012-2018
- 近年替代：Plegma 希腊 13 户（2022-07 至 2023-09）；EIA-930 PJM 2022-2024 小时需求
- 数据：单户 15 分钟主序列、13 户 15 分钟汇总序列、PJM 小时需求，并保留缺失插值标记
- 代码：官方代码未公开；本目录新增数据下载、15 分钟聚合和缺失值处理脚本

## 来源与许可

- 各子目录的代码与数据分别来自上表列出的上游仓库，各自沿用原始许可证：
  - `01-...` MIT License，见该目录下的 `LICENSE`
  - `02-...` GNU General Public License v3，见该目录下的 `LICENSE`
  - `03-...` SiGMA 为 MIT License，见该目录下的 `LICENSE`；Dynamic TMoE 与 FreqCycle 上游未声明顶层许可证，仅 `Dynamic-TMoE` 内部归集的基线带有各自许可
  - `04-...` 数据来自 Plegma（CC BY 4.0）与 EIA-930（美国公共领域），详见该目录下的 `DATA_LICENSE.md`
- `01`—`03` 保留上游原始代码；`04` 的下载/预处理脚本为本仓库新增。引用请优先引用原论文与数据提供方。
