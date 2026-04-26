---
id: S-GreptimeDB开源四年
title: GreptimeDB 开源四年：回望出发、决策、弯路，和同行的人
author: "[[Jiachun]]"
source: https://greptime.cn/blogs/2026-04-21-greptimedb-four-years-retrospective
reference: Clippings/GreptimeDB 开源四年：回望出发、决策、弯路，和同行的人.md
date: 2026-04-26
tags:
  - GreptimeDB
  - 开源
  - 时序数据库
  - Rust
---

## 核心内容总结

- GreptimeDB 选择 Rust 写数据库：前期招聘更难，但 Rust 的所有权模型在 CI 阶段就消除大量并发和内存 bug，社区吸引力也超出预期，2025 年还意外获得 AI vibe coding 红利。
- 存储引擎重写时机比方向更重要：v0.4 重写 Mito2 是因为前三个版本积累了足够用户反馈和性能数据，瓶颈已到数据组织方式层面，局部修补无效。
- 统一 metrics/logs/traces 不是规划出来的，是被真实问题一步步推到这条路上，本质是为 Observability 2.0 打好数据库层基础。

## 关键数据

- 团队在上一家公司支撑过**每秒 1 亿数据点**写入的时序数据库系统
- v0.4 重写后：扫描类查询提速**数倍**，个别场景超 **10 倍**
- v1.0 Flat 格式：200 万时间线下写入吞吐提升 **4 倍多**，部分查询从 **17 秒降到 3 秒**
- **126 位贡献者**，6100 stars，5200+ commits，226 个 releases

## 简述要点

为什么出发？团队在大厂做可观测数据平台时，踩过存储成本高、实时分析难、数据类型割裂三个坑，市面没有同时解决这三个问题的方案，于是创业做 GreptimeDB。

Rust 选型：国内算少数派，但团队已写四年 Rust，更重要的是数据库内核需要精确控制内存和高并发，Go/Java 的 GC pause 在存储引擎层是不可接受的延迟毛刺。四年后回头看，Rust 帮他们在 CI 阶段就消灭了大量并发内存 bug，社区贡献者也多能深入引擎层。2025 年还意外发现 Rust 是最适合 vibe coding 的语言——编译器把 AI 生成的错误精确拍回来，形成高效"生成-报错-修正"循环。

存储引擎重写时机：v0.1-v0.3 用行存 BTreeMap 装时序数据，主键标签被重复存储，内存放大严重。从 v0.4 重写为 Mito2，按时间线组织的 Series 结构 + 列式存储 + TWCS compaction，才拿到数量级提升。核心认知是：**"什么时候重写"比"要不要重写"更关键**——太早没理解真实需求模式，太晚技术债拖死。

统一数据模型：不是规划出来的愿景，是被"metrics 解释不清时得和日志链路一起看"这个真实别扭感推到的方向。落地时先推进 metrics 表模型，再把 logs 纳入统一入口，最后补 traces。底层仍针对不同 workload 做不同优化。AI Agent 时代加速了这个方向——Agent 的可观测数据天然是高基数高维度宽事件，统一存储 + OTLP 写入能力成为刚需。

## 疑点 / 待验证

- Observability 2.0 的"宽事件"模型能否真正替代传统三支柱模式，尚需更多生产验证
- 自研 Rust 数据库在 AI 辅助 coding 时代的优势是否会持续扩大

## 术语表

- **Observability 2.0**：以"宽事件"为核心、从同一份原始数据派生 metrics/logs/traces 的可观测性范式
- **TWCS**：Time-Window Compaction Strategy，Cassandra 启发的时序数据 compaction 策略
- **Series**：时间线，时序数据中同一主键的时间序列
- **vibe coding**：AI 辅助编程，代码主要由 AI 生成，人工校正

## 原始来源

[[Clippings/GreptimeDB 开源四年：回望出发、决策、弯路，和同行的人.md]]
