---
id: C-Agent优先开发
title: Agent 优先开发
reference: Clippings/工程技术：在智能体优先的世界中利用 Codex.md
updated: 2026-04-15
---

## 定义

Agent 优先开发（Agent-first Development）是一种以智能体（Agent）为主要代码贡献者的人类软件工程范式。其核心原则是"不手动编写代码"：人类工程师的职责从写代码转向**设计环境、明确意图、构建反馈回路**，智能体负责执行。

## 关联来源

[[Clippings/工程技术：在智能体优先的世界中利用 Codex.md]]

## 已知边界 / 局限

- **架构连贯性未知**：完全由智能体生成的代码库在 1 年以上时间跨度内的架构健康度尚无先例
- **反馈回路质量决定上限**：环境规范不清晰时，智能体会因缺乏工具和内部结构而停滞
- **知识边界严格**：Codex 运行时无法访问的任何信息（Google Docs、Slack、人类头脑中的隐性知识）对其而言不存在——代码仓库必须成为唯一的记录系统
- **Agent-to-Agent 评审**：需要在智能体评审工具、人机反馈整合机制上持续投入

## 实际案例

**OpenAI 团队 Harness Engineering 实验**（2025-2026）：3 人工程师团队 + Codex，5 个月交付约 100 万行代码的内部 beta 产品，平均每人每天 3.5 个 PR。核心技术实践：

- **渐进式披露**：`AGENTS.md`（~100 行地图）+ 结构化 `docs/` 目录作为真实记录系统
- **可观测性堆栈**：Codex 直接查询 LogQL/PromQL/TraceQL 自主推理应用状态
- **Chrome DevTools MCP**：Codex 自主验证 UI 修复，端到端驱动错误复现→修复→验证循环
- **黄金原则 + 垃圾回收循环**：自定义 lint 强制执行架构不变式，定期后台任务扫描漂移并自动重构
- **架构前置**：分层领域架构（Types→Config→Repo / Providers→Service→Runtime→UI）+ 自定义 lint 机械执行，而非等规模扩大再演进
