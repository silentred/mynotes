---
id: C-AI原生数据库
title: AI 原生数据库
updated: 2026-04-08
---

## 定义

AI 原生数据库（AI-Native Database）是将 AI 推理能力深度嵌入数据存储层的新一代数据库架构，与传统的 AI 增强（AI on DB，将向量检索插件叠加到传统数据库）不同，AI 原生数据库从设计层面将 AI 视为一等公民，追求混合搜索、AI Function（AI 直接操作数据库）和 Document In Data Out（文档直接入、AI 直接吐出完整答案）的能力。

## 关联来源

[[Clippings/AI原生数据库的思考.md]]

## 已知边界 / 局限

- **RAG vs AI 原生 DB 的本质区别**：RAG 的知识在上下文窗口中（每次重新发现），AI 原生 DB 的知识在数据库中（重复使用）；前者适合快速问答，后者适合深度研究
- **混合搜索的实现复杂度**：RRF（Reciprocal Rank Fusion）融合多路召回结果，但不同召回路线的相关性打分体系不一致时融合效果难以保证
- **AI Function 的安全和成本问题**：让 AI 直接执行数据库操作（SELECT/INSERT）存在注入风险和成本失控可能，需要严格的安全边界和成本控制

## 版本 / 演进

- **传统数据库 + 向量插件**（pgvector、MySQL Vector）：在现有关系型数据库上扩展向量索引，架构简单但非 AI 原生设计
- **向量数据库**（Pinecone、Milvus、Qdrant）：专为向量检索设计，高效但仅限于向量能力
- **AI 原生混合搜索数据库**（OceanBase seekdb 等）：将向量检索、全文检索、BM25 等多路召回统一在数据库层，结合 RRF 和 LLM 重排
