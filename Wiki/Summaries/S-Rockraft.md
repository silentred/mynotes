---
id: S-Rockraft
title: Rockraft：基于 OpenRaft 与 RocksDB 的强一致 KV 存储框架
author: codedump
source: https://www.codedump.info/zh/post/20260412-rockraft/
reference: Clippings/Rockraft：基于 OpenRaft 与 RocksDB 的强一致 KV 存储框架.md
date: 2026-04-14
tags:
  - Rust
  - Raft
  - 分布式存储
  - KV存储
  - OpenRaft
---

## 核心内容总结

1. Redis 协议已是事实 KV 存储协议标准，但现有实现（Valkey、Kvrocks、Dragonfly 等）均为最终一致性，Rockraft 通过引入 Raft 共识算法，为 Redis 协议补全 CP 能力，实现强一致持久化 KV 存储。
2. Rockraft 架构四层：RPC/通信层（承接客户端 + 集群内通讯）→ OpenRaft 共识引擎（维护 Raft 状态转移，与存储解耦）→ 存储抽象适配层（RaftLogStorage + RaftStateMachine Trait 是核心胶水）→ RocksDB 物理存储层（三列族：Raft Logs / Hard State / State Machine）。
3. Rust 语言选择：类型安全 + 内存安全降低并发编程心智负担；底层选用 OpenRaft（现代化异步事件驱动架构，基于 Raft 事件而非定时 tick，生产用户包括 Databend/CnosDB/RobustMQ）而非已进入维护模式的 raft-rs。
4. 存储层通过列族（Column Family）实现物理/逻辑隔离：Raft Logs 列族利用 RocksDB 顺序写特性存储日志；State Machine 列族存放真正被 Commit 的业务数据（仅在日志达成多数派共识后才回放）；Hard State 列族保证节点重启后不发生脑裂。
5. 框架提供原子批量写入、条件事务（8 种比较操作）、线性一致性读取等接口，用户基于 Rockraft 只需实现两个 Trait 即可构建专属强一致存储。

## 关键数据

- **Kvrocks 成本优势**：存储成本仅为纯内存方案的 **1/5 ~ 1/10**，支持数十 TB 级数据
- **Dragonfly 吞吐量**：最高可达 Redis 的 **25 倍**（BSL 许可证）
- **架构核心 Trait**：RaftLogStorage（日志存储）+ RaftStateMachine（状态机应用），两 Trait 打通共识引擎与存储层
- **三层列族隔离**：Raft Logs / Hard State / State Machine

## 简述要点

Redis 协议已是 KV 存储的事实标准，但其现有实现均未突破最终一致性。Rockraft 的动机是为这一广泛生态引入强一致性：写入返回成功意味着已在集群多数节点持久化。架构层面，OpenRaft 作为共识引擎完全与存储解耦，只负责 Raft 状态机状态转移（日志复制、Leader 选举、成员变更），具体如何存储日志和应用数据由用户实现的 Trait 决定。Rockraft 自身则通过实现 RaftLogStorage + RaftStateMachine，将共识引擎与 RocksDB 连通——日志以顺序写方式落入 Raft Logs 列族，Commit 后的业务操作才在 State Machine 列族回放。Rust 的类型安全使这一 Trait 边界清晰，编译期即能捕获大量错误。框架支持条件事务（CAS）、线性一致性读取、Learner 角色、动态成员变更等高级特性，未来方向包括引入 Raft Engine 优化存储性能及 Multi-Raft 支持。

## 疑点 / 待验证

- OpenRaft 目前尚不支持多 Raft 组（Multi-Raft），Rockraft 计划在其上层实现，是否会引入额外复杂性
- Joint Consensus 成员变更的安全性优于单步变更，但运维复杂度更高，实际生产中的权衡取舍

## 术语表

- **Rockraft**：基于 OpenRaft + RocksDB 的 Rust 强一致 KV 存储框架，通过 RaftLogStorage/RaftStateMachine 两个 Trait 解耦共识与存储
- **OpenRaft**：现代化 Raft 实现，完全异步事件驱动（基于 Raft 事件而非定时 tick），通过 RaftLogStorage/RaftStateMachine/RaftNetwork 三个 Trait 扩展存储和网络层
- **raft-rs**：Rust 生态最成熟的 Raft 库（源自 etcd Go 实现移植），已进入维护模式；TiKV 基于此实现 Multi-Raft
- **RaftLogStorage Trait**：OpenRaft 定义的核心接口，用户实现后告知 Raft 引擎"如何存储和读取日志"，是共识层与存储层解耦的关键
- **RaftStateMachine Trait**：OpenRaft 定义的核心接口，用户实现后告知 Raft 引擎"如何将 Committed 日志应用到业务状态机"
- **Joint Consensus**：Raft 成员变更算法，先经过新旧配置共同生效的联合配置阶段，再过渡到新配置，避免单步变更在网络分区时可能导致的一致性问题
- **线性一致性读取（Linearizable Read）**：读取操作返回最近一次写入的结果，如同在单一副本上执行；OpenRaft 提供 `ensure_linearizable` 接口实现
- **Column Family（列族）**：RocksDB 的逻辑隔离机制，同一 RocksDB 实例通过列族实现物理/逻辑隔离，三列族设计：Raft Logs（顺序写日志）、Hard State（Term/Vote 等重启必需状态）、State Machine（业务数据）
- **Learner（Non-voter）**：Raft 中不参与投票的节点，可接收日志但不参与选举，用于扩展只读副本或热备

## 原始来源

[[Clippings/Rockraft：基于 OpenRaft 与 RocksDB 的强一致 KV 存储框架.md]]
