---
id: C-LLM知识库
title: LLM 知识库模式（LLM Wiki Pattern）
updated: 2026-04-08
---

## 定义

LLM Wiki Pattern 是一种利用 LLM 构建和运维个人/团队知识库的方法论，核心思想是：Raw Sources（只读原始资料）→ LLM 编译 Wiki（摘要、概念、交叉引用）→ LLM 操作 Wiki 进行问答和增强。与 RAG 的"知识在上下文窗口中"不同，LLM Wiki 的知识以 md 文件形式持久积累在文件系统结构中，具有复合增长（compounding）特性——每次使用增强未来所有查询的能力。

## 关联来源

[[Clippings/llm-wiki.md]]
[[Clippings/LLM Knowledge Bases by @karpathy.md]]

## 已知边界 / 局限

- **规模天花板**：约 100 篇源文章（40 万词）内无需向量检索基础设施；超过此规模需要引入 Qmd 等搜索引擎（BM25 + 向量混合 + LLM 重排）
- **多用户协作的权威性挑战**：Wiki 层完全依赖 LLM 作为唯一维护者，假设单一编辑者权威；多人协作时"LLM 维护者的唯一权威"假设失效
- **Raw Sources 的 immutable 原则脆弱**：源文档本身有错误时，Wiki 如何处理而不引入二次错误传播需要额外的校验机制
- **LLM 生成质量的稳定性**：长文本（书籍章节）的编译效果是否稳定，不同 LLM 能力差异是否显著影响 Wiki 质量，尚无系统性验证

## 版本 / 演进

- **Karpathy 的实现**：raw/ → LLM 增量编译 Wiki → Obsidian 作为前端 IDE → LLM 通过 CLI/MCP 操作 Wiki，约 100 篇源文档、40 万词规模
- **Qmd**：本地 markdown 搜索引擎（BM25 + 向量 + LLM 重排），离线运行，支持 CLI 和 MCP server 两种 LLM 接入方式
- **渐进式演进**：Wiki 过大时从 index 文件导航升级为 Qmd 搜索，无需推翻重来
