---
id: S-LLM Knowledge Bases by karpathy
title: LLM Knowledge Bases：Karpathy 的 AI 个人知识库工作流
author: Andrej Karpathy
source: https://x.com/karpathy/status/2039805659525644595
date: 2026-04-05
tags:
  - AI
---

## 核心结论

1. **LLM Wiki 模式**区别于 RAG 的本质在于：Wiki 是**持久化、复合增长的知识资产**，跨文档的引用和矛盾在编译时就已处理，查询时不再需要从原始文档重新拼装——知识是被"记住"而非"检索"。
2. Karpathy 的 AI 工作流：原始数据（raw/）→ LLM 增量编译 Wiki（Summaries/Articles/Concepts）→ Obsidian 作为前端 IDE → LLM 通过 CLI/MCP 操作 Wiki 进行问答和增强。
3. Wiki 的"lint"阶段（健康检查：找矛盾、填空白、查孤立页）是 LLM 独有能力，人工维护 wikis 的核心障碍（维护成本随规模超线性增长）在 LLM 这里近乎为零。

## 关键数据

- Karpathy 部分 Wiki 规模：约 100 篇源文章，约 40 万词（400K words）
- Qmd：本地 markdown 搜索工具，支持 BM25 + 向量混合搜索和 LLM 重排，有 CLI 和 MCP 两种接入方式
- Obsidian Web Clipper：将网页文章转为 markdown；配套热键可自动下载图片到本地
- Log 文件格式：每个 entry 以 `## [YYYY-MM-DD]` 开头，用 `grep "^## \["` 即可解析时间线

## 疑点 / 待验证

- Wiki 规模从 100 篇增长到 1000 篇时，index 文件 + 全文扫描是否仍然足够高效，还是必须引入向量检索（MCP/qmd）作为补充？
- LLM 生成的 Wiki 页面之间的交叉引用（backlinks）维护成本：新增文章时需更新多少现有页面的引用，LLM 能否无遗漏地完成这一增量更新？
- 当前 Wiki 层完全依赖 LLM 生成，不做人工校验——在知识密集型领域（如医学、法律），"AI 写、AI 改"的信任边界在哪里？

## 术语表

- **LLM Wiki Pattern**：原始数据 → LLM 编译 → 结构化 Wiki → LLM 操 Wiki 进行问答和增强，知识以 md 文件形式持久积累。
- **Raw Layer**：原始资料目录（.md、PDF、图片），不可变，LLM 只读不写，作为信任根。
- **Wiki Layer**：LLM 生成的摘要、概念页、文章，按目录结构组织，LLM 全权维护。
- **Schema/CLAUDE.md**：LLM Wiki 的操作规范（目录职责、命名规范、工作流），是 LLM 作为 Wiki 管理员的"制度文档"。
- **Linting（健康检查）**：LLM 周期性扫描 Wiki 发现矛盾、陈旧引用、孤立页和空白概念，是 Wiki 自我进化的机制。
- **Qmd**：本地 markdown 搜索工具，支持 BM25/向量混合 + LLM 重排，离线运行，有 CLI 和 MCP server。

## 原始来源

[[Clippings/LLM Knowledge Bases by @karpathy.md]]
