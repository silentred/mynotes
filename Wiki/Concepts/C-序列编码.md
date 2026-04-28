---
id: C-序列编码
title: 序列编码（Sequence Encoding for ML）
reference: "Clippings/Chapter 4 Learning From Sequences and Alignments  From sequences to knowledge, improving and learning from sequence alignments.md"
updated: 2026-04-28
---

## 定义

序列编码是将生物序列（DNA、RNA 或蛋白质的字母串）转换为机器学习模型可接受的数值向量的过程。编码方案的选择直接影响模型能学到什么，因为不同的编码方式隐含了对氨基酸/核苷酸之间关系的不同假设。

## 关联来源

[[Clippings/Chapter 4 Learning From Sequences and Alignments  From sequences to knowledge, improving and learning from sequence alignments.md]]

## 已知边界 / 局限

- **通用编码（Ordinal / Binary / OHE）**：忽视生物结构信息，只是将字母转换为数字；OHE 的特征维度随序列长度和字母表大小线性增长（DNA: n×4，蛋白质: n×20）。
- **生物特异编码（AAIndex / Taylor's Venn / BLOMAP）**：依赖已知的物理化学性质数据库，可能不适用于非标准氨基酸或人工蛋白质。
- **学习式嵌入（learned embeddings）**：需要大量训练数据，结果难以解释，且依赖训练语料的分布——在特定家族蛋白上训练的嵌入可能对其他家族蛋白质不适用。
- 所有编码方案的一个共同局限：**编码的是序列信息，而非结构信息**——真正影响蛋白功能的 3D 结构信息需要通过 MSA 的共变信号间接获取。

## 实际案例

- Blassel 在 HIV 耐药分类研究中对比了 5 种编码方案（Ordinal, Binary, OHE, AAIndex, Group），在 10 个 RF 模型的二进制分类任务上评估准确率/精确率/召回率，OHE 综合表现最优且解释性最强，被采用为 Chapter 6 研究的编码方案。
- BLOMAP（基于 BLOSUM62 的 5 维编码）成功用于 HIV-1 蛋白酶切割位点预测，证明了从替换矩阵蒸馏进化信息到编码向量的有效性。
