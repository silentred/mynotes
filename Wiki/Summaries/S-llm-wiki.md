---
id: S-llm-wiki
title: LLM Wiki：利用 LLM 构建个人知识库的模式与架构
author: Andrej Karpathy
source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
date: 2026-04-08
tags:
  - AI
---

## 核心结论

1. **LLM Wiki 的核心价值**是将知识从"每次查询时重新发现"变为"持久积累"——Wiki 中的交叉引用、矛盾标记、概念聚合是 LLM 一次编译、长期复用的资产，与 RAG 的根本区别在于积累性（compounding）。
2. 三层架构：**Raw Sources（只读）** → **Wiki（LLM 生成维护）** → **Schema/CLAUDE.md（规范）**，LLM 是 Wiki 的唯一编辑者，人类只负责素材和提问。
3. **知识积累 vs 检索**：RAG 是"知识在上下文窗口中"，LLM Wiki 是"知识在文件系统结构中"；前者重发现，后者重复用；前者适合快速问答，后者适合深度研究。

## 关键数据

- Wiki 规模建议：index.md 可覆盖约 100 篇源文档、几百个页面的知识库，无需引入向量检索基础设施
- Log.md 时间线格式：`## [YYYY-MM-DD] ingest | Article Title` 格式，可用 `grep "^## \[" log.md | tail -5` 解析
- Obsidian Web Clipper：网页文章转 markdown；设置固定附件目录 + 下载热键，可将远程图片本地化供 LLM 直接引用
- Qmd（MCP server）：BM25 + 向量混合搜索 + LLM 重排，离线运行，LLM 可直接调用
- 架构演进提示：当 Wiki 过大时，可从 index 文件导航升级为专用搜索引擎（qmd），是渐进式的最佳实践

## 疑点 / 待验证

- 多用户场景（团队 Wiki）下的权限和一致性：Wiki 的 LLM 编辑模式假设单一编辑者，多人协作时 LLM 维护者的"唯一权威"假设如何打破。
- Raw Sources 的 immutable 原则在实践中难以完全遵守——当源文档本身有错误时，Wiki 如何处理而不引入二次错误传播。
- 该模式依赖 LLM 的摘要和交叉引用质量，长文本（如书籍章节）的编译效果是否稳定，不同 LLM 能力差异是否显著影响 Wiki 质量。

## 术语表

- **LLM Wiki Pattern**：Raw → LLM 编译 Wiki → LLM 操作 Wiki 的知识管理飞轮，知识随每次使用和每次 ingestion 积累。
- **Compounding（复合增长）**：Wiki 每次更新不仅回答当前问题，还增强未来所有查询的能力——与 RAG 的本质区别。
- **Raw Sources**：Immutable 的原始资料集合，LLM 只读不写，是 Wiki 的信任根。
- **Wiki Layer**：LLM 生成和全权维护的知识层，包含 Summaries、Concepts、Articles、Comparisons 等，按约定目录结构组织。
- **Schema（CLAUDE.md）**：描述 Wiki 结构的配置文件，是 LLM 作为 Wiki 管理员的操作手册和约束规范。
- **Linting**：周期性健康检查，发现矛盾、陈旧、孤立页，LLM 可增量修复，是 Wiki 自我进化的机制。
- **Qmd**：本地 markdown 搜索引擎（BM25 + 向量 + LLM 重排），离线运行，提供 CLI 和 MCP server 两种 LLM 接入方式。

## 原始来源

[[Clippings/llm-wiki.md]]
