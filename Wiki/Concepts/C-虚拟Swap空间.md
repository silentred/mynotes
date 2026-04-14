---
id: C-虚拟Swap空间
title: 虚拟 Swap 空间
reference: Clippings/最硬核的一次 Linux 内核重构.md
updated: 2026-04-14
---

## 定义

虚拟 Swap 空间（Virtual Swap Space）是一层将 swap entry 与底层物理 swap 设备解耦的抽象：swap entry 不再直接绑定设备索引+槽位偏移，而是指向一个虚拟槽位，再由虚拟层映射到物理设备或 zswap/零页。这解决了 swap off 扫描 PTE、zswap 必须预占物理设备空间等历史遗留问题。

## 关联来源

[[Clippings/最硬核的一次 Linux 内核重构.md]]

## 已知边界 / 局限

- **内存开销显著**：swp_desc 结构体（~32 字节）相比原 swap entry（8 字节）扩大最多 4 倍，对以释放内存为目标的子系统而言代价可观
- **性能回退**：Meta 方案在部分基准测试中出现性能回退
- **强制 vs 可选**：Meta 方案为强制中间层，TencentOS GhostSwap 主张应该是可选的
- **语义破坏**：实质上破坏了 swap off 的原有语义（swap off 原本意味着彻底移除设备）
- **社区分歧**：两条路线（Virtual Swapspace vs Dynamic Ghost Swapfile）尚无合并迹象，swap tiers 补丁也可能整合进来

## 实际案例

- **Meta Virtual Swapspace**：引入 swp_desc 数组作为强制中间层，页面可在 swap 设备和 zswap 之间自由迁移，无需预先分配后备槽位；但带来 4 倍内存开销和性能回退，社区合并前景不明
- **TencentOS Dynamic Ghost Swapfile**：非强制方案，以 XArray 实现动态大小虚拟 swap 文件，`swapon /dev/ghostswap` 获得 PB 级虚拟空间，对现有用户零侵入，性能和可扩展性优势明显；Kairui Song 与 Chris Li（Google）联合推进
- **Swap Tiers**：Youngjun Park 提出的分层 swap 方案，允许配置高/低速设备 tier + cgroup 钩子控制进程组可访问的 tier，为延迟敏感工作负载提供 QoS
