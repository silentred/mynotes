---
id: S-Chapter2-AligningSequenceData
title: Chapter 2 Aligning Sequence Data
author: Luc Blassel
source: https://thesis.lucblassel.com/aligning-sequence-data.html
reference: Clippings/Chapter 2 Aligning Sequence Data  From sequences to knowledge, improving and learning from sequence alignments.md
date: 2026-04-26
tags:
  - 生物信息学
  - 序列比对
  - 计算生物学
---

## 核心内容总结

1. 序列比对（Alignment）通过插入空位（gap）处理插入缺失（indel），比 Hamming 距离更适合生物学序列比较；是比较基因组学、蛋白结构预测、变异检测等下游分析的基础。
2. Needleman-Wünsch（NW）算法以动态规划实现全局比对，时间空间复杂度均为 O(nm)；Smith-Waterman（SW）算法在此基础上加入非负约束实现局部比对，两者本质相同但应用场景不同。
3. 打分矩阵将生物学知识编码进比对：PAM 基于近缘序列突变计数，BLOSUM62 基于 62% 相似度保守区块，均以 Log-odds 形式计算替换得分。
4. 间隙罚分从简单线性罚分演化为仿射罚分（gap open + gap extend），Gotoh 算法将复杂度保持在 O(nm)；最新 WFA 算法将复杂度降至 O(ns)，比传统方法快 10-300 倍。
5. 实用比对工具均采用启发式"种子延伸"策略：BLAST 以 k-mer 哈希找种子再扩展；minimap2 以 minimizer 稀疏采样减少存储；BWA 以 FM-index 实现内存高效索引。

## 关键数据

- **BLAST** 论文引用超过 10 万次，是最广泛使用的序列比对工具
- **WFA 算法**比传统动态规划快 10-300 倍，复杂度 O(ns)，s 为比对得分
- **minimap2** 使用 (w,k) minimizer 策略：窗口 w 内选择最小的 k-mer 存入哈希表，相邻窗口共享 minimizer 的特性保证如果两序列有 w-k+1 公共子串，则必然共享一个 minimizer
- **Mapping quality**：-10log₁₀(p)，p 为错配概率；bowtie2 最大值 42，BWA 37，minimap2 60
- 多序列比对（MSA）是 NP-hard 问题，精确算法指数级时间空间复杂度，渐进式比对（progressive alignment）是主流启发式方案

## 简述要点

为什么要做序列比对？因为生物序列的相似性蕴含着进化和功能信息——两条序列能否对齐、怎么对齐，决定了我们能否推断物种间的亲缘关系、预测蛋白质结构、检测基因组变异。而 Hamming 距离只适合比较等长且无插入缺失的序列，对生物序列几乎无用。

生物序列比对的核心问题是如何处理插入缺失（indel）。以 `ATGTGCAGTA` 和 `AGTGCAGTAC` 为例，逐字符比较几乎全错，但如果假设第一个 T 被删除、末尾插入了 C，两条序列就能完美对齐。这引入了"空位"（gap）的概念，使得序列比对问题等价于字符串编辑距离。

Needleman-Wünsch（NW）算法和 Smith-Waterman（SW）算法是两条序列比对的理论基础。两个算法都利用动态规划构建打分矩阵：NW 在整个矩阵中寻找最高打分的对齐路径，实现全局比对；SW 在此基础上加入非负约束，从最高分单元格回溯至零分，实现局部比对——在两条远缘物种基因组中寻找高度保守的区域。两种算法时间空间复杂度均为 O(nm)，对两条人类基因组比对需要约 10¹⁹ 个矩阵单元格，存储空间达 10 EB（数据中心级别）。Hirschberg 通过分治策略将空间复杂度降至 O(n+m)，诞生了 Myers-Miller 算法。

打分的生物学化是另一个关键进步。简单 match=+1/mismatch=-1 没有利用任何生物学知识。PAM 矩阵基于 71 个近缘蛋白家族构建，通过统计accepted mutation（被自然选择接受的突变）推算突变概率矩阵；BLOSUM62 则基于 62% 相似度的保守区块直接统计氨基酸配对出现频率。两种矩阵都以 Log-odds 形式 S_{i,j}=log(q_{ij}/p_ip_j) 计算——q_{ij} 是实际观察到的对齐概率，p_ip_j 是随机对齐的期望概率，比值大于 1 说明该替换常见且可能由进化选择保留。

空位罚分同样经历演进。线性空位罚分（每个 indel 都是 -1）不符合生物学现实——indel 通常涉及多个核苷酸。Gotoh 于 1982 年提出仿射空位罚分：gap open 单独计一次高成本，gap extend 计低成本的延伸罚分，鼓励长间隙替代多段短 indel，同时将复杂度保持在 O(nm)。

然而即使用了仿射空位罚分，动态规划对大规模序列仍太慢。1977 年提出的 BLAST 是最早广泛使用的启发式比对工具：预计算 query 和 target 的 k-mer 哈希表，查找命中后以 SW 算法向两侧扩展，设定阈值过滤低分候选。BLAST 至今仍是 NCBI 的核心服务，处理数亿条 target 序列。

为了减少哈希表存储开销，minimizer 策略被提出：窗口 w 内的所有 k-mer 只选"最小"（按特定排序）的存入哈希表。相邻窗口大概率共享同一个 minimizer，保证如果两序列有公共子串则必然共享 minimizer——这使得哈希表大幅稀疏化。minimap2、winnowmap2 都使用这一策略。Winnowmap 还对高频 k-mer 降权，以应对重复序列区域的比对。

Read-mapping 是序列比对在组学分析中的具体应用：把测序 read 比对到参考基因组上。挑战来自两方面——测序错误（长读长错误率 85%-98%）和基因组本身的重复区域（着丝粒、端粒等）。同聚物压缩作为预处理可缓解长读长的同聚物错误。Mapping quality 用来量化比对的可信度，但不同工具的定义差异很大。

多序列比对（MSA）问题本身是 NP-hard，无法求得精确解。渐进式比对（progressive alignment）是主流方案：先建引导树（guide tree），然后从叶到根逐层两两比对/合并 profiles。CLUSTAL、MAFFT、T-Coffee、MUSCLE 等主流工具都采用这一框架或其变体。"once a gap, always a gap"——早期比对的错误会级联传播，迭代细化（iterative refinement）作为补救。

## 疑点 / 待验证

- 在大规模基因组比较中，BLOSUM 和 PAM 矩阵的选择对结果影响有多大，是否有系统性的benchmark？
- WFA 算法虽然快 10-300 倍，但在什么场景下精度损失最显著，是否适合作为 read-mapping 的核心引擎？

## 术语表

- **Gap（空位）**：序列比对中为处理插入缺失而插入的空字符
- **Indel（插入缺失）**：插入或删除事件的统称，会导致序列相对位移
- **NW 算法（Needleman-Wünsch）**：基于动态规划的全局比对算法，1970 年提出
- **SW 算法（Smith-Waterman）**：基于动态规划的局部比对算法，1981 年提出
- **PAM 矩阵**：基于 point accepted mutation 统计的氨基酸替换矩阵，数值代表进化距离（如 PAM250 适合远缘蛋白）
- **BLOSUM 矩阵**：基于保守区块实际对齐频率的氨基酸替换矩阵，数值代表序列相似度（如 BLOSUM62 适合 62% 相似度）
- **仿射空位罚分（Affine Gap Penalty）**：gap open + gap extend 分别计分的空位罚分模型
- **Seed and Extend**：先以索引结构快速找到候选匹配区域（seed），再用动态规划扩展验证的比对策略
- **Minimizer**：窗口 w 内按特定排序选取的最小 k-mer，用于稀疏化哈希索引
- **Mapping Quality**：-10log₁₀(p)，量化 read 比对到参考基因组位置的可信度

## 原始来源

[[Clippings/Chapter 2 Aligning Sequence Data  From sequences to knowledge, improving and learning from sequence alignments.md]]
