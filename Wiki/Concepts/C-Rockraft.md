---
id: C-Rockraft
title: Rockraft
reference: Clippings/Rockraft：基于 OpenRaft 与 RocksDB 的强一致 KV 存储框架.md
updated: 2026-04-14
---

## 定义

Rockraft 是一个基于 OpenRaft 共识引擎与 RocksDB 物理存储的 Rust 强一致 KV 存储框架。它将 "Raft + RocksDB" 的架构组合解耦为通用基座，用户通过实现 RaftLogStorage 和 RaftStateMachine 两个 Trait，即可基于此构建专属的强一致性存储系统。

## 关联来源

[[Clippings/Rockraft：基于 OpenRaft 与 RocksDB 的强一致 KV 存储框架.md]]

## 已知边界 / 局限

- OpenRaft 目前不支持多 Raft 组（Multi-Raft），Rockraft 计划在其上层实现，存在额外复杂性风险
- Joint Consensus 成员变更安全性高但运维复杂，不如单步变更直观
- 框架成熟度仍在演进，未来可能引入 Raft Engine 优化存储性能

## 实际案例

- **Rockraft 自身**：Rust 实现，架构四层（RPC/通信 → OpenRaft 共识引擎 → 存储抽象适配层 → RocksDB），三列族隔离（Raft Logs/Hard State/State Machine）
- **coredb**：基于 Rockraft 的强一致且兼容 Redis 协议的服务，写入返回成功 = 半数以上节点写入成功
- **TiKV**（raft-rs）：基于 raft-rs 的生产用户，展示 Multi-Raft 架构（海量 Region 分片）
- **Databend / CnosDB / RobustMQ**：OpenRaft 的生产用户
