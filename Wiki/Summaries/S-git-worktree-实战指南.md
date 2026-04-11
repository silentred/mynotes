---
id: S-git-worktree-实战指南
title: git worktree 实战指南：使用场景、常用命令、解决的问题与日常工作流
author: zempty思考与行动，让未来更清晰
source: https://zhuanlan.zhihu.com/p/1938293629455152167
date: 2026-04-11
tags:
  - git
  - worktree
---

## 核心内容总结

1. **git worktree 为同一仓库创建多个并行工作区**：多个工作目录共享 `.git/objects` 和索引，每个工作区可检出不同分支/提交，同时开发互不干扰，磁盘占用远低于多仓 clone。
2. **核心约束：同一分支同时只能被一个 worktree 检出**：并行多任务需使用不同分支名或 `--detach` 检出到指定提交，同一分支重复检出会报错。
3. **典型场景覆盖并行开发、热修复、长分支隔离、大仓并行编译、评审验证**：常用命令为 `add`（创建）、`remove/prune`（清理）、`lock`（保护）、`move`（迁移）、`repair`（修复）。
4. **相比切分支+stash 更安全，相比多仓 clone 更省空间**：避免了频繁 stash 的上下文污染和误操作风险，同时共享对象库节省磁盘 I/O。
5. **目录约定 `.wt/` + 用完即清理是好习惯**：推荐在仓库根目录旁建立 `.wt/` 子目录集中管理所有 worktree，任务完成后统一 remove + prune 回收空间。

## 关键数据

- 创建：`git worktree add ~/.wt/feature-x -b feature/x origin/main`
- 强制删除：`git worktree remove -f ~/.wt/feature-x`（有丢弃未提交改动风险）
- 清理残留：`git worktree prune`
- 锁定保护：`git worktree lock ~/.wt/release-1-5 --reason "hotfix"`
- 路径迁移：`git worktree move old-path new-path`
- 仓库迁移后修复：`git worktree repair`
- 常见报错：`branch <name> already checked out` 表示同一分支已被其他 worktree 检出

## 疑点 / 待验证

- `sparse-checkout` 与 worktree 可组合使用但关注点不同，前者解决单工作区目录稀疏检出，后者解决多并行工作区，二者协同使用的最佳实践尚无定论。
- 对 submodule/subtree 等多仓协作场景，worktree 不提供替代方案，仍需独立管理依赖关系。

## 术语表

- **git worktree**：Git 提供的工作树特性，允许同一仓库同时拥有多个工作目录，共享 `.git/objects` 与索引，每个工作区可独立操作。
- **worktree prune**：清理无效或已被手动删除的 worktree 记录，与 `remove` 不同（删除指定路径 vs 清理所有残留）。
- **worktree lock**：锁定工作区防止被误删或 prune，可附加原因说明。
- **--detach**：以分离头指针方式检出到指定提交，不占用分支名，适合临时验证场景。

## 原始来源

[[Clippings/git worktree 实战指南：使用场景、常用命令、解决的问题与日常工作流]]
