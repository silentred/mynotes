---
id: S-Chapter1-WhatIsSequenceData
title: Chapter 1 What is Sequence Data ?
author: Luc Blassel
source: https://thesis.lucblassel.com/what-is-sequence-data.html
reference: Clippings/Chapter 1 What is Sequence Data ?  From sequences to knowledge, improving and learning from sequence alignments.md
date: 2026-04-26
tags:
  - 生物信息学
  - DNA测序
  - 计算生物学
---

## 核心内容总结

1. DNA 是由四种核苷酸（A/T/C/G）组成的多聚体，通过互补配对（A-T, C-G）形成双螺旋结构存储遗传信息；人类基因组约 31 亿碱基对，仅 1%-2% 为编码 DNA，其余大部分功能未知。
2. 遗传信息通过 DNA→RNA→蛋白质的中心法则转化为生命活动所需的蛋白质，64 个密码子对应 20 种氨基酸，遗传密码的冗余性为复制错误提供了一定的容错能力。
3. Sanger 测序（1977）通过双脱氧核苷酸链终止实现测序，是所有现代测序技术的理论基础；成本从每碱基 1000 美元降至 0.5 美元，通量从 1kb/天提升至 120kb/小时。
4. 长读长测序（PacBio SMRT 和 Oxford Nanopore）可产生 10kb-60kb reads，适合组装复杂基因组和串联重复区域，但准确率仅 85%-98%，显著低于 Sanger 的 99.999%。
5. 同聚物（连续相同碱基）是长读长测序的主要错误来源，通过同聚物压缩（HPC）将连续相同碱基缩减为单个碱基，可有效降低错误率，已在 HiCanu、minimap2 等主流工具中广泛使用。

## 关键数据

- **人类基因组**：31 亿碱基对（3.1GBp）
- **Sanger 测序成本**：从 $1000/碱基降至 $0.5/kb，通量达 120kb/小时，准确率 99.999%
- **PacBio 读长**：中位数 10kb，最高 60kb，通量 2-11Gb/小时，成本 $0.32/Mb，准确率 85%-92%
- **Nanopore 读长**：中位数 10-12kb，最高 2.3Mb，通量最高 260Gb/小时，成本 $0.13/Mb，准确率 87%-98%
- **人类基因组同聚物**：50% 的基因组位于长度≥2 的同聚物中，10% 位于长度≥4 的同聚物中，最长同聚物达 86 个碱基

## 简述要点

为什么需要理解生物序列数据？因为它是一切生命活动的底层编码——从 DNA 双螺旋结构到蛋白质功能，从基因突变到疾病关联，测序技术正在快速降低获取这种编码信息的门槛。

首先，DNA 通过四种核苷酸的排列组合存储遗传信息，双螺旋结构利用互补配对（A-T, C-G）确保信息可从任一条链恢复。人类基因组约 31 亿碱基，但其中编码蛋白质的 DNA 仅占 1%-2%，其余大部分仍是不知其功能的"暗物质"。遗传信息通过中心法则流向蛋白质：DNA 转录为 RNA，RNA 以三个碱基为一组（密码子）翻译为氨基酸序列，64 个密码子对应 20 种氨基酸——这种冗余性为复制错误提供了容错空间。

测序技术的演进从 Sanger 开始。1977 年 Sanger 等人发明链终止法，利用双脱氧核苷酸（ddNTP）随机终止 DNA 合成，通过电泳按长度分离产物并读取序列。这个方法奠定了现代测序的理论基础，后续改进包括荧光标记（淘汰放射性标记）、毛细管电泳（淘汰凝胶）和自动化流程。最新 Sanger 技术可达 1000bp 读长、99.999% 准确率，但成本仍需约 $500/Mb。

2000 年代兴起的第二代测序（NGS）以 Illumina 为代表，通过桥式扩增和荧光标记实现高通量，成本降至 $0.07/Mb，通量达 2.5-12.5Gb/小时，但读长仅约 150bp，在复杂基因组区域面前显得短促。第三代长读长测序解决了这个痛点：PacBio SMRT 利用零模波导（ZMW）实时检测荧光标记的核苷酸 incorporation，中位读长 10kb；Oxford Nanopore 直接让 DNA 单链穿过纳米孔，测量电流变化通过机器学习推断序列，理论上读长仅受分子长度限制，实际可达 2.3Mb。两种技术通量分别达 11Gb/小时和 260Gb/小时，但准确率只有 85%-98%，远低于短读长技术。

准确率问题主要来自同聚物区域——连续相同碱基是长读长的主要错误模式。PacBio 和 Nanopore 的插入缺失错误主要发生在 AAAA 或 TTTT 这类区域，而非随机分布。这是因为在同聚物中，测序信号难以区分"读了 5 次 A"还是"漏了 1 次 A"。同聚物在人类基因组中占比极大：50% 的序列位于长度≥2 的同聚物中，最长同聚物达 86 个碱基。

针对这个问题，同聚物压缩（HPC）作为一种预处理技巧被提出：将连续相同碱基缩减为单个碱基（如 AAACTGGG → ACTG）。这个方法在 HiCanu、wtdbg2、shasta 等组装工具中广泛使用，也在 minimap2、winnowmap2 的比对中使用。代价是丢失了同聚物长度的真实信息，但换取错误率的大幅下降被视为值得的权衡。

## 疑点 / 待验证

- 同聚物压缩丢失的长度信息在哪些下游分析中影响最大，是否有方法在保留信息的同时纠错？
- Nanopore 和 PacBio 在同聚物错误模式上的差异（ONT 错误率与同聚物长度无关，PacBio 错误率随长度上升）是否有更深层的信号处理原因？

## 术语表

- **核苷酸（Nucleotide）**：DNA 的基本单元，由核糖、磷酸基团和含氮碱基组成
- **密码子（Codon）**：RNA 上每三个连续核苷酸为一组，对应一个氨基酸
- **Sanger 测序**：1977 年发明的链终止法测序技术，是所有现代测序的理论基础
- **NGS（Next-Generation Sequencing）**：第二代测序，以 Illumina 为代表，高通量短读长
- **SMRT（Single Molecule Real-Time）**：PacBio 开发的长读长测序技术
- **ZMW（Zero-Mode Waveguide）**：100nm 直径的纳米孔，用于 SMRT 测序的实时荧光检测
- **同聚物（Homopolymer）**：连续相同碱基的序列，如 AAAA
- **HPC（Homopolymer Compression）**：同聚物压缩，将连续相同碱基缩减为单个碱基的预处理方法

## 原始来源

[[Clippings/Chapter 1 What is Sequence Data ?  From sequences to knowledge, improving and learning from sequence alignments.md]]
