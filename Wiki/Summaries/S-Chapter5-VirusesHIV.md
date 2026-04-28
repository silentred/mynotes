---
id: S-Chapter5-VirusesHIV
title: 病毒、HIV 与耐药性：一个生物信息学背景概览
author: Luc Blassel
source: "https://thesis.lucblassel.com/viruses-hiv-and-drug-resistance.html"
reference: "Clippings/Chapter 5 Viruses, HIV and Drug Resistance  From sequences to knowledge, improving and learning from sequence alignments.md"
date: 2026-04-28
tags:
  - HIV
  - 药物耐药
  - 病毒学
---

## 核心内容总结
1. HIV 是全球最致命的流行病之一，至今已导致约 **3600 万**人死亡，但 ART 药物估计在 1995-2015 年挽救了 **950 万**条生命。
2. HIV 的高突变率（因逆转录酶缺乏校对机制）和基因重组能力使其在药物压力下快速产生耐药突变，这是耐药性研究的生物学基础。
3. 抗 HIV 药物主要靶向逆转录酶（RT）、蛋白酶（PR）和整合酶（IN）三个关键蛋白，其中 RT 被最多药物靶向，分为 NRTI 和 NNRTI 两类。
4. 耐药突变机制多样：有的阻止药物掺入（如 M184V 之于 3TC），有的能切除已掺入的药物（如 TAMs 之于 AZT），有的直接让药物结合口袋消失（如 K103N）。
5. 高收入国家可通过药物轮换（HAART）应对多药耐药，低收入国家因治疗方案单一导致多药耐药病毒流行，这是全球公共卫生的不平等缩影。

## 关键数据
- 截至 2010 年，全球约 **3300 万**人感染 HIV，其中 **70%** 新感染发生在撒哈拉以南非洲。
- HIV-1 源自黑猩猩的 SIV 跨物种传播，Group M（最流行群组）的共同祖先可追溯到 **1910-1931** 年间。
- 第一个抗 HIV 药物 AZT（齐多夫定）在 **1987** 年获 FDA 批准，仅 3 年后即出现耐药株。
- 截至 2022 年，FDA 批准了 **27** 种单药抗 HIV 药物，另有多种单药组合方案。
- HIV-1 目前有 **9** 个亚型（A-K）和 **118** 个已识别的循环重组型（CRF）。

## 简述要点
如果你想知道为什么 HIV 耐药性研究如此困难，答案其实藏在病毒自身的复制策略里。HIV 的逆转录酶（RT）在将病毒 RNA 转录为 DNA 时**没有校对机制**，导致每次复制都可能引入突变——这给了病毒在药物压力下快速探索"变异空间"的能力。再加上基因重组（当不同毒株共感染同一宿主时），HIV 几乎可以像一位高明的棋手，不断找到规避药物的走法。

对抗 HIV 的策略遵循一个清晰的逻辑：靶向病毒复制周期中的关键环节。RT 将 RNA 转为 DNA（步骤 3），整合酶将病毒 DNA 插入宿主基因组（步骤 4），蛋白酶切割多蛋白前体产生功能性蛋白（步骤 7）——每一个环节都是一个可靶向的弱点。NRTI 假装成核苷酸掺入 DNA 链使其终止，NNRTI 绑定到 NNIBP 口袋改变 RT 活性位点构象，蛋白酶抑制剂堵住切割通路的"隧道"。

但病毒的应对同样精彩。有的耐药突变（如 M184V）改变了 RT 活性位点的结构，使药物无法有效结合；有的（如 TAMs 系列）进化出了"切除"已掺入药物的能力；还有的（如 K103N）直接改变了 NNRTI 结合口袋的形状使其消失。这些机制在 **3D 蛋白结构层面**可以得到直观的解释，这也是为什么结构生物学是耐药研究不可或缺的一部分。

最令人深思的不是技术细节，而是公共卫生的不平等：高收入国家通过 HAART（多种药物联合使用）大幅降低了耐药风险，而非洲国家的治疗方案有限，药物轮换几乎不可行，导致多药耐药病毒的流行。这提醒我们，**耐药性问题不仅是分子生物学的挑战，更是一个资源配置的问题**。

## 疑点 / 待验证
- Asp 蛋白的存在和功能仍在学术争论中，它是否是 HIV-1 的第十个基因尚无定论。

## 术语表
- **ART (Anti-Retroviral Therapy)**：抗逆转录病毒治疗，通过靶向 HIV 复制周期各环节抑制病毒
- **HAART**：高活性抗逆转录病毒联合治疗，通常包含 2 NRTI + 1 其他类型药物
- **NRTI / NNRTI**：核苷类 / 非核苷类逆转录酶抑制剂，分别通过竞争性抑制和变构抑制阻断 RT
- **DRM (Drug Resistance Mutation)**：耐药突变，在药物选择压力下出现的使病毒逃避药物抑制的氨基酸替换
- **CRF (Circulating Recombinant Form)**：循环重组型，由不同亚型 HIV 在宿主体内重组形成的稳定毒株

## 原始来源
[[Clippings/Chapter 5 Viruses, HIV and Drug Resistance  From sequences to knowledge, improving and learning from sequence alignments.md]]
