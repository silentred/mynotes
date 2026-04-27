---
id: C-动态规划序列比对
title: 动态规划序列比对
reference: Clippings/Chapter 2 Aligning Sequence Data  From sequences to knowledge, improving and learning from sequence alignments.md
updated: 2026-04-26
---

## 定义

动态规划序列比对（Dynamic Programming Sequence Alignment）是将动态规划应用于两条生物序列的比对问题，通过构建打分矩阵并在矩阵中寻找最优路径，找到最小编辑距离或最大比对得分的序列对齐方式。NW 算法实现全局比对（对齐两序列全长），SW 算法通过非负约束实现局部比对（对齐最高相似的子序列），两者本质相同但回溯起点不同。

## 关联来源

[[Clippings/Chapter 2 Aligning Sequence Data  From sequences to knowledge, improving and learning from sequence alignments.md]]

## 已知边界 / 局限

- **适用场景**：两条短序列的精确最优比对（当需要保证最优解时）；作为种子扩展策略中的 extend 步骤
- **不适用场景**：两条人类基因组级别的序列（需要 10¹⁹ 矩阵单元格，约 10EB 存储）；大量序列的批量比对（NGS 时代的大规模 read-mapping）；需要启发式近似解的大规模搜索

## 实际案例

- 两条 1000bp 序列的全局比对：NW 矩阵 1000×1000，时间 O(nm)
- Myers-Miller 算法（改良 NW）：以分治策略将空间复杂度从 O(nm) 降至 O(n+m)，在 EMBOSS `stretcher` 中实现
- BLAST 的 extend 步骤：用 SW 算法从种子向两侧扩展验证
