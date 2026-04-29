---
id: C-自注意力机制
title: 自注意力机制
reference: Clippings/第二章 Transformer 架构.md
updated: 2026-04-29
---

## 定义

自注意力机制（Self-Attention）是注意力机制的一种特殊形式，其 Query、Key、Value 均来自同一个输入序列通过不同的参数矩阵 $W_q$、$W_k$、$W_v$ 变换得到，用于建模序列内部每个 token 与其他所有 token 的相关关系。

## 关联来源

[[Clippings/第二章 Transformer 架构.md]]

## 已知边界 / 局限

- 计算复杂度为 $O(n^2)$（n 为序列长度），长序列场景下计算和内存开销显著，是后续 FlashAttention、稀疏注意力等优化的核心动机。
- 自注意力本身是**位置无关**的（permutation equivariant），需要配合位置编码才能区分 token 顺序。
- 单头自注意力只能捕捉一种相关关系模式，实际使用需通过多头机制来同时建模多种语义依赖。

## 实际案例

- **Transformer Encoder**：使用无掩码自注意力，每个 token 可关注序列中所有位置，实现双向上下文建模。
- **Transformer Decoder**：使用掩码自注意力（Masked Self-Attention），通过上三角掩码遮蔽未来 token，保证自回归生成的因果性。
- **BERT**：仅使用 Encoder 的自注意力机制做双向预训练。
- **GPT 系列**：仅使用 Decoder 的掩码自注意力做单向自回归预训练。
- **Vision Transformer (ViT)**：将图像切分为 patch 序列后应用自注意力，验证了该机制在 CV 领域的泛化能力。
