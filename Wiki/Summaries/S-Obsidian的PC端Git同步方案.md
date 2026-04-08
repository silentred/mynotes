---
id: S-Obsidian的PC端Git同步方案
title: Obsidian PC 端 Git 同步：Git 是最适合文本的版本管理方案
author: 沨沄极客
source: https://utgd.net/article/9642
date: 2026-04-05
tags:
  - obsidian
---

## 核心结论

1. **Obsidian 的双向链接特性使云盘同步方案（OneDrive/iCloud）失效**：修改被广泛引用的文档名称会同时修改所有引用链接，云盘在冲突时只能二选一或都保留，导致大量重复文件（OneDrive 出现稿件.md→稿件 1~21.md 的真实案例）。
2. **Git 是最适合文本内容的同步方案**：定时提交而非实时（减少冲突）、冲突可逐文件处理（而非整库二选一）、完整保留历史版本——Obsidian 的 .md 格式天然适配 Git 的 diff 和 timeline 能力。
3. **Obsidian Git 插件提供了完整的 GUI 操作入口**：Backup（提交+推送）、Pull（拉取）、Commit（仅提交）、Stage/Unstage 四个核心操作即可覆盖日常同步，无需记忆命令行。

## 关键数据

- **推荐平台**：Gitee（国内访问稳定） vs GitHub（需处理网络问题），均支持私有仓库；自托管推荐 Gogs.io（轻量，可运行在 NAS 上）
- **仓库容量限制**：GitHub 无硬上限（建议<1GB，总量<5GB）；Gitee 500MB/仓库；Gogs.io 自托管无限制
- **单文件限制**：GitHub 100MB（>50MB 警告）；Gitee 50MB；单文件过大建议使用 Git LFS
- **.gitignore 建议**：`.obsidian/workspace`（工作区布局），避免同步每次编辑状态变化
- **Timeline 查看**：VSCode 内置 Timeline 面板可查看每个 .md 文件的提交历史
- **自动同步配置**：Auto Backup after file change（默认 10 分钟）+ Auto pull（默认 10 分钟）

## 疑点 / 待验证

- 多设备同时编辑同一笔记时，Git 冲突的实际处理体验：在 Obsidian Git 插件内处理 vs 借助 GitHub Desktop，哪个更顺畅。
- Git LFS（Large File Storage）对 Obsidian 库中 PDF/图片附件的同步效果，以及 Gogs.io 对 LFS 的支持程度。
- Obsidian Git 与 Obsidian Sync（官方付费方案）同时使用时的冲突可能性——官方建议两者不可同时启用。

## 术语表

- **Obsidian Git 插件**：在 Obsidian 内提供 Git 操作面板（Backup/Pull/Commit/Stage），无需命令行即可完成定时同步。
- **Git 同步 vs 云盘同步**：Git 的定时提交 + 冲突按文件处理，相比云盘实时同步的整库冲突二选一，更适合 Obsidian 的 Wiki 语义结构。
- **.gitignore**：Git 忽略规则文件，控制哪些文件不纳入版本控制，`workspace` 布局文件建议加入以避免同步编辑器状态。
- **Git LFS（Large File Storage）**：Git 扩展，用于管理大型二进制文件（PDF、图片），将文件内容存储在 LFS 服务器上，仓库仅存指针。

## 原始来源

[[Clippings/Obsidian 的 PC 端同步方案，无代码搞定 Git 同步.md]]
