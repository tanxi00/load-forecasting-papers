# 03-time-series-forecasting-models-2026

2026 年顶会主赛道的时序预测模型官方实现，用于论文A（Semmelmann et al. 2024）的模型对比实验。

所有子目录均为**上游官方仓库原样归集**，未修改任何代码；引用方式与许可证以各目录内的原始文件为准。

## 收录清单

| 目录 | 模型 | 会议 / 年份 | 上游仓库 | 许可 | 代码状态 |
|---|---|---|---|---|---|
| `Dynamic-TMoE` | Drift-Aware Dynamic Mixture of Experts | ICML 2026 | [andone-07/Dynamic-TMoE](https://github.com/andone-07/Dynamic-TMoE) @ `3e41235` | 未声明（`baselines/` 内各基线沿用各自许可） | 完整 |
| `FreqCycle` | Multi-Scale Time-Frequency Analysis | AAAI 2026 | [boya-zhang-ai/FreqCycle](https://github.com/boya-zhang-ai/FreqCycle) @ `668ba82` | 未声明 | 完整 |
| `SiGMA` | Generalizing Multi-Scale Modeling with a Single Operator | ICML 2026 | [cheonwoolee/SiGMA](https://github.com/cheonwoolee/SiGMA) @ `b4ac7c9` | MIT | 完整 |

> 本目录原先收录的是 `xCPD`（ICLR 2026，`Clearloveyuan/xCPD`）。但其上游仓库 README 只有一句
> "We will release our source code in recent two weeks."，`models/` 下仅有 DLinear / PatchTST / TimeMixer /
> TSMixer 四个基线，模型本体至今未上传（最后一次提交 2026-03-19），无法运行，因此替换为代码完整的 SiGMA。
> 待 xCPD 作者放出代码后可再补收。

## 与论文A 实验的对齐

论文A 的任务是「看前 48 小时、预测未来 24 小时」的日前逐小时负荷预测，
数据分社区（Comb）/ 住户（HH）/ 热泵（HP）三个层级，并含气温等外生变量。

| 模型 | 在我们的任务里对应什么 |
|---|---|
| `Dynamic TMoE` | 漂移感知的动态专家池，对应数据集中 2019→2020 约 −21% 的年际漂移 |
| `FreqCycle` | 多尺度时频分析，替代原论文 CEEMDAN 分解那一套流程 |
| `SiGMA` | 单一算子统一多尺度，结构简洁、易复现，适合当主力对比基线 |

三个仓库都基于 [thuml/Time-Series-Library](https://github.com/thuml/Time-Series-Library) 的框架，
因此参数口径一致：`--seq_len 48 --pred_len 24` 即论文A 的输入/输出长度。
数据集需自行按各仓库 README 说明放置，训练命令为：

| 目录 | 训练命令 |
|---|---|
| `Dynamic-TMoE` | `bash scripts/ETTh1.sh`（按数据集名替换） |
| `FreqCycle` | `bash scripts/FreqCycle/etth1.sh` |
| `SiGMA` | `bash script/SiGMA_ETTh1.sh`（按数据集名替换） |
