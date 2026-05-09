---
id: C-预训练语言模型
title: 预训练语言模型
reference: Clippings/第二章 Transformer 架构.md
updated: 2026-04-29
---

## 定义

预训练语言模型（Pre-trained Language Model, PLM）是在大规模无标注语料上通过自监督任务（如语言模型、掩码预测）预训练，再针对下游任务微调的 NLP 范式。ELMo 确立范式雏形，BERT 将其推向高潮，GPT 系列则从 Decoder-Only 路线演进为 LLM 基座。

## 关联来源

[[Clippings/第二章 Transformer 架构.md]]

[[Clippings/第三章 预训练语言模型.md]]

## 已知边界 / 局限

- Encoder-Only（BERT）擅长 NLU（分类、序列标注），但不适合生成任务
- Decoder-Only（GPT）通过因果掩码保序生成，但无法使用双向上下文理解
- 预训练-微调范式在 LLM 时代逐渐被上下文学习（In-Context Learning）和指令微调替代
- BERT 的 MLM 预训练需要特殊标记 [MASK]，造成预训练-微调不一致

## 实际案例

- **BERT（Google, 2018）**：Encoder-Only，12/24 层 Encoder，MLM + NSP 预训练，GLUE/SQuAD SOTA
- **GPT 系列（OpenAI）**：Decoder-Only，自回归 LM 预训练，参数量从 110M 增至 175B+（GPT-3），终成 LLM 基座
- **T5（Google, 2019）**：Encoder-Decoder，Text-to-Text 统一格式，所有 NLP 任务统一为输入/输出文本
- **ElMo（2018）**：双向 LSTM + 语言模型预训练，开创预训练-微调范式但架构落后于 Transformer
