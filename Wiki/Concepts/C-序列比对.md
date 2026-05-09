---
id: C-序列比对
title: 序列比对
reference: Clippings/Chapter 1 What is Sequence Data ?.md
updated: 2026-04-26
---

## 定义

序列比对（Sequence Alignment）是将两个或多个生物序列（DNA/RNA/蛋白质）按位置对应排列，使同源区域对齐以便比较的技术。它是生物信息学的核心方法，广泛应用于进化分析、功能预测、耐药性研究等领域。

## 关联来源

[[Clippings/Chapter 1 What is Sequence Data ?.md]]

## 已知边界 / 局限

- 比对质量决定下游分析（系统发育、变异检测、ML 建模）的可靠性
- 传统比对算法依赖固定规则（动态规划、种子-扩展），在面对高变异区域时准确率下降
- 读段比对的精确性受限于测序读长和参考基因组完整性

## 实际案例

- **HIV 耐药性研究**（Luc Blassel PhD）：通过对 HIV 病毒序列的比对，使用机器学习推断每个突变的功能角色——区分耐药性突变与背景突变，将传统比对结果作为 ML 的输入特征
- **读段比对改进**（Contribution 1）：通过探索序列转换空间（sequence transformation space）提高读段比对对插入、删除、替换等操作的敏感度
- **对齐学习**：用机器学习方法学习序列如何对齐本身，超越动态规划的固定规则，是生物信息学的前沿方向
