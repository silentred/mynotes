---
id: S-第五章：共识算法
title: 分布式共识算法：FLP、Paxos、Raft 与线性一致性读
author: codedump
source: https://www.codedump.info/dist-system-cn/consensus/
date: 2026-04-05
tags:
  - distributed-sys
---

## 核心结论

1. **FLP 不可能性是理论边界**：在完全异步系统 + 任意一个节点崩溃的场景下，不存在确定性共识算法——共识算法必须通过引入超时等部分同步假设来换取活性（Paxos/Raft 均如此）。
2. **Raft 的核心是 Leader 选举 + 日志复制**：通过日志索引+任期号二元组保证全序性，Leader 选举限制（给日志不比本节点旧的 Candidate 投票）保证安全性，日志匹配属性（Log Matching Property）保证所有节点日志一致。
3. **联合成员变更（Joint Consensus）是工程实践的主流**：单步成员变更在理论上存在正确性问题（已提交日志可被覆盖），实际生产环境如 etcd 使用两阶段变更（$C_{old,new}$ 过渡配置）保证脑裂不发生。

## 关键数据

- **Leader 选举**：随机化选举超时 [T, 2T]，解决活锁（livelock）；Pre-Vote 预选举阶段防止日志不新的节点触发不必要的选举；Leader Lease 机制防止同日志节点间反复切换
- **ReadIndex 线性一致性读**：Leader 当选后先提交 no-op 日志确认身份 → 取 commitIndex 为 readIndex → 等状态机应用到 readIndex → 执行读取，相比每次读走 Raft 日志流程开销大幅降低
- **日志匹配属性**：两条日志（任期号，索引）二元组一致 → 数据一致；以此为基础，一致性检查（Consistency Check）通过 Follower 拒绝请求携带的最近一致位置，逐步回退 nextIndex 修正日志不一致
- **单步成员变更正确性问题**：$C_u$ 未提交时 Leader 宕机 → 新 Leader $L_2$ 提交 $C_v$ 和日志 E → $L_1$ 重新当选 → 覆盖已提交日志 → 修复：Leader 当选后必须先提交 no-op 日志
- **联合共识两阶段**：$C_{old,new}$ 日志需同时满足 $C_{old}$ 和 $C_{new}$ 两个多数派才能提交，确保中间状态两个配置均有交集，不产生两个不相交多数派

## 疑点 / 待验证

- Raft 选主时"日志不比本节点旧"的判断标准（任期号 + 索引比较）在工程实现中是否存在 corner case，尤其在网络分区恢复后的日志追赶场景。
- CheckQuorum 机制（etcd 中 Leader 主动探测是否与多数派保持连通）在高负载下的心跳延迟是否会影响 Lease 有效性判断。
- Joint Consensus 在节点数量为偶数时的正确性是否有特殊边界条件，多个联合变更连续发生时配置序列的交集性质是否始终满足。

## 术语表

- **共识算法（Consensus Algorithm）**：在部分节点故障或网络分区下，分布式集群就系统状态达成唯一决定的算法，是构建强一致性系统的基础。
- **FLP 不可能性（FLP Impossibility）**：完全异步系统 + 至少一个崩溃故障节点 → 无确定性共识算法，是分布式共识的理论边界。
- **Paxos**：Leslie Lamport 提出的共识算法，Basic Paxos 解决单值共识，Multi-Paxos 通过选主优化多值写入，无内置成员变更机制。
- **Raft**：通过强 Leader、选举限制、日志匹配属性保证安全性的共识算法，成员变更支持单步变更（需修复）和联合共识（推荐）。
- **任期号（Term）**：Raft 中的单调递增时间戳，标识逻辑时钟，用于判断节点状态和日志新旧，是 Fencing Token 的实现。
- **日志匹配属性（Log Matching Property）**：两条日志（任期号，索引）一致则数据一致；前面的日志也必然一致，是 Raft 一致性检查的基础。
- **ReadIndex**：Raft 实现线性一致性读的机制，通过确认 Leader 身份 + 取 commitIndex + 等状态机应用，避免每次读走 Raft 日志流程。
- **Pre-Vote**：Raft 选举前的预投票阶段，节点先试探是否能赢得多数派日志投票，不递增任期号，避免不必要的 Leader 退位。
- **联合共识（Joint Consensus）**：Raft 成员变更的两阶段方案，$C_{old,new}$ 过渡配置需同时满足新旧两个多数派，避免单步变更的脑裂风险。
- **CheckQuorum**：etcd 中 Leader 主动探测与多数派连通性的机制，超时主动放弃任期，防止网络分区下的"孤岛 Leader"。

## 原始来源

[[Clippings/第五章：共识算法.md]]
