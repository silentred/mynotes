---
id: C-Raft
title: Raft 共识算法
updated: 2026-04-08
---

## 定义

Raft 是一种分布式共识算法，通过强 Leader、选举限制和日志匹配属性保证分布式系统中多个节点就日志顺序达成一致，是 Paxos 的可理解性替代方案，在 etcd、Kubernetes 等工业系统中广泛采用。

## 关联来源

[[Clippings/raft 工程化案例之 etcd 源码实现.md]]
[[Clippings/第五章：共识算法.md]]
[[Clippings/etcd 中线性一致性读的具体实现.md]]

## 已知边界 / 局限

- **成员变更的正确性问题**：单步成员变更在某些情况下会丢失已提交日志（需修复为 Leader 当选后先提交 no-op 日志）；联合共识虽正确但实现复杂，实践中需谨慎处理
- **活锁风险**：日志相同的节点间可能反复切换 Leader；Pre-Vote 和 Leader Lease 可缓解但不能完全消除
- **线性一致性读的开销**：ReadIndex 虽优化了读性能，但高并发读场景下仍有 Leader 确认身份的心跳开销
- **日志压缩（快照）对运维的要求**：快照生成时机需配置，过频影响性能，过疏导致重启恢复慢

## 版本 / 演进

- 原始 Raft 论文（Diego Ongaro, 2014）：单步成员变更（后续发现存在正确性问题）
- 2015 年修正：Leader 当选后先提交 no-op 日志，再同步成员变更日志
- etcd 实现：加入 CheckQuorum 机制，防止孤岛 Leader；ReadIndex 优化线性一致性读；LeaseRead 进一步优化读延迟
