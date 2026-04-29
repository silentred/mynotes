---
id: S-第二章-Transformer架构
title: Transformer 架构深度解析：从注意力机制到手搓完整模型
author: Datawhale
source: https://datawhalechina.github.io/happy-llm/#/./chapter2/%E7%AC%AC%E4%BA%8C%E7%AB%A0%20Transformer%E6%9E%B6%E6%9E%84
reference: Clippings/第二章 Transformer 架构.md
date: 2026-04-29
tags:
  - Transformer
  - 注意力机制
  - 深度学习
  - NLP
---

## 核心内容总结

- RNN/LSTM 虽擅长序列建模，但**无法并行计算**且**难以捕捉长距离依赖**，这两个硬伤直接催生了 Transformer。
- 注意力机制的核心公式是 $\text{attention}(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$，其中除以 $\sqrt{d_k}$ 是为了防止点积过大导致 softmax 梯度消失。
- 自注意力（Self-Attention）让 Q、K、V 来自同一输入，使每个 token 能直接建模与序列中所有其他 token 的关系——这是 Transformer 抛弃 RNN 后仍能理解上下文的根本原因。
- 多头注意力用多组参数矩阵并行计算多种注意力分布再拼接，让模型同时关注不同层次的语义关系，原论文实验也验证了不同头确实能学到不同模式。
- Encoder 用无掩码自注意力（双向），Decoder 用掩码自注意力（单向）加上交叉注意力（Q 来自 Decoder，K/V 来自 Encoder），这种设计让模型既能理解完整输入，又能逐 token 自回归生成输出。

## 关键数据

- Transformer 原论文中 Encoder 和 Decoder 各由 **6 层** Layer 堆叠而成。
- 位置编码使用 $\text{base}=10000$ 的正余弦函数，**偶数维度用 sin，奇数维度用 cos**，该选择来自实验验证。
- 位置编码的数学优美之处：$\langle p_m, p_n \rangle$ 仅依赖相对位置 $m-n$，这使得模型能泛化到训练时未见过的序列长度。

## 简述要点

RNN 统治 NLP 的时代有两个绕不开的硬伤：逐 token 串行计算让 GPU 并行能力形同虚设，长序列中远距离依赖关系的信号衰减也始终无法根治。Vaswani 等人的回答很直接——既然序列顺序是瓶颈，那就换一种机制来建模顺序。他们从 CV 领域借来注意力机制的思想，核心直觉很简单：**Query 和 Key 做点积得到相似度分数，用 softmax 归一化为权重，再对 Value 加权求和**。整个过程高度可并行，且任意两个位置的 token 之间的交互路径长度恒为 1，长距离依赖问题迎刃而解。

具体到工程实现，文章用从零逐行写代码的方式把每个组件拆解得非常清晰。自注意力让 Q=K=V 来自同一输入，掩码自注意力通过上三角 `-inf` 矩阵遮蔽未来 token 实现因果约束，多头注意力则是用一个组合大矩阵替代 n 组小矩阵（矩阵内积再拼接等价于拼接矩阵再内积）来高效并行。Encoder 端是双向自注意力 + 前馈网络，Decoder 端多了一层交叉注意力层（用 Encoder 输出作为 K/V）。位置编码选择正余弦函数而非可学习参数，核心原因是其内积天然表达相对位置关系，**数学推导证明了 $\langle p_m, p_n \rangle = g(m-n)$**。

从零实现一个完整 Transformer 大约需要 10 个左右的 Python 类，代码量不算大但信息密度高。文章还特别指出一个实现细节：原论文配图是 Post-Norm（LayerNorm 在 Attention 后），但**现代 LLM 普遍采用 Pre-Norm（LayerNorm 在 Attention 前）**，因为后者训练更稳定。

## 疑点 / 待验证

- 文中提到位置编码 base=10000 是"实验结果"，但未给出消融实验的具体数据，这个值对更长序列的适应性边界在哪里尚待验证。
- Pre-Norm vs Post-Norm 的优劣讨论仅点到为止，更深入的梯度流动分析需要参考其他文献。

## 术语表

- **自注意力（Self-Attention）**：Q、K、V 来自同一输入的注意力变体，用于建模序列内部 token 间关系
- **掩码自注意力（Masked Self-Attention）**：通过上三角掩码屏蔽未来 token 的自注意力，保证自回归生成时不泄露未来信息
- **多头注意力（Multi-Head Attention）**：并行计算多组注意力后拼接，每组使用不同的 $W_q$、$W_k$、$W_v$ 参数矩阵
- **层归一化（Layer Norm）**：对每个样本所有维度做归一化，比 Batch Norm 更稳定，不受 batch size 影响
- **位置编码（Positional Encoding）**：用正余弦函数为每个位置生成唯一向量，加到词向量上以注入顺序信息
- **残差连接（Residual Connection）**：$output = x + F(\text{LayerNorm}(x))$，让底层信息直通高层，缓解深层网络退化

## 原始来源

[[Clippings/第二章 Transformer 架构.md]]
