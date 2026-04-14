---
id: S-最硬核的一次Linux内核重构
title: 最硬核的一次 Linux 内核重构：Swap 子系统现代化
author: TencentOS（Kairui Song 等）
source: https://mp.weixin.qq.com/s?__biz=MjM5ODYwMjI2MA==&mid=2649801153
reference: Clippings/最硬核的一次 Linux 内核重构.md
date: 2026-04-14
tags:
  - Linux内核
  - Swap子系统
  - 内核重构
  - 内存管理
---

## 核心内容总结

1. 腾讯 TenCentOS 内核工程师 Kairui Song 用 18 个月分阶段重构 Linux Swap 子系统，Phase 1（swap table，6.18）替换 XArray 获 5-20% 性能提升；Phase 2（swap map 移除，7.0）节省约 30% 元数据内存；Phase 3/4（统一分配路径、swap cgroup 静态数组移除）再节省约 512MB（1TB swap 设备场景）。
2. 重构核心思路：将 swap cache 与 swap map 两个独立数据结构**统一于 swap table**，消除 XArray 后以简单 C 数组管理槽位状态，大幅减少锁争用与内存开销。
3. 删除 swap bypass 特性（Phase 2）的重要副作用：THP/mTHP（大页）在任何引用计数下均可完整换入，不再受限于 bypass 路径。
4. 虚拟 Swap 空间是下一步方向：Meta 的 Virtual Swapspace 方案（强制中间层）与 TencentOS 的 Dynamic Ghost Swapfile（XArray 实现，PB 级虚拟空间，零侵入）并存，社区尚有分歧。
5. MGLRU 补丁（2026 年 3 月）针对文件页面回收优化，测试中有约 **30%** 性能提升（HDD 场景超 100%），生产 OOM 问题明显减少。

## 关键数据

- **Phase 1 性能提升**：5-20%（swap table 替换 XArray，6.18 合入）
- **Phase 2 内存节省**：约 **30%** 元数据开销（swap map 移除，7.0+）
- **Phase 3 内存节省**：约 **512MB**（swap cgroup 静态数组移除，1TB swap 设备）
- **Phase 4 虚拟空间**：PB 级（`/dev/ghostswap` 单次 swapon）
- **MGLRU 补丁提升**：文件密集负载 **~30%**，HDD 部分场景 **>100%**
- **核心数据结构演进**：address_space + XArray + swap cluster + swap map（多套独立机制）→ **swap table（单一统一机制）**

## 简述要点

Linux Swap 子系统数十年积累了大量复杂度：swap cache 和 page cache 共用 XArray，swap map 作为独立字节数组追踪引用计数，两者还需 SWAP_HAS_CACHE 位锁同步，且每 64MB 一个 address_space 结构造成大量锁竞争。Kairui Song 的重构分阶段推进：Phase 1 以 swap table（动态分配的 per-cluster C 数组）替代 XArray，统一 address_space 和 swap cluster 为单一聚簇方案，同时引入 swap_space 简化 API，吞吐量提升 5-20%。Phase 2 移除 swap bypass（因其复杂性已不再必要：swap table 使 swap cache 足够快），同时去掉 SWAP_HAS_CACHE 位，swap map 引用计数被合并进 swap table entry（低 bit 编码类型，高位存引用计数 PFN 或 shadow），swap map 整体移除，节省 30% 元数据。Phase 3/4 统一匿名页和共享内存换出路径消除竞态，并移除 mm/swap_cgroup.c 的静态数组（512MB/1TB），提出 Dynamic Ghost Swapfile 探索架构上限。后续 MGLRU 补丁继续推动内存回收优化。

## 疑点 / 待验证

- Dynamic Ghost Swapfile 的 XArray 实现与 Meta Virtual Swapspace 的强制中间层方案能否在社区合并
- swap tiers（分层 swap）与虚拟 swap 空间两条路线最终是否走向融合

## 术语表

- **Swap 子系统**：将匿名页（进程堆/栈/数据区）换出到持久化存储的内存管理机制，当 RAM 不足时腾出空间给活跃工作负载
- **Swap Table**：Phase 1 引入的核心数据结构，用 per-cluster C 数组替代 XArray，每个 entry 直接编码槽位状态（空/驻留 folio/shadow/bad slot），统一了 swap cache 和 swap map 职责
- **Swap Map**：原内核中每槽位一字节的引用计数数组，存在 62 计数上限溢出处理（溢出页链表）、SWAP_HAS_CACHE 位锁等复杂性，Phase 2 后被合并进 swap table
- **Swap Cache**：映射 swap 槽位与物理页 folio 的缓存层，处理换入 IO 期间的同步与反向查询；Phase 2 后接管 swap map 的并发控制职责
- **Swap Bypass**：2018 年引入的优化路径（快速设备绕过 swap cache 直接同步换入），Phase 2 因 swap table 使 cache 足够快而被移除
- **XArray**：Linux 内核的高效数组结构（原 radix tree），Phase 1 前被 swap 子系统用于管理 swap cache；被 swap table 替代后已移除
- **SWAP_HAS_CACHE Bit**：swap map 中的位标志，表示槽位已分配但无 PTE 引用；作为位锁用于并发同步，Phase 2 后被移除
- **虚拟 Swap 空间（Virtual Swapspace）**：Meta 提出的强制中间层方案，以 swp_desc 数组统一管理 swap entry 与 zswap/零页等映射，解决 swap off 扫描和 zswap 困境
- **GhostSwap / Dynamic Ghost Swapfile**：TencentOS 提出的非强制虚拟 swap 方案，以 XArray 实现 PB 级虚拟空间，零侵入现有用户，swapon /dev/ghostswap 即可使用
- **MGLRU（Multi-Gen LRU）**：多代 LRU 页面回收算法，2026 年 3 月补丁聚焦文件页回收与脏页处理优化

## 原始来源

[[Clippings/最硬核的一次 Linux 内核重构.md]]
