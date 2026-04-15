---
id: S-利用Codex构建
title: 工程技术：在智能体优先的世界中利用 Codex
author: Ryan Lopopolo（OpenAI）
source: https://openai.com/zh-Hans-CN/index/harness-engineering/
reference: Clippings/工程技术：在智能体优先的世界中利用 Codex.md
date: 2026-04-15
tags:
  - AI
  - Codex
  - 软件工程
  - 智能体开发
---

## 核心内容总结

1. OpenAI 团队用 5 个月完全由 Codex（无一行人工代码）构建了一个拥有 **~100 万行代码** 的内部 beta 产品，3 人团队平均每天 3.5 个 PR；随着团队扩至 7 人，吞吐量反而**增加**。
2. 核心范式转变：**工程师工作从"写代码"转向"设计环境、明确意图、构建反馈回路"**，Codex 执行，人类掌舵。
3. 智能体开发的三大瓶颈及解法：情境稀缺 → 渐进式披露（`AGENTS.md` 是地图而非百科全书，真实知识在结构化 `docs/`）；吞吐量 > 人工 QA → 赋予 Codex 完整可观测性堆栈（LogQL/PromQL/TraceQL 直接查询）；代码熵累积 → 编码"黄金原则"到 linter + 自动化垃圾回收循环。
4. 完全由智能体生成的代码库需要**架构前置**（分层领域架构 + 自定义 lint 强制执行不变式），而非等数百人时再演进。
5. 当前最棘手挑战集中在**设计环境、反馈回路和控制系统**；Agent-first 开发仍处于早期，架构连贯性如何随时间演变尚不明确。

## 关键数据

- **代码规模**：~100 万行，5 个月内完成
- **团队效率**：3 人 → 平均每人每天 **3.5 个 PR**；扩至 7 人后吞吐量**增加**
- **单次运行**：Codex 单次任务可持续工作超 **6 小时**（常在人类睡眠时间）
- **反馈循环**：Ralph Wiggum 循环（智能体自审 → 智能体复审 → 循环直到全员满意）
- **知识管理**：约 100 行 `AGENTS.md` 作为地图，真实知识在结构化 `docs/` 目录中

## 简述要点

OpenAI 团队用 5 个月交付了一个无人工代码的百万行产品，证明 Agent-first 开发可行且吞吐远超传统模式。关键洞察：**Codex 运行时无法访问的任何信息都不存在**——Google Docs、Slack、人类头脑中的知识统统不可达。因此代码仓库必须成为唯一的记录系统（Single Source of Truth），知识以 Markdown 形式编码进版本化目录。`AGENTS.md` 是内容目录而非手册，通过渐进式披露引导智能体从稳定切入点逐步深入。自定义 linter + 结构测试机械地强制执行架构不变式（分层领域架构：Types→Config→Repo，Providers→Service→Runtime→UI），跨越"数百人时才会推迟"的架构约束阶段。Codex 通过 Chrome DevTools MCP 驱动应用验证 UI 修复，通过本地可观测性堆栈（Vector→Victoria Logs/Metrics/Traces）直接查询 LogQL/PromQL/TraceQL 进行推理闭环。代码熵通过"黄金原则"（主观但可机械执行的规则）持续清理，而非每周人工 20% 时间处理——定期后台任务扫描偏差、更新质量分数、发起重构 PR，一分钟内完成审查并自动合并。

## 疑点 / 待验证

- 完全由智能体生成的代码库，架构连贯性在 1 年、3 年、5 年后如何维持，是否需要人类定期干预
- Agent-first 模式在非技术公司、非内部工具场景的迁移成本和成功率
- Codex 单次 6 小时运行的可靠性边界，以及 Token 成本与人工成本的平衡点

## 术语表

- **Codex**：OpenAI 的 AI 编程智能体，能够直接操作代码仓库、写测试、跑命令、处理 Pull Request，支持 MCP 协议接入 Chrome DevTools、可观测性工具等
- **Agent-first 开发**：以智能体为主要代码贡献者的人类工程范式，人类负责设计环境、明确意图、构建反馈回路；核心原则是"不手动编写代码"
- **渐进式披露（Progressive Disclosure）**：知识管理策略，从小型稳定的入口点（`AGENTS.md` 地图）逐步引导到深层信息（结构化 `docs/` 目录），避免一次性大量上下文压垮智能体
- **AGENTS.md 作为目录**：将 `AGENTS.md` 从百科全书转变为内容目录，仅作为导航地图，真实知识分布在版本化的 `docs/design-docs/`、`docs/exec-plans/`、`docs/references/` 等结构化目录中
- **可观测性堆栈（Observability Stack for Agents）**：临时本地日志/指标/追踪基础设施（Vector→Victoria Logs/Metrics/Traces），通过 LogQL/PromQL/TraceQL API 暴露给 Codex，使其能自主推理应用状态而非依赖人类解读
- **Chrome DevTools MCP**：Model Context Protocol 实现，Codex 通过 MCP 驱动浏览器进行 UI 快照、事件观察、路径验证，实现端到端自主验证修复
- **代码熵 / 黄金原则**：Agent-first 开发中 Codex 会复现仓库既有模式（含不良模式），导致漂移；"黄金原则"是主观但可机械执行的规则，通过 lint 和自动化清理循环持续应用
- **垃圾回收循环（Garbage Collection Loop）**：定期后台 Codex 任务扫描偏差、更新质量分数、发起针对性重构 PR，类比内存管理中的 GC 概念
- **Ralph Wiggum 循环**：智能体自审→其他智能体复审→人类反馈→循环直到所有审核者满意，是一种 Agent-to-Agent 评审模式

## 原始来源

[[Clippings/工程技术：在智能体优先的世界中利用 Codex.md]]
