---
id: C-线性一致性读
title: 线性一致性读
updated: 2026-04-08
---

## 定义

线性一致性读（Linearizable Read）要求每次读请求都能读到最新写入的值，是分布式系统中最强的一致性保证。它要求：非并发操作的执行顺序在全局排序中必须与实时时间一致——换言之，系统"表现得像一个单一副本"，读操作不返回过期数据。

## 关联来源

[[Clippings/etcd 中线性一致性读的具体实现.md]]
[[Clippings/第五章：共识算法.md]]
[[Clippings/第四章：复制.md]]

## 已知边界 / 局限

- **Leader 确认身份的必要性**：网络分区时旧 Leader 可能仍认为自己是 Leader，若直接读会返回过期数据——必须在读前确认 Leader 身份
- **ReadIndex 的 Leader 确认开销**：新 Leader 需先提交 no-op 日志确认身份，高并发读场景下这是主要瓶颈
- **LeaseRead 的时钟漂移风险**：假设在心跳后一段时间内（租约期内）Leader 身份有效，若时钟漂移或网络分区在租约期内发生，可能返回脏读

## 版本 / 演进

- **走 Raft 日志流程**（朴素方案）：每次读当写处理，提交空日志后读，开销 O(n) 消息
- **ReadIndex**（etcd 3.x）：Leader 当选后提交 no-op → 取 commitIndex 为 readIndex → 等状态机应用 → 读；比朴素方案大幅优化
- **LeaseRead**：跳过 Leader 心跳确认，直接用租约期内身份 + 当前 commitIndex，读延迟进一步降低但牺牲部分安全性
