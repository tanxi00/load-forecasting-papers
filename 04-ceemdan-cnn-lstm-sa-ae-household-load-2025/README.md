# CEEMDAN-CNN-LSTM-SA-AE household load forecasting

本目录对应论文：

> Chun Li, Jiarong Shi. A novel CNN-LSTM-based forecasting model for
> household electricity load by merging mode decomposition, self-attention
> and autoencoder. *Energy* 330 (2025) 136883.
> DOI: `10.1016/j.energy.2025.136883`

## 原论文数据

- 主实验：法国 Sceaux 单户用电数据，原始 1 分钟采样，2006-12 至
  2010-11；按 15 分钟聚合后共 138,354 条，论文只使用前 10,000 条。
  按常见 UCI 数据起点推算，这 10,000 条约覆盖 2006-12-16 至
  2007-03-30。
- 外部验证：论文称为 Kentucky/PJM 数据，小时级 MW 负荷。正文称
  2012-01-01 至 2018-03-08 共 57,740 条，并称后续实验使用 2018 年数据；
  但原图横轴显示出 2018 年下半年，数据口径存在内部不一致。

论文未公开代码。数据可用性声明只有 “Data will be made available on
request.”，公开检索也未找到作者代码仓库。

## 近年替代数据

| 原论文角色 | 替代数据 | 覆盖期 | 分辨率 |
|---|---|---|---|
| Sceaux 单户负荷 | Plegma `House_01` | 2022-07 至 2023-09 | 10 秒聚合成 15 分钟 |
| Kentucky/PJM 区域负荷 | PJM `DEOK` 小时负荷 | 2022-01 至 2026-10 | 小时 |

Plegma 数据包含希腊 13 户家庭，许可为 CC BY 4.0。这里的
`House_01` 被作为主单户序列，完整 13 户聚合结果也保留在
`data/plegma_all_households_15min.csv`。

论文中的“Kentucky dataset”与 PJM `DEOK` zone 高度吻合：原始 Kaggle
文件有 57,739 条，范围为 2012-01-01 至 2018-08-03；论文写 57,740 条，
仅相差 1 条。因此近年数据也从 PJM Data Miner 2 的 `DEOK` zone 获取。

## 文件

- `data/plegma_house01_15min.csv`：论文式单户 15 分钟主实验数据。
- `data/plegma_all_households_15min.csv`：13 户 15 分钟数据，便于扩展成
  多户实验。
- `data/pjm_deok_hourly_2022_2026.csv`：PJM DEOK 2022 年至 2026-10 的
  小时负荷。
- `scripts/download_and_prepare.py`：官方数据处理脚本。
- `scripts/download_pjm_deok.py`：PJM Data Miner 2 的 DEOK 下载脚本。

Plegma 列：

- `load_kw`：15 分钟内的整户平均有功功率。
- `energy_kwh`：由平均功率换算的 15 分钟电量，即 `load_kw / 4`。
- `source_10s_samples`：该 15 分钟区间中实际存在的 10 秒样本数。
- `source_coverage`：相对完整覆盖 90 个 10 秒样本的比例。
- `raw_load_kw`：插值前的原始聚合值。
- `is_imputed`：`1` 表示因缺失而使用线性插值填充。

`pjm_deok_hourly_2022_2026.csv` 同时保留 `demand_mw_raw` 和插值后的
`demand_mw`，并通过 `is_imputed` 标识填充值。

PJM DEOK 文件包含 42,119 个连续小时，UTC 范围为
2022-01-01 05:00 至 2026-10-22 03:00，对应 Eastern Prevailing Time
2022-01-01 00:00 至 2026-10-21 23:00。各年度行数为 8,760、8,760、
8,784、8,760、7,055；本次下载数据没有缺失小时，因此 `is_imputed`
全部为 0。

## 复现

1. 从
   `https://doi.org/10.15129/3b01a6c6-2efd-424a-b8b8-5fe7fa445ded`
   下载 `PlegmaDataset_Clean.7z`，解压得到 `House_01` 至 `House_13`。
2. 从 <https://apiportal.pjm.com/> 申请免费 Data Miner 2 API key。
3. 运行：

```bash
python scripts/download_and_prepare.py \
  --plegma-root /path/to/Clean_Dataset \
  --output-dir data

python scripts/download_pjm_deok.py \
  --api-key "$PJM_API_KEY" \
  --start 2022-01-01 \
  --end 2026-10-22 \
  --output data/pjm_deok_hourly_2022_2026.csv
```

## 训练注意

原论文先在完整序列上执行 CEEMDAN，再划分训练集和测试集。这个流程会让
测试期信息参与整段分量分解，可能高估效果。复现时应先按时间切分，再在
训练段拟合 CEEMDAN，测试阶段使用滚动或分块分解。

原论文的输入窗口为 8 个历史时刻、预测下一时刻、训练/测试按时间 80/20。
替换数据仍保持以下任务结构：

- Plegma：过去 2 小时预测未来 15 分钟。
- PJM：过去 8 小时预测未来 1 小时。

## 来源与许可

- Plegma Data: Athanasoulias et al., University of Strathclyde,
  DOI `10.15129/3b01a6c6-2efd-424a-b8b8-5fe7fa445ded`, CC BY 4.0.
- Plegma descriptor: Athanasoulias et al., *Scientific Data* 11, 376
  (2024), DOI `10.1038/s41597-024-03208-0`.
- PJM Data Miner 2, Hourly Load: Metered:
  <https://dataminer2.pjm.com/feed/hrl_load_metered>.

再分发派生 CSV 时请保留上述署名与来源链接。
