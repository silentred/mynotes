---
id: S-AI原生数据库的思考
title: AI 原生混合搜索与 seekdb：OceanBase 的 AI 数据库战略
author: 杨传辉
source: https://mp.weixin.qq.com/s/mR_hVCVszx2EONfj9o2ihw
date: 2026-04-05
tags:
  - AI
  - database
---

## 核心结论

1. AI 场景驱动数据库新工作负载：**面向 Agent 的多模混合搜索**——需同时支持结构化（关系）、半结构化（JSON）和无结构化（向量、全文、图）数据，通过 RRF 加权融合、模型重排序（Rerank）实现精准召回。
2. AI 数据库的演进路径：从 **AI Ready**（关系库 + 向量插件）到 **AI Native**（数据库内嵌 AI Function，SQL 直调 Embedding/Rerank/LLM），数据与模型深度融合才是终态。
3. OceanBase seekdb 定位：**面向开发者的轻量 AI 原生数据库**，1C2G 起步配置，一套引擎支持关系 + JSON + 向量 + 全文混合搜索，已开源（Apache 2.0）。

## 关键数据

- 混合搜索多路召回：全文 + 稀疏向量 + 稠密向量融合，实验表明三者结合召回率最高
- seekdb 起步配置：**1C2G**，目标是优化到 500MB 内存
- 向量数据库竞品：Milvus/Pinecone/Qdrant 全局搜索强但缺乏 SQL/Join 能力；ES 全文强但向量弱
- 召回结果融合算法：RRF（Reciprocal Rank Fusion）对各路排名取倒数求和，无需调参；加权融合可配置权重；模型融合（BGE-reranker、Qwen-rerank）效果最好
- 多租户挑战：海量 Agent 即海量租户，需要 schema 管理优化（OceanBase 单集群支持的表格数提升 1-2 个数量级）

## 疑点 / 待验证

- 向量搜索与全文搜索的融合效果在不同数据分布下的最优权重配置尚无定论，需结合业务数据调优。
- seekdb 开源早期功能仍有不足（全文/混合搜索性能、Mac 安装、Python SDK 接口丰富度），社区反馈将推动快速迭代。
- Oracle 26ai 的 Annotations（语义打标）和 Snowflake Tags 的实践效果，以及 OceanBase ODC DataPilot 的 Text2Metrics 准确率 90%+ 的真实场景验证。

## 术语表

- **AI 原生混合搜索（AI Native Search）**：向量 + 全文 + 稀疏向量 + 图搜索多路融合，通过 Rerank 排序得到精准结果的过程。
- **AI Function**：数据库内嵌的 AI 算子（ai_embed、ai_rerank、ai_complete、ai_parse_document、ai_filter、ai_join 等），一条 SQL 即可同时操作数据与调用模型。
- **seekdb**：OceanBase 开源的面向开发者的 AI 原生数据库（Apache 2.0），起步 1C2G，支持关系/JSON/向量/全文混合搜索。
- **RRF（Reciprocal Rank Fusion）**：多路召回融合算法，按排名倒数求和，简单鲁棒，不依赖各路分数的绝对值。
- **Document In, Data Out**：将文档写入数据库后，由数据库自动完成切片、Embedding、混合搜索、生成，不再需要应用层拼装多个数据库和模型。
- **数模融合**：数据和模型的深度融合，AI Function 将无结构数据处理嵌入数据库执行算子，同时优化 AI 调用次数。

## 原始来源

[[Clippings/AI原生数据库的思考.md]]
