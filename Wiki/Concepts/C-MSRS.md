---
id: C-MSRS
title: 映射友好序列约减（MSR）
reference: Clippings/Chapter 3 Contribution 1 Improving Read Alignment by Exploring a Sequence Transformation Space  From sequences to knowledge, improving and learning from sequence alignments.md
updated: 2026-04-26
---

## 定义

MSR（Mapping-friendly Sequence Reductions，映射友好序列约减）是一种序列预处理框架，通过在比对前对 reads 和参考序列施加确定性的流式变换，使长读长测序错误（特别是同聚物插入缺失）对比对的影响最小化。MSR 是同聚物压缩（HPC）的严格推广——通过将 HPC 形式化为滑动窗口 ℓ=2 的 g 函数，可以探索更广的变换空间，找到比 HPC 表现更优的序列约减函数。

## 关联来源

[[Clippings/Chapter 3 Contribution 1 Improving Read Alignment by Exploring a Sequence Transformation Space  From sequences to knowledge, improving and learning from sequence alignments.md]]

## 已知边界 / 局限

- **适用场景**：长读长（PacBio/Nanopore）的 read-mapping 预处理；整个人类基因组、果蝇等真核生物基因组的比对
- **不适用场景**：高度重复的着丝粒/端粒区域（MSR 和 HPC 均不如 raw reads）；对高阶（ℓ>2）MSR 的穷举搜索仍不可行

## 实际案例

- **MSR_E**：最低 mapping error rate at 最高 mapq threshold，输出以 T 为主
- **MSR_F**：最高 mapped reads 比例 at mapq=0，AA→T, AC→T, AG→A, CA→A, CC→T, GA→G
- **MSR_P**：最高比例的 mapq 阈值优于 HPC at mapq=60，几乎只输出 A/T
