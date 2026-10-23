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
| Kentucky/PJM 区域负荷 | EIA-930 PJM 小时需求 | 2022-01 至 2024-12 | 小时 |

Plegma 数据包含希腊 13 户家庭，许可为 CC BY 4.0。这里的
`House_01` 被作为主单户序列，完整 13 户聚合结果也保留在
`data/plegma_all_households_15min.csv`。

EIA 的 `demand_mw` 来自 EIA-930 小时需求。EIA 原始值标为每小时 MWh，
其数值与小时平均 MW 相同，因此保留字段名 `demand_mw`。

## 文件

- `data/plegma_house01_15min.csv`：论文式单户 15 分钟主实验数据。
- `data/plegma_all_households_15min.csv`：13 户 15 分钟数据，便于扩展成
  多户实验。
- `data/eia_pjm_hourly_demand.csv`：PJM 2022-2024 小时需求。
- `scripts/download_and_prepare.py`：官方数据处理脚本。

Plegma 列：

- `load_kw`：15 分钟内的整户平均有功功率。
- `energy_kwh`：由平均功率换算的 15 分钟电量，即 `load_kw / 4`。
- `source_10s_samples`：该 15 分钟区间中实际存在的 10 秒样本数。
- `source_coverage`：相对完整覆盖 90 个 10 秒样本的比例。
- `raw_load_kw`：插值前的原始聚合值。
- `is_imputed`：`1` 表示因缺失而使用线性插值填充。

`eia_pjm_hourly_demand.csv` 同时保留 `demand_mw_raw` 和插值后的
`demand_mw`，并通过 `is_imputed` 标识填充值。

## 复现

1. 从
   `https://doi.org/10.15129/3b01a6c6-2efd-424a-b8b8-5fe7fa445ded`
   下载 `PlegmaDataset_Clean.7z`，解压得到 `House_01` 至 `House_13`。
2. 从 <https://www.eia.gov/opendata/> 申请免费 API key。
3. 运行：

```bash
python scripts/download_and_prepare.py \
  --plegma-root /path/to/Clean_Dataset \
  --eia-api-key "$EIA_API_KEY" \
  --output-dir data
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
- EIA-930 Hourly Electric Grid Monitor:
  <https://www.eia.gov/electricity/gridmonitor/>, U.S. public-domain data.

再分发派生 CSV 时请保留上述署名与来源链接。
