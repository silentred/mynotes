---
id: S-第三章-预训练语言模型
title: 预训练语言模型：BERT、T5、GPT 与 LLaMA
author: Datawhale（Happy LLM 系列）
source: https://datawhalechina.github.io/happy-llm/#/./chapter3/%E7%AC%AC%E4%B8%89%E7%AB%A0%20%E9%A2%84%E8%AE%AD%E7%BB%83%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B
reference: Clippings/第三章 预训练语言模型.md
date: 2026-05-09
tags:
  - LLM
  - BERT
  - GPT
  - T5
  - Transformer
---

## 核心内容总结

1. Transformer 之后 NLP 预训练分三条路线：Encoder-Only（BERT）以 MLM 理解双向语义，Decoder-Only（GPT）以 CLM 自回归生成，Encoder-Decoder（T5）以 Text-to-Text 统一所有任务。
2. Encoder-Only 路线以 BERT 为首，MLM + NSP 预训练在 NLU 任务上达到 SOTA；后续优化包括 RoBERTa（去 NSP + 更大规模）和 ALBERT（参数分解共享 + SOP 替代 NSP）。
3. Encoder-Decoder 路线代表 T5，核心创新：将所有 NLP 任务统一为 Text-to-Text 格式，Span Corruption 预训练任务替代 MLM。
4. Decoder-Only 路线从 GPT-1（117M）→ GPT-2（1.5B）→ GPT-3（175B）规模狂飙，最终以涌现能力开启 LLM 时代；LLaMA 以更多 token 训练小模型实现同等性能，颠覆"越大越好"认知。

## 关键数据

- **BERT base/large**：110M / 340M 参数
- **GPT 系列**：GPT-1 117M → GPT-2 1.5B → GPT-3 **175B**
- **GLUE 基准**：BERT 得分 80.5 → RoBERTa 88.5
- **SQuAD 2.0**：BERT 80.0 → RoBERTa 86.5 → ALBERT 89.5（单模型）
- **LLaMA-13B**：在大多数基准上超越 GPT-3 175B

## 简述要点

预训练语言模型（PLM）继承了 ELMo 的预训练+微调范式，将 Transformer 架构推向三条路线。Encoder-Only 以 BERT 为代表，通过 MLM（随机遮盖 token 预测）利用双向上下文捕获深层语义，适用于文本分类、序列标注等 NLU 任务。RoBERTa 通过去除 NSP、增大数据和步长、更大 BPE 词表显著提升性能；ALBERT 以参数分解和跨层共享大幅减少参数量。Encoder-Decoder 路线的 T5 将所有任务统一为输入文本→输出文本格式，以 Span Corruption 预训练任务覆盖更广场景。Decoder-Only 路线的 GPT 以自回归 CLM 预训练奠定生成能力，到 GPT-3 涌现上下文学习能力。LLaMA 的核心洞察是"更多 token 训练更小模型"——用 1T+ token 训练 13B 参数即可匹配 175B 的性能，改变了规模竞争的范式。

## 疑点 / 待验证

- ALBERT 的 SOP 任务是否已完全解决 BERT 的 NSP 缺陷，还是场景限制仍然存在
- Decoder-Only 路线最终在 LLM 时代的全面胜出是否源于预训练任务（CLM vs MLM）的本质差异

## 术语表

- **Encoder-Only PLM**：仅使用 Transformer Encoder 的预训练模型，代表 BERT；以 MLM 预训练，适合 NLU 任务
- **MLM（Masked Language Model）**：随机遮盖输入 token 让模型预测被遮词，使模型学习双向上下文语义
- **NSP（Next Sentence Prediction）**：BERT 的辅助预训练任务，预测两段文本是否为连续句子
- **Encoder-Decoder PLM**：同时保留 Encoder 和 Decoder 的预训练模型，代表 T5；统一所有任务为 Text-to-Text 格式
- **Span Corruption**：T5 的预训练任务，随机遮盖连续 token 片段让模型恢复
- **Decoder-Only PLM**：仅使用 Transformer Decoder 的预训练模型，代表 GPT；以 CLM 预训练，适合 NLG
- **CLM（Causal Language Model）**：自回归因果语言模型，每个 token 仅能依赖左侧上下文

## 原始来源

[[Clippings/第三章 预训练语言模型.md]]
