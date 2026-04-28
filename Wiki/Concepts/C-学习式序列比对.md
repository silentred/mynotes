---
id: C-学习式序列比对
title: 学习式序列比对（Learned Sequence Alignment）
reference: "Clippings/Chapter 7 Learning Alignments, an Interesting Perspective  From sequences to knowledge, improving and learning from sequence alignments.md"
updated: 2026-04-28
---

## 定义

学习式序列比对是指用机器学习方法（主要是深度学习）替代或增强传统动态规划比对算法的过程。它有两种主要范式：（1）**预测替换矩阵**——用神经网络预测位置特异性评分矩阵（PSSM），再喂给经典比对算法（NW/SW）；（2）**直接预测比对**——用序列到序列模型直接输出对齐结果，跳过显式的评分矩阵步骤。

## 关联来源

[[Clippings/Chapter 7 Learning Alignments, an Interesting Perspective  From sequences to knowledge, improving and learning from sequence alignments.md]]
[[Clippings/Chapter 2 Aligning Sequence Data  From sequences to knowledge, improving and learning from sequence alignments.md]]

## 已知边界 / 局限

- **注意力二次复杂度瓶颈**：Transformer 的 self-attention 时间和空间复杂度为 O(n²)，长序列（>1000 残基）训练成本极高，基因组级别的序列不可行。
- **数据依赖**：学习式比对需要大量标注数据（通常是结构比对或模拟比对），标注质量直接决定模型质量——而结构比对的覆盖范围远小于序列数据的规模。
- **泛化问题**：在特定蛋白家族或数据分布上训练的模型可能无法泛化到进化距离较远的序列对——DEDAL 在远程同源比对上的优势依赖于其预训练数据的多样性。
- **可解释性差**：学习式比对学到的 scoring function 是一个黑箱，不像 PAM/BLOSUM 矩阵那样有清晰的进化模型解释。当比对结果与传统方法不一致时，很难判断哪个更"正确"。
- **读长比对的额外挑战**：参考序列和读段之间的长度差使 seq2seq 模型非常不经济——当前最实用的方向是学习式索引和学习式种子选择，而非端到端学习比对。

## 实际案例

- **DEDAL**：用 Transformer 编码残基对，预测位点特异的匹配/空位开启/空位延伸得分，结合可微 SW 算法做端到端训练，在 Pfam-A 种子数据库的远程同源比对上优于 MUSCLE 等传统方法。
- **BetaAlign**：将比对形式化为"从非比对序列翻译到比对序列"，用 Transformer 直接输出对齐，在短序列（~40 残基）上超过传统多序列比对工具。
- **AlphaFold2 的 EvoFormer**：通过 MSA 上的跨序列注意力机制（attention over rows and columns）学习位置间的共变关系，是目前"学习式序列信息利用"最成功的工程案例。
- **BWA-MEME / DeepMinimizer**：在读长比对场景中，用学习式索引替代后缀数组，用学习式 minimizer 选择优化种子密度，展示了 ML 在比对流程特定步骤上增强（而非取代）传统算法的价值。
