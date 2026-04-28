---
id: S-Chapter4-LearningFromSequences
title: 如何从生物序列中学习：ML 在序列比对分析中的全景
author: Luc Blassel
source: "https://thesis.lucblassel.com/learning-from-sequences-and-alignments.html"
reference: "Clippings/Chapter 4 Learning From Sequences and Alignments  From sequences to knowledge, improving and learning from sequence alignments.md"
date: 2026-04-28
tags:
  - 机器学习
  - 生物信息学
  - 序列比对
---

## 核心内容总结
1. 监督学习（回归和分类）是生物序列分析中最成熟的范式，从蛋白质结构预测到病毒耐药性分类都已有大量验证。
2. 序列编码是将字母序列转为数值向量的关键预处理步骤——One-Hot 编码虽然增加特征维度但解释性最好，是实践中的首选。
3. 生物特异编码（如 AAIndex、Taylor's Venn、BLOMAP）将氨基酸的物理化学性质嵌入编码，可以提升模型对生物信号的捕捉能力。
4. 训练集/测试集分离、k-fold 交叉验证是对抗过拟合和数据泄漏的基本防线，在生物数据中尤其重要因为进化相关性很容易导致虚假信号。
5. 即使简单的模型（如 Naive Bayes、Logistic Regression）在合理的编码方案下也能表现良好，模型复杂度和可解释性的 trade-off 在生物学场景中始终存在。

## 关键数据
- BLOSUM62 矩阵衍生的 BLOMAP 编码将每个氨基酸映射为 **5** 维向量，成功预测了 HIV-1 蛋白酶切割位点。
- 对于 DNA，One-Hot 编码使特征维度变为 **n × 4**（n 为序列长度）——这是最常用的生物序列编码。
- AAIndex 数据库包含 **566** 种氨基酸物理化学性质指数，通过 PCA 降维后可选择最有信息量的子集。
- 测试了 Ordinal、Binary、OHE、AAIndex、Group 五种编码方案后，综合准确性、精确率和召回率，**OHE + Random Forest** 组合表现最优。

## 简述要点
如果把生物序列直接喂给机器学习模型，模型看到的只是一堆字母，而字母之间没有天然的数值关系。所以编码方案的选择直接决定了模型能从数据中学到什么——这是本章最核心的 insight。

Ordinal 编码（A=1, C=2, G=3, T=4）最直觉但引入了根本不存在的"顺序"，可能误导模型。One-Hot 编码解决了这个问题：每个氨基酸变成一个稀疏的二进制向量，虽然维度膨胀了，但每个特征的含义清晰，解释性强。在 Blassel 的实际实验中——为 Chapter 6 的 HIV 耐药研究做技术选型——OHE 确实是胜出的方案。还有一种更巧妙的思路是利用氨基酸的物理化学性质直接编码：AAIndex 把疏水性、柔性、残基体积等属性数字量化，BLOMAP 则从 BLOSUM62 替换矩阵中蒸馏出进化相似性信息。

机器学习范式的选择同样关键。监督学习（给定输入-输出对）在生物序列领域有天然的应用场景——从序列预测甲基化位点、剪接位点、蛋白功能，到预测病毒耐药性。无监督学习（只有输入，没有标签）则用于聚类蛋白家族、降维（PCA 直接作用于 MSA）、以及距离矩阵的快速近似。最近**自监督学习**（先做预训练任务，再微调）在蛋白语言模型（如 ProtBert）上爆发，这与 NLP 的 BERT 一脉相承。还有一个少被提及但很实用的点：**end-to-end 学习**——把序列比对这种传统非 ML 任务做成可微分的损失函数，嵌入神经网络联合优化，这正是 Chapter 7 的主题。

对于实际做分析的人，本章最值得记住的是**过拟合和数据泄漏**的警告。在生物序列分析中，直接把训练集上见过的序列拿去测试是错误的——因为进化相关性会让同源序列出现在两个集合中，模型的泛化能力会被严重高估。按 HIV 亚型拆分训练/测试集是一种有效的规避策略。

## 疑点 / 待验证
- 自监督学习方法（如蛋白语言模型）在大量数据上预训练后，对低数据量的生物学问题的迁移效果如何，本章未展开讨论。
- 文中提到 Ordinal 编码在某些情况下与 OHE 性能相当，具体什么条件下成立需要更多实验验证。

## 术语表
- **OHE (One-Hot Encoding)**：将分类变量编码为稀疏二进制向量，第 i 位为 1 表示该变量取第 i 个类别值
- **Overfitting**：模型在训练集上表现优异但在测试集上表现差，即学到了训练数据的噪声特征而非可泛化模式
- **k-fold Cross-Validation**：将训练集分为 k 份，轮流用 1 份验证、k-1 份训练，取 k 次平均性能评估
- **AAIndex**：公共数据库，收录氨基酸的各种物理化学性质指数，每组指数为 20 个数值（每种氨基酸一个）
- **BLOMAP**：基于 BLOSUM62 替换矩阵的非线性投影编码，将每个氨基酸编码为 5 维向量

## 原始来源
[[Clippings/Chapter 4 Learning From Sequences and Alignments  From sequences to knowledge, improving and learning from sequence alignments.md]]
