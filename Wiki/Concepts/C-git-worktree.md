---
id: C-git-worktree
title: Git Worktree（工作树）
updated: 2026-04-11
---

## 定义

Git Worktree 是 Git 2.6+ 引入的特性，允许同一个仓库同时拥有多个独立工作目录，每个工作目录可检出不同分支或特定提交，底层共享 `.git/objects` 存储与索引，从而在实现工作隔离的同时保持磁盘空间高效利用。

## 关联来源

[[Clippings/git worktree 实战指南：使用场景、常用命令、解决的问题与日常工作流]]

## 已知边界 / 局限

- **同一分支同一时刻只能被一个 worktree 检出**：这是 Git 的硬约束，无法绕过；并行多任务需使用不同分支或 `--detach` 分离头指针。
- **完全隔离需求时 worktree 不够**：若需要独立的 `.git` 历史、配置或 hooks（如不同全局设置），应使用完整的多仓 clone 而非 worktree。
- **强制删除有数据丢失风险**：`git worktree remove -f` 可能丢弃未提交的改动，必须在删除前确认工作区无遗留变更。
- **不解决稀疏检出问题**：sparse-checkout 解决单工作区目录级裁剪，与 worktree 的并行工作区关注点互补但不可替代。

## 实际案例

- **并行开发 + 热修复**：主区在 `main` 开发新功能，另一个 worktree 基于 `release/1.5` 做热修，两者互不干扰，无需 stash。
- **评审验证专用工作区**：`git fetch origin pull/123/head:pr-123 && git worktree add ~/.wt/pr-123 pr-123`，本地验证后直接 remove 清理。
- **大仓多版本并行编译**：monorepo 多分支同时构建，复用同一对象库避免重复下载，节省磁盘与网络 I/O。
