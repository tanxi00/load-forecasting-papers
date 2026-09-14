# 负荷预测论文代码与数据合集

个人整理的电力/能源负荷预测**期刊论文**配套代码与数据，按研究主题分目录存放。

## 分类索引

| 目录 | 类别 | 论文 | 期刊 / 年份 | DOI | 上游仓库 | 许可 |
|---|---|---|---|---|---|---|
| `01-energy-community-heatpump-load-forecasting` | 居民与能源社区负荷预测 | The impact of heat pumps on day-ahead energy community load forecasting | Applied Energy, 368 (2024) | [10.1016/j.apenergy.2024.123364](https://doi.org/10.1016/j.apenergy.2024.123364) | [leloq/load-forecasting-with-heatpumps](https://github.com/leloq/load-forecasting-with-heatpumps) @ `6b76f0d` | MIT |
| `02-midterm-hourly-load-forecasting-gam` | 系统级中短期负荷预测 | Efficient mid-term forecasting of hourly electricity load using generalized additive models | Applied Energy, 388 (2025) | [10.1016/j.apenergy.2025.125444](https://doi.org/10.1016/j.apenergy.2025.125444) | [MonikaZimmermann/load-forecasting](https://github.com/MonikaZimmermann/load-forecasting) @ `758414d` | GPL-3.0 |

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

## 来源与许可

- 两个子目录的代码与数据分别来自上表列出的上游仓库，各自沿用原始许可证：
  - `01-...` MIT License，见该目录下的 `LICENSE`
  - `02-...` GNU General Public License v3，见该目录下的 `LICENSE`
- 本仓库仅做归集整理，未修改原始代码；文件内容与上游对应提交一致。引用请优先引用原论文与上游仓库。
