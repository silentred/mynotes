---
id: S-Chapter6-InferringMutationRoles
title: 用机器学习从序列比对中推断 HIV 耐药突变——一个可解释模型驱动的发现方法
author: Luc Blassel, Anna Tostevin, Christian Julian Villabona-Arenas, et al.
source: "https://thesis.lucblassel.com/HIV-paper.html"
reference: "Clippings/Chapter 6 Contribution 2 Inferring Mutation Roles From Sequence Alignments Using Machine Learning  From sequences to knowledge, improving and learning from sequence alignments.md"
date: 2026-04-28
tags:
  - 机器学习
  - HIV
  - 耐药突变
  - 生物信息学
published: 2021-08
journal: PLoS Computational Biology
doi: "10.1371/journal.pcbi.1008873"
---

## 核心内容总结
1. 用朴素贝叶斯、L1-正则化逻辑回归和随机森林三种可解释分类器，从 UK（n≈55,000）和非洲（n≈4,000）两大数据集区分治疗-初治 HIV 序列，发现了 **6 个新的潜在耐药相关突变**（L228R/L228H/E203K/D218E/I135L/H208Y）。
2. 这 6 个突变均为**辅助性或补偿性突变**——当移除已知耐药突变对应的特征后分类器仍保留预测能力，但移除含已知突变的所有序列后预测能力归零，说明它们本身不直接导致耐药。
3. 所有 6 个突变在 RT 的 3D 结构上均位于**活性位点或 NNIBP 调节口袋附近**，遗传屏障低（仅需 1 个碱基改变），与已知耐药突变高度共现（RR 值高达 **115.7x**）。
4. 实验表明存在更复杂的 epistasis（多个本身不耐药的突变组合产生耐药）的可能性**很低**——逻辑回归优于其他模型，且移除已知突变特征后的"Fisher 分类器"表现与 ML 分类器相当，说明单个突变的独立性解释已足够。
5. 按 HIV 亚型切分训练/测试集（B 型训练、C 型测试，反之亦然）有效规避了系统发育相关性造成的虚假信号。

## 关键数据
- 训练集：**55,539** 条 UK 序列（75% 初治），测试集：**3,990** 条非洲序列（58% 初治），UK 数据中 25% 的初治序列已携带至少 1 个已知耐药突变。
- 特征空间：**1,318** 个突变特征（二进制），其中 **121** 个对应已知耐药突变。
- L228R 的相对风险 RR(new,treatment) = **18.1** [95% CI: 12.9-27.3]，RR(new,any RAM) = **115.7** [55.1-507.3]。
- 非洲序列含耐药突变的中位数 RAM 数为 **3**，UK 仅为 **1**——非洲病毒的多药耐药更严重。
- 移除已知 RAM 特征后分类器在非洲测试集上保留显著预测能力（AMI 接近 1 个数量级高于 UK），因为非洲序列更难"伪装"成初治。

## 简述要点
传统上找到新的 HIV 耐药突变靠的是统计检验——对每个氨基酸位置逐个做 Fisher exact test，看突变频率在接受治疗和未接受治疗的患者间是否有显著差异。这个方法的致命弱点是**它只能看单个突变**。如果两个突变一起才产生耐药性，单独看一个的频率差异根本不够显著——多重检验校正后更是如此。

Blassel 等人想了一个很聪明的替代方案：不直接找突变，而是**训练分类器区分治疗和初治序列，然后从分类器里反推哪些突变最重要**。关键是选可解释的模型——朴素贝叶斯输出条件概率，L1-正则化逻辑回归输出非零权重，随机森林输出 Gini 重要性，每一种都能告诉你"哪些突变在驱动决策"。

最有意思的实验设计是**信号剥离**。第一轮用全部特征训练，分类器准确区分治疗和初治，验证了方法可行。第二轮移除 121 个已知耐药突变特征——分类器**仍然保留了预测能力**，说明数据中还有未知信号。第三轮更激进：不仅移除已知突变特征，还删除所有携带至少一个已知突变的序列——分类器**完全失去了预测能力**。

这个三重实验讲了一个完整的故事：所有直接导致耐药的突变（primary DRMs）可能都已被发现（放心），但还有不少**辅助和补偿性突变**附着在已知突变周围（有趣），而不存在复杂的 epistasis——即多个本身无耐药性的突变组合产生耐药（意外但合理）。

6 个新发现的突变在 RT 蛋白 3D 结构上都落到了关键区域附近——site 228（靠近活性位点和 NNIBP）、site 203/208（活性位点旁的 α-螺旋）、site 135（p51 亚基上靠近 NNIBP）、site 218（靠近活性位点）。这种结构层面的"合理性检验"增强了对发现可信度的信心。

## 疑点 / 待验证
- 6 个新突变均为辅助/补偿性突变，它们的具体生物学功能（是增强耐药程度还是补偿适应度损失）需要通过体外实验进一步验证。
- 研究使用了 OHE 编码，但近年来 learned embeddings（如蛋白语言模型）可能捕捉到更微妙的序列模式，两者结合是否能发现更隐蔽的 epistasis 值得探索。
- 药物类型的 granularity 有限——研究只能区分"是否接受过 RTI 治疗"，无法细分具体使用了哪种 RTI。

## 术语表
- **RAM (Resistance-Associated Mutation)**：耐药相关突变，比 DRM 更宽泛的概念，包括直接耐药突变、辅助突变和补偿突变
- **PRAM (Potentially Resistance-Associated Mutation)**：潜在耐药相关突变，指分类器发现的高重要性但尚未被斯坦福数据库收录的突变
- **Epistasis**：上位效应，指多个突变之间的相互作用，组合效应不等于个体效应的简单加和
- **Balanced Accuracy**：对不平衡数据集的修正准确率，分别计算每类准确率后取平均
- **AMI (Adjusted Mutual Information)**：调整互信息，衡量分类器预测标签与真实标签的一致性，校正了随机因素

## 原始来源
[[Clippings/Chapter 6 Contribution 2 Inferring Mutation Roles From Sequence Alignments Using Machine Learning  From sequences to knowledge, improving and learning from sequence alignments.md]]
