---
id: S-Chapter7-LearningAlignments
title: 让深度学习学习序列比对：从 word2vec 到 Transformer 的生物信息学应用
author: Luc Blassel
source: "https://thesis.lucblassel.com/learning-alignments-an-interesting-perspective.html"
reference: "Clippings/Chapter 7 Learning Alignments, an Interesting Perspective  From sequences to knowledge, improving and learning from sequence alignments.md"
date: 2026-04-28
tags:
  - 深度学习
  - 序列比对
  - Transformer
  - 生物信息学
---

## 核心内容总结
1. 从 NLP 迁移到生物信息学的学习式嵌入（word2vec→dna2vec/protVec→BERT→ProtBERT）实现了对生物序列的低维语义表示，解决了 One-Hot 编码维度爆炸的问题。
2. Transformer 的 self-attention 机制通过加权聚合所有 token 的上下文信息来学习长程依赖，但**二次复杂度**在蛋白质/DNA 长度下成为关键瓶颈。
3. 学习序列比对有两种路线：**预测替换矩阵**（如 DEDAL 用 Transformer + 可微 SW 算法在远程同源比对上超过传统方法）和**直接预测比对**（如 BetaAlign 把比对视为序列翻译问题）。
4. 在读长比对场景中，学习式方法的主要应用是学习数据结构索引（如 BWA-MEME 学习预测后缀数组位置）和 minimizer 选择方案（如 DeepMinimizer 学习最优密度分布）。
5. AlphaFold2 中的 EvoFormer 模块证明了 MSA 嵌入 + 注意力机制的强大组合，这是"用学习对齐提升下游任务"目前最成功的案例。

## 关键数据
- 英语词典 **47 万**个词，用 OHE 编码一个词需要 47 万维稀疏向量——这正是 NLP 推动 embedding 技术发展的驱动力。
- DEDAL 同时在 **3 个任务**上训练：MLM（UniRef50 3000 万序列）、同源检测（Pfam-A 120 万序列）、比对任务（可微 SW），在远程同源对齐上显著优于传统方法。
- 蛋白语言模型（如 ProtBERT）的参数量达到**百万到亿**级别，GPT-3 更是达到 **1750 亿**参数。
- BetaAlign 在约 **40** 个残基长度的短序列上超过了 MUSCLE、CLUSTALW，但在 500-1000 残基长序列上性能仅与传统方法持平。

## 简述要点
如果我们接受一个前提——序列比对本质上是找到两个序列之间的最优对应关系——那么这个问题和机器翻译惊人地相似：从源语言"翻译"到目标语言。本章正是沿着这个类比展开的。

从 word2vec（把单词嵌入到语义相关的低维向量空间）到 dna2vec（把 k-mer 做同样的事），生物信息学一直跟随着 NLP 的脚印。真正的转折点是 Transformer：self-attention 机制不再像 RNN 那样只能看到局部的上下文，而是对所有位置的 token 做加权求和——这意味着一个位置的表示可以从整个序列的任何一个位置"借信息"。AlphaFold2 的 EvoFormer 正是利用这一点，在 MSA 上做跨序列的注意力，从而捕捉到了进化共变信号。

但 Transformer 的 self-attention 有个不可忽视的代价：时间和空间复杂度对序列长度是**二次的**。一个典型的蛋白质序列可能 500 残基，一个人类基因组是 30 亿碱基对——直接把基因组塞进 Transformer 是不可行的。这也是为什么目前的学习式比对方法都限制在短序列或特定场景（如蛋白结构预测中只需要对 MSA 做注意力，而 MSA 的序列数量通常远小于比对的长度）。

说回"学习比对"这件事。实践中出现了两条路线。**路线一**（预测替换矩阵）：用神经网络预测位置特异性打分矩阵（PSSM），然后把这个矩阵喂给经典比对算法（NW 或 SW）。DEDAL 是这条路线的最佳代表——它的 Transformer 编码器为每对残基预测匹配/开放空位/延伸空位的得分，然后用可微的 SW 算法做端到端训练。结果它在**远程同源**比对（序列相似度很低但仍有关联）上显著优于所有传统方法。**路线二**（直接预测比对）：把比对看作直接的序列到序列变换，用 Transformer 的编码器-解码器架构直接输出对齐结果。BetaAlign 在短序列上证明了可行性，但在长序列上受限于注意力机制的复杂度。

对于读长比对（reads mapping），情况更加复杂——参考序列和读段之间的长度差异巨大。这里的实用突破来自**学习式索引**：BWA-MEME 用学习的模型替代传统后缀数组的部分内容，Sapling 用同样的思路加速了后缀数组查询。还有 DeepMinimizer 用神经网络学习选择均匀分布的 minimizer——这直接减少了种子索引的内存和时间开销。

## 疑点 / 待验证
- 对于超长序列（>1000 残基），目前所有的 learned alignment 方法都面临注意力瓶颈，Performer/Linformer 等线性注意力变体在比对任务上的效果尚未验证。
- 可微比对框架是否能真正学到"正确"的进化模型还是只是拟合训练集上的结构比对，仍有争议。
- 学习式索引在读长比对中的优势已在细菌基因组上展现，但在更大规模的参考基因组（如人类）上的扩展性待确认。

## 术语表
- **Self-Attention**：Transformer 核心机制，每个 token 的表示是所有 token 的加权和，权重由训练学习
- **PSSM (Position-Specific Scoring Matrix)**：位置特异评分矩阵，为每个位置的每对残基分配比对得分
- **MLM (Masked Language Modeling)**：随机遮挡部分 token 让模型预测被遮挡内容，是 BERT 类模型的预训练范式
- **Learned Index**：用学习模型替代传统数据结构输出，如 BWA-MEME 用模型预测后缀数组位置
- **End-to-End Learning**：将整个流程联合优化，以最终任务的损失反向传播到所有模块

## 原始来源
[[Clippings/Chapter 7 Learning Alignments, an Interesting Perspective  From sequences to knowledge, improving and learning from sequence alignments.md]]
