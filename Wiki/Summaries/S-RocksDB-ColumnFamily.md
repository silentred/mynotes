---
id: S-RocksDB-ColumnFamily
title: RocksDB Column Family：共享 WAL、独立 LSM
author: "[[Liao Tonglang]]"
source: https://quant67.com/post/db/rocksdb/13-column-family/13-column-family.html
reference: Clippings/【RocksDB 内核机制】Column Family：共享 WAL 与独立 LSM.md
date: 2026-08-17
tags:
  - RocksDB
  - 存储引擎
  - LSM
---

## 核心内容总结
- **CF 是逻辑分区**：RocksDB 3.0 引入 Column Family，每个 key-value 恰属一个 CF；WAL 整库共享，MemTable / SST / Version 链按 CF 独立。
- **跨 CF 原子写**：一次 `WriteBatch` 可含多 CF 记录，依赖单 WAL + 单 sequence 空间保证整批 commit 或都不生效。
- **两层 Options**：`DBOptions`（整库，如 `max_background_jobs`、`wal_dir`、`rate_limiter`）与 `ColumnFamilyOptions`（单 CF，如 `write_buffer_size`、`compaction_style`、`comparator`）分层管理。
- **WAL 回收被最慢 CF 牵制**：任一 CF flush 时可能切换新 WAL，旧 WAL 只有在所有 CF 都 flush 且数据进入 SST 后才可删除；`max_total_wal_size` 触发自动 flush 滞后 CF。
- **CF vs 多 DB**：CF 共享 WAL 实现原子跨 CF 写，代价是 stall 联动；多 DB 硬隔离 I/O 但丧失跨库原子批写。

## 关键数据
- 同一窗口算子注册 `ValueStateDescriptor("count")` 与 `MapStateDescriptor("user-last-seen")` → 至少 2 个业务 CF（外加 RocksDB 内置 `default`）。
- RocksDB 9.x 版本锚定，Flink 1.20+ 适用。
- 文章含 2 张 mermaid 流程图，分别描绘"单 DB 多 CF 共享 WAL 物理布局"和"Flink WindowOperator → CF 映射"。

## 简述要点
Column Family 是 RocksDB 在 LevelDB 单 LSM 模型之上做的"逻辑分区"抽象。它的精妙之处在于把"哪些共享、哪些隔离"这个权衡做到了细致入微——WAL 共享是为了跨 CF 原子写（事务级别的刚需），MemTable/SST 独立是为了不同数据有不同的 compaction 策略与 TTL。这套设计让 Flink 这种"每种 state 变量需要独立 LSM 行为"的引擎天然适配：一个算子注册多种 state descriptor，RocksDB 端就建对应数量的 CF，无需用户手动管理 LSM 分裂。但硬币的另一面是"stall 联动"——某个 CF 写爆炸导致 L0 堆积，共享的 `WriteController` 会 stall 所有 CF 的写入。这是社区一直在讨论"能否 per-CF RateLimiter"的核心动因。从选型角度看：CF 适合"模块隔离 + 单进程嵌入 + 需要跨模块原子写"的场景（TiKV、Flink）；多 DB 实例适合"硬隔离优先、跨库一致性可妥协"的场景。

## 疑点 / 待验证
- per-CF RateLimiter / stall 配额目前社区讨论多，文章明确说"无默认产品行为"——需后续在 RocksDB 9.x issue tracker 跟进。
- `DropColumnFamily` 后数据延迟删除直至 Handle 归零，对运维监控"何时真的释放磁盘"的判断有迷惑性，未给出推荐探针方案。

## 术语表
- Column Family（CF）：RocksDB 的逻辑分区单位，同一 DB 实例内可有多组独立 LSM 但共享一份 WAL。
- SuperVersion：单个 CF 的快照视图，由 mem + imm + Version 组成，`GetImpl` 需传入 `ColumnFamilyHandle*` 定位。
- `WriteBatch`：原子批写容器，可跨 CF；跨 CF 原子性依赖单 WAL + 单 sequence 空间。
- WAL 回收：旧 WAL 仅当所有 CF flush 且数据进入 SST 后才能删除，最慢 flush 的 CF 决定回收节奏。
- `ColumnFamilyHandle`：CF 的运行时句柄，类似"打开的 CF 文件描述符"，Drop 后仍可对已 drop CF 读写直至引用归零。

## 原始来源
[[Clippings/【RocksDB 内核机制】Column Family：共享 WAL 与独立 LSM.md]]