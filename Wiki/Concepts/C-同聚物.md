---
id: C-同聚物
title: 同聚物（Homopolymer）
reference: Clippings/Chapter 1 What is Sequence Data ?  From sequences to knowledge, improving and learning from sequence alignments.md
updated: 2026-04-26
---

## 定义

同聚物是由连续相同碱基组成的 DNA 序列片段（长度≥2），如 AAAA（长度 4 的腺嘌呤同聚物）。在计算生物学中，同聚物错误是长读长测序技术（PacBio 和 Nanopore）的主要测序错误模式——插入或缺失错误主要发生在同聚物区域，导致"读多了"或"漏读了"某个碱基。

## 关联来源

[[Clippings/Chapter 1 What is Sequence Data ?  From sequences to knowledge, improving and learning from sequence alignments.md]]

## 已知边界 / 局限

- **适用场景**：PacBio SMRT 和 Oxford Nanopore 长读长测序的错误分析、同聚物压缩（HPC）算法的应用场景
- **不适用场景**：Sanger 测序和 Illumina 等短读长技术不受同聚物问题显著影响（因读长短、准确率高）；同聚物压缩会丢失真实的同聚物长度信息，不适合需要精确长度数据的分析场景

## 实际案例

- 人类基因组 T2T-CHM13 v1.1 中，50% 的基因组位于长度≥2 的同聚物中，最长同聚物达 86 个碱基
- HiCanu、wtdbg2、shasta 等组装工具内置 HPC 预处理；minimap2、winnowmap2 在比对时使用 HPC
- Nanopore 的错误率与同聚物长度无关，而 PacBio 和短读长技术的错误率随同聚物长度上升
