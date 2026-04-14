---
id: C-Swap子系统
title: Swap 子系统
reference: Clippings/最硬核的一次 Linux 内核重构.md
updated: 2026-04-14
---

## 定义

Linux Swap 子系统是内存管理子系统的核心组件，负责在 RAM 不足时将匿名页（进程堆、栈及数据结构）换出到持久化存储，从而为活跃工作负载腾出物理内存。其核心职责包括 swap slot 分配、swap cache 管理、以及换入/换出 IO 调度。

## 关联来源

[[Clippings/最硬核的一次 Linux 内核重构.md]]

## 已知边界 / 局限

- **历史复杂性积累**：数十年间 swap cache 共用 XArray、swap map 独立维护引用计数、SWAP_HAS_CACHE 位锁同步，机制分散、锁争用严重
- **swap map 计数上限**：单字节计数器最多 62 个引用，溢出需追加物理页链表，复杂且有性能陷阱
- **swap bypass 副作用**：为快速设备（ZRAM）优化的绕过路径增加了大量条件分支和竞态 bug
- **swap off 代价高昂**：移除 swap 设备需扫描全部匿名页 PTE，更新所有 swap entry

## 实际案例

**Kairui Song 的 Swap 现代化工程（18 个月，4 个阶段）**：
- **Phase 1（Linux 6.18）**：引入 swap table（per-cluster C 数组）替换 XArray，统一 swap cache 和 swap cluster，聚簇方案从两套减为一套，吞吐量提升 5-20%
- **Phase 2（Linux 7.0+）**：移除 swap bypass，swap cache 足够快不再需要 bypass；将 swap map 引用计数合并进 swap table entry（低 bit 编码类型），彻底移除 swap map，节省 30% 元数据内存
- **Phase 3/4（进行中）**：统一 anon/shmem 分配路径消除竞态，移除 swap cgroup 静态数组（1TB 设备节省 512MB），提出 Dynamic Ghost Swapfile（PB 级虚拟空间）
