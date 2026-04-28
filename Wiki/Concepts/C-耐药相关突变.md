---
id: C-耐药相关突变
title: 耐药相关突变（Resistance-Associated Mutations, RAMs）
reference: "Clippings/Chapter 6 Contribution 2 Inferring Mutation Roles From Sequence Alignments Using Machine Learning  From sequences to knowledge, improving and learning from sequence alignments.md"
updated: 2026-04-28
---

## 定义

耐药相关突变（RAMs）是比耐药突变（DRMs）更宽泛的概念，指在药物选择压力下出现的、与耐药性存在统计关联的氨基酸替换。它包括三类：
1. **主要耐药突变（Primary DRMs）**——直接导致药物靶点改变、使药物失效的突变；
2. **辅助突变（Accessory mutations）**——增强主要突变耐药效果的突变；
3. **补偿突变（Compensatory mutations）**——修复耐药突变带来的适应度损失但不直接参与耐药的突变。

## 关联来源

[[Clippings/Chapter 6 Contribution 2 Inferring Mutation Roles From Sequence Alignments Using Machine Learning  From sequences to knowledge, improving and learning from sequence alignments.md]]
[[Clippings/Chapter 5 Viruses, HIV and Drug Resistance  From sequences to knowledge, improving and learning from sequence alignments.md]]

## 已知边界 / 局限

- 统计关联不等于因果关系：RAMs 的发现基于治疗 vs 初治序列的频率差异，不能直接证明该突变在表型层面导致耐药——需要通过体外实验或临床验证确认。
- 系统发育相关性是虚假信号的主要来源：同一谱系中的序列共享祖先突变（而非独立获得），简单的频率比较会高估突变与耐药的关联。需要按亚型/进化支分层，或在不同流行病学背景的独立数据集中验证。
- **Epistasis 盲区**：如果耐药需要两个突变的组合但每个单独突变没有耐药效果，基于单个突变频率的方法（无论是统计检验还是可解释 ML 的特征重要性）都可能漏掉。
- RAM 分类的时序性：辅助/补偿突变的判定依赖于已知主要 DRMs 的存在——如果新发现的主要 DRMs 被加入列表，某些"辅助"突变可能需要重新分类。

## 实际案例

- Blassel 等通过训练三类可解释分类器（NB/LR/RF）从 UK 约 55,000 条 HIV RT 序列中发现了 6 个潜在 RAMs（L228R, L228H, E203K, D218E, I135L, H208Y），通过"信号剥离实验"确定了它们均为辅助/补偿性突变而非 primary DRMs。
- 斯坦福 HIV 耐药数据库（Stanford HIVDB）维护了已知 DRMs 列表，临床上的基因型耐药检测（如 Geno2pheno）依赖这些列表来解释患者的病毒序列。
- NRTI 和 NNRTI 耐药突变的耐药机制不同：NRTI 突变（如 M184V）通过改变活性位点阻止药物掺入，NNRTI 突变（如 K103N）通过改变 NNIBP 构象使药物无法结合。
