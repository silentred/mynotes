---
id: S-raft工程化案例之etcd源码实现
title: Raft 工程化案例：etcd 源码实现
author: 小徐先生1212
source: https://mp.weixin.qq.com/s/jsJ3_E_5IOs4_rPDM5axzQ
date: 2026-04-05
tags:
  - database
  - etcd
  - raft
  - distributed-sys
---

## 核心结论

1. etcd 将 Raft 算法实现拆分为**算法层**（纯粹的共识逻辑）和**应用层**（网络通信、持久化、状态机管理），两者通过 channel 异步通信，实现了关注点分离。
2. 算法层通过 **Ready 结构**与应用层交互：每轮处理完请求后，Ready 封装已提交日志（CommittedEntries）、待持久化日志（Entries）和待发送消息（Messages），由应用层完成 I/O 后调用 Advance 推进。
3. Raft 节点本质是**消息驱动的状态机**，任意操作（选举、日志同步、读请求）最终都封装为 Message 输入节点状态机，驱动状态变更。

## 关键数据

- etcd 走读源码版本：tag v3.1.10
- 日志存储分两层：**unstable**（未持久化）+ **storage**（已持久化）
- Leader 心跳间隔：heartbeatTimeout = 1 tick；选举超时：electionTimeout = 10 tick；选举超时带随机扰动避免活锁
- ReadIndex 算法需要 leader 向所有节点广播特殊心跳，确认自身仍为合法 leader 后才能返回数据，确保线性一致性

## 疑点 / 待验证

- etcd 中 **LeaseRead**（租约读）的安全性边界：依赖时钟同步，若 follower 与 leader 时钟偏差过大可能读到过期数据。
- 消息驱动状态机的设计虽然简化了协议，但 Message 类职责过重（耦合日志/选举/心跳/读请求），是否符合工程化最佳实践有争议。
- raftNode 与 kvStore、httpapi 的分层设计是否具有普适性，复杂业务中是否需要更精细的分层抽象。

## 术语表

- **算法层（Algorithm Module）**：内聚 raft 共识机制核心的静态库，通过 channel 与应用层异步通信，对应用层屏蔽共识细节。
- **应用层（Application Module）**：聚合存储、通信能力的模块，是 raft 节点的主 goroutine，承上启下。
- **Ready 结构**：算法层处理完一轮请求后输出的结果封装，包含 SoftState、HardState、Entries、CommittedEntries、Messages 五类数据。
- **Node 接口**：应用层与算法层交互的唯一入口，包含 Propose、Ready、Advance、Tick 等方法。
- **raftLog**：算法层管理预写日志的核心模块，含 unstable（未持久化）和 storage（持久化）两个子模块。
- **readOnly**：leader 持有的一组挂起读请求队列，通过 ReadIndex 机制实现线性一致性读。
- **Progress**：leader 记录其他节点日志同步进度的结构，Match = 已同步索引，Next = 下次同步起点。
- **PreVote 机制**：在正式发起选举前先进行预竞选，避免因网络分区导致节点频繁切换身份而破坏系统稳定性。

## 原始来源

[[Clippings/raft 工程化案例之 etcd 源码实现.md]]
