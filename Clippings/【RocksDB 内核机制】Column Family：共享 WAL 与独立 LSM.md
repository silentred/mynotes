---
title: "【RocksDB 内核机制】Column Family：共享 WAL 与独立 LSM"
source: "https://quant67.com/post/db/rocksdb/13-column-family/13-column-family.html"
author:
  - "[[Liao Tonglang]]"
published: 2026-07-07
created: 2026-08-17
description: "从 RocksDB 3.0 引入的 ColumnFamily 出发，拆解共享 WAL、独立 MemTable/SST/Version链、<code>ColumnFamilyHandle</code> 生命周期与DBOptions/ColumnFamilyOptions 分层；并对照 Flink 多 state 变量到 CF的映射边界。"
tags: []
---
[第 12 篇](https://quant67.com/post/db/rocksdb/12-concurrent-ratelimit/12-concurrent-ratelimit.html) 把 compaction 并发与 RateLimiter 钉在 `CompactionJob` 线程池上。LevelDB 时代「整库一棵 LSM + 一份 MANIFEST」在 Flink state、TiKV Region 本地引擎等场景不够用： **同一 DB 实例内需要多组 comparator、独立 compaction 策略、可单独 drop 的逻辑分区** ，又不能牺牲跨分区原子写。

数据管理

RocksDB 3.0 引入 **Column Family（CF）** ：每个 key-value 恰属一个 CF； **WAL 整库共享** ， **MemTable 与 SST 文件按 CF 独立** 。本文是系列 **第 13 篇** ，沿 Wiki *Column Families* 与 `db/column_family.*` 源码路径说明机制、 `ColumnFamilyHandle` 语义、选项分层，以及 Flink 如何把多种 state 变量映射到不同 CF（Flink 侧细节见 [stream/12](https://quant67.com/post/db/stream-processing/12-rocksdb-state-backend/12-rocksdb-state-backend.html) ，本系列第 16 篇补内核侧对照）。

> **本文是「RocksDB 内核机制」系列第 13 篇（共 18 篇）。 [→ 系列目录](https://quant67.com/post/db/rocksdb/index.html)**
> 
> | 篇目 | 核心内容 |
> | --- | --- |
> | 第 12 篇 · [并发 Compaction 与 Rate Limiter](https://quant67.com/post/db/rocksdb/12-concurrent-ratelimit/12-concurrent-ratelimit.html) | `CompactionJob` 线程池 |
> | **第 13 篇 · Column Family** | **共享 WAL、独立 LSM、Flink CF 映射** |
> | 第 14 篇 · [事务与 OCC](https://quant67.com/post/db/rocksdb/14-transactions/14-transactions.html) | `OptimisticTransactionDB` |
> | 第 15 篇 · [Checkpoint 与 Ingest](https://quant67.com/post/db/rocksdb/15-checkpoint-ingest/15-checkpoint-ingest.html) | 硬链接快照 |

> **版本锚定** ：RocksDB **9.x** （ `facebook/rocksdb` ，Wiki 与 `include/rocksdb/*.h` ）；Flink **1.20+** （CF 映射引用官方 *State Backends* 文档，B 级）。本篇不粘贴未实测的 WAL 回收延迟数字。
> 
> 数据管理

---

## 一、问题：单 LSM 树不够用时拆什么

LevelDB 只有 **default** 一棵 LSM：comparator、memtable 大小、compression、compaction 策略全库统一。 [第 3 篇](https://quant67.com/post/db/rocksdb/03-rocksdb-architecture/03-rocksdb-architecture.html) 已把 CF 标为相对 LevelDB 的核心 diff 之一。生产嵌入的典型诉求：

| 诉求 | 单 CF 的困难 | CF 提供的抽象 |
| --- | --- | --- |
| 不同 state 变量隔离 scan | 同一 Iterator 扫全库 | 每 CF 独立 LSM，点查/范围扫限定在 CF 内 |
| 按模块调 compaction | 全局 `compaction_style` | `ColumnFamilyOptions` per-CF |
| 逻辑删除一组 [数据](#) | 逐 key Delete | `DropColumnFamily` 快速丢弃整棵子树 |
| 跨模块原子更新 | 只能靠 `WriteBatch` | 仍用 `WriteBatch` ，但可一次写多个 CF |

CF **不是** 多进程隔离，也 **不是** 独立 WAL 目录；它是 **同一 `DB` 指针下的逻辑分区** ， [磁盘](#) 上仍共用一个 DB 目录（ `MANIFEST` 全局一份，见 [第 6 篇](https://quant67.com/post/db/rocksdb/06-sst-manifest/06-sst-manifest.html) ）。

数据管理

---

## 二、共享 WAL、独立 LSM：磁盘与内存布局

Wiki *Column Families* 的实现要点（A 级）：

> Column Families **share the write-ahead log** and **don’t share memtables and table files**.

<svg id="mermaid-diagram-1-0" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 1217.1953125px;" viewBox="0 0 1217.1953125 482" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="mermaid-diagram-1-0_flowchart-v2-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-diagram-1-0_flowchart-v2-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-diagram-1-0_flowchart-v2-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-diagram-1-0_flowchart-v2-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><marker id="mermaid-diagram-1-0_flowchart-v2-circleEnd" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-diagram-1-0_flowchart-v2-circleStart" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-diagram-1-0_flowchart-v2-circleEnd-margin" viewBox="0 0 10 10" refY="5" refX="12.25" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-diagram-1-0_flowchart-v2-circleStart-margin" viewBox="0 0 10 10" refX="-2" refY="5" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-diagram-1-0_flowchart-v2-crossEnd" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-diagram-1-0_flowchart-v2-crossStart" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-diagram-1-0_flowchart-v2-crossEnd-margin" viewBox="0 0 15 15" refX="17.7" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" style="stroke-width: 2.5;"></path></marker><marker id="mermaid-diagram-1-0_flowchart-v2-crossStart-margin" viewBox="0 0 15 15" refX="-3.5" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" style="stroke-width: 2.5; stroke-dasharray: 1, 0;"></path></marker><g><g><g id="mermaid-diagram-1-0-DB" data-look="classic"><rect style="" x="8" y="112" width="1201.1953125" height="362"></rect><g transform="translate(530, 112)"><foreignObject width="157.1953125" height="24"><p>单个 RocksDB DB 实例</p></foreignObject></g></g><g id="mermaid-diagram-1-0-CF2" data-look="classic"><rect style="" x="28" y="241" width="462.1640625" height="208"></rect><g transform="translate(180.70703125, 241)"><foreignObject width="156.75" height="24"><p>Column Family: count</p></foreignObject></g></g><g id="mermaid-diagram-1-0-CF1" data-look="classic"><rect style="" x="727.03125" y="241" width="462.1640625" height="208"></rect><g transform="translate(874.0234375, 241)"><foreignObject width="168.1796875" height="24"><p>Column Family: default</p></foreignObject></g></g></g><g><path d="M608.598,62L608.598,66.167C608.598,70.333,608.598,78.667,608.598,87C608.598,95.333,608.598,103.667,608.598,111.333C608.598,119,608.598,126,608.598,129.5L608.598,133" id="mermaid-diagram-1-0-L_Write_WAL_0" style=";" data-edge="true" data-et="edge" data-id="L_Write_WAL_0" data-points="W3sieCI6NjA4LjU5NzY1NjI1LCJ5Ijo2Mn0seyJ4Ijo2MDguNTk3NjU2MjUsInkiOjg3fSx7IngiOjYwOC41OTc2NTYyNSwieSI6MTEyfSx7IngiOjYwOC41OTc2NTYyNSwieSI6MTM3fV0=" data-look="classic" marker-end="url(#mermaid-diagram-1-0_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M696.742,174.067L757.936,181.056C819.13,188.045,941.518,202.022,1002.712,213.178C1063.906,224.333,1063.906,232.667,1063.906,240.333C1063.906,248,1063.906,255,1063.906,258.5L1063.906,262" id="mermaid-diagram-1-0-L_WAL_M1_0" style=";" data-edge="true" data-et="edge" data-id="L_WAL_M1_0" data-points="W3sieCI6Njk2Ljc0MjE4NzUsInkiOjE3NC4wNjY4MzMxMDU5ODA2Nn0seyJ4IjoxMDYzLjkwNjI1LCJ5IjoyMTZ9LHsieCI6MTA2My45MDYyNSwieSI6MjQxfSx7IngiOjEwNjMuOTA2MjUsInkiOjI2Nn1d" data-look="classic" marker-end="url(#mermaid-diagram-1-0_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M520.453,174.067L459.259,181.056C398.065,188.045,275.677,202.022,214.483,213.178C153.289,224.333,153.289,232.667,153.289,240.333C153.289,248,153.289,255,153.289,258.5L153.289,262" id="mermaid-diagram-1-0-L_WAL_M2_0" style=";" data-edge="true" data-et="edge" data-id="L_WAL_M2_0" data-points="W3sieCI6NTIwLjQ1MzEyNSwieSI6MTc0LjA2NjgzMzEwNTk4MDY2fSx7IngiOjE1My4yODkwNjI1LCJ5IjoyMTZ9LHsieCI6MTUzLjI4OTA2MjUsInkiOjI0MX0seyJ4IjoxNTMuMjg5MDYyNSwieSI6MjY2fV0=" data-look="classic" marker-end="url(#mermaid-diagram-1-0_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M1063.906,320L1063.906,324.167C1063.906,328.333,1063.906,336.667,1063.906,344.333C1063.906,352,1063.906,359,1063.906,362.5L1063.906,366" id="mermaid-diagram-1-0-L_M1_S1_0" style=";" data-edge="true" data-et="edge" data-id="L_M1_S1_0" data-points="W3sieCI6MTA2My45MDYyNSwieSI6MzIwfSx7IngiOjEwNjMuOTA2MjUsInkiOjM0NX0seyJ4IjoxMDYzLjkwNjI1LCJ5IjozNzB9XQ==" data-look="classic" marker-end="url(#mermaid-diagram-1-0_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M153.289,320L153.289,324.167C153.289,328.333,153.289,336.667,153.289,344.333C153.289,352,153.289,359,153.289,362.5L153.289,366" id="mermaid-diagram-1-0-L_M2_S2_0" style=";" data-edge="true" data-et="edge" data-id="L_M2_S2_0" data-points="W3sieCI6MTUzLjI4OTA2MjUsInkiOjMyMH0seyJ4IjoxNTMuMjg5MDYyNSwieSI6MzQ1fSx7IngiOjE1My4yODkwNjI1LCJ5IjozNzB9XQ==" data-look="classic" marker-end="url(#mermaid-diagram-1-0_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M842.824,320L842.824,324.167C842.824,328.333,842.824,336.667,818.343,346.268C793.862,355.87,744.899,366.74,720.418,372.175L695.936,377.61" id="mermaid-diagram-1-0-L_V1_MAN_0" style=";" data-edge="true" data-et="edge" data-id="L_V1_MAN_0" data-points="W3sieCI6ODQyLjgyNDIxODc1LCJ5IjozMjB9LHsieCI6ODQyLjgyNDIxODc1LCJ5IjozNDV9LHsieCI6NjkyLjAzMTI1LCJ5IjozNzguNDc3MTM1NTE5MTYyMX1d" data-look="classic" marker-end="url(#mermaid-diagram-1-0_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M374.371,320L374.371,324.167C374.371,328.333,374.371,336.667,398.852,346.268C423.334,355.87,472.296,366.74,496.778,372.175L521.259,377.61" id="mermaid-diagram-1-0-L_V2_MAN_0" style=";" data-edge="true" data-et="edge" data-id="L_V2_MAN_0" data-points="W3sieCI6Mzc0LjM3MTA5Mzc1LCJ5IjozMjB9LHsieCI6Mzc0LjM3MTA5Mzc1LCJ5IjozNDV9LHsieCI6NTI1LjE2NDA2MjUsInkiOjM3OC40NzcxMzU1MTkxNjIxfV0=" data-look="classic" marker-end="url(#mermaid-diagram-1-0_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path></g><g><g><g data-id="L_Write_WAL_0" transform="translate(0, 0)"></g></g><g><g data-id="L_WAL_M1_0" transform="translate(0, 0)"></g></g><g><g data-id="L_WAL_M2_0" transform="translate(0, 0)"></g></g><g><g data-id="L_M1_S1_0" transform="translate(0, 0)"></g></g><g><g data-id="L_M2_S2_0" transform="translate(0, 0)"></g></g><g><g data-id="L_V1_MAN_0" transform="translate(0, 0)"></g></g><g><g data-id="L_V2_MAN_0" transform="translate(0, 0)"></g></g></g><g><g id="mermaid-diagram-1-0-flowchart-WAL-0" data-look="classic" transform="translate(608.59765625, 164)"><rect style="" x="-88.14453125" y="-27" width="176.2890625" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-58.14453125, -12)"><rect></rect><foreignObject width="116.2890625" height="24"><p>共享 WAL (*.log)</p></foreignObject></g></g><g id="mermaid-diagram-1-0-flowchart-M1-1" data-look="classic" transform="translate(1063.90625, 293)"><rect style="" x="-90.2890625" y="-27" width="180.578125" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-60.2890625, -12)"><rect></rect><foreignObject width="120.578125" height="24"><p>MemTable / imm</p></foreignObject></g></g><g id="mermaid-diagram-1-0-flowchart-V1-2" data-look="classic" transform="translate(842.82421875, 293)"><rect style="" x="-80.79296875" y="-27" width="161.5859375" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-50.79296875, -12)"><rect></rect><foreignObject width="101.5859375" height="24"><p>Version L0..Ln</p></foreignObject></g></g><g id="mermaid-diagram-1-0-flowchart-S1-3" data-look="classic" transform="translate(1063.90625, 397)"><rect style="" x="-45.5234375" y="-27" width="91.046875" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-15.5234375, -12)"><rect></rect><foreignObject width="31.046875" height="24"><p>*.sst</p></foreignObject></g></g><g id="mermaid-diagram-1-0-flowchart-M2-4" data-look="classic" transform="translate(153.2890625, 293)"><rect style="" x="-90.2890625" y="-27" width="180.578125" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-60.2890625, -12)"><rect></rect><foreignObject width="120.578125" height="24"><p>MemTable / imm</p></foreignObject></g></g><g id="mermaid-diagram-1-0-flowchart-V2-5" data-look="classic" transform="translate(374.37109375, 293)"><rect style="" x="-80.79296875" y="-27" width="161.5859375" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-50.79296875, -12)"><rect></rect><foreignObject width="101.5859375" height="24"><p>Version L0..Ln</p></foreignObject></g></g><g id="mermaid-diagram-1-0-flowchart-S2-6" data-look="classic" transform="translate(153.2890625, 397)"><rect style="" x="-45.5234375" y="-27" width="91.046875" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-15.5234375, -12)"><rect></rect><foreignObject width="31.046875" height="24"><p>*.sst</p></foreignObject></g></g><g id="mermaid-diagram-1-0-flowchart-MAN-7" data-look="classic" transform="translate(608.59765625, 397)"><rect style="" x="-83.43359375" y="-27" width="166.8671875" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-53.43359375, -12)"><rect></rect><foreignObject width="106.8671875" height="24"><p>全局 MANIFEST</p></foreignObject></g></g><g id="mermaid-diagram-1-0-flowchart-Write-8" data-look="classic" transform="translate(608.59765625, 35)"><rect style="" x="-102.109375" y="-27" width="204.21875" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-72.109375, -12)"><rect></rect><foreignObject width="144.21875" height="24"><p>WriteBatch 多 CF 写</p></foreignObject></g></g></g></g></g><defs></defs><defs></defs></svg>

一次 `DB::Write` 把整批 `WriteBatch` 追加到 **当前活跃 WAL** ；recovery 时按 batch 里的 **CF id** 把记录 replay 到 **各自 CF 的 MemTable** （ [第 4 篇](https://quant67.com/post/db/rocksdb/04-wal-writebatch/04-wal-writebatch.html) ）。读路径上，每个 CF 持有独立 **SuperVersion** （mem + imm + `Version` ）， [第 7 篇](https://quant67.com/post/db/rocksdb/07-get-snapshot/07-get-snapshot.html) 的 `GetImpl` 需传入 `ColumnFamilyHandle*` 才能定位正确 LSM。

**原子写跨 CF** ： `WriteBatch` 可含 `{cf1,k1,v1}` 与 `{cf2,k2,v2}` ；要么整批 commit，要么都不生效——依赖 **单 WAL 顺序 + 单 sequence 空间** ，而非 per-CF WAL。

---

## 三、WAL 回收与 max\_total\_wal\_size

共享 WAL 带来 **回收耦合** ：某个 CF flush 后，WAL 里仍可能有 **其他 CF 未落盘** 的数据，旧 WAL 不能删。

拼车

Wiki 说明（A 级）：

- **任一 CF flush 时可能切换新 WAL** ；新写入进新文件。
- 旧 WAL 仅当 **所有 CF 都已 flush 且其中数据全部进入 SST** 后才可删除。
- 应定期 flush 各 CF； `DBOptions::max_total_wal_size` 可在 WAL 过大时 **自动 flush 滞后的 CF** 。

[工程](#) 含义：Flink 多 CF 作业若某一 state 写入很少、长期不 flush，会 **拖住 WAL 体积** ，间接影响 checkpoint 与磁盘占用——这与 [stream/13 状态调优](https://quant67.com/post/db/stream-processing/13-state-tuning/13-state-tuning.html) 里「多 CF 共享 WAL」的调参点一致。本篇只钉机制，不展开 Flink 指标。

---

## 四、ColumnFamilyHandle 与 Open 语义

`ColumnFamilyHandle` 类似 **已打开的 CF 文件描述符** （Wiki 用语）。要点：

| API / 行为 | 说明 |
| --- | --- |
| `DB::Open(..., vector<ColumnFamilyDescriptor>, handles)` | 读写打开须 **列出 DB 中现有全部 CF** ，否则 `InvalidArgument` |
| `DB::OpenForReadOnly` | 可只打开 **CF 子集** |
| `DB::ListColumnFamilies` | 静态方法，枚举磁盘上 CF 名 |
| `CreateColumnFamily` / `DropColumnFamily` | 在线增删；Drop 后若仍有 Handle 引用， **[数据](#) 延迟删除** |
| `delete handle` | 关闭前须释放 **所有** Handle，再 `delete db` |

`WriteBatch::Put(ColumnFamilyHandle*, ...)` 、 `Get/Iterator/NewIterator` 等均需显式 CF 参数。默认 CF 名为 `"default"` ；仅用旧 API（无 CF 参数）的代码等价于 **只写 default** （Wiki *Backward compatibility* ）。

**Drop 语义** ： `DropColumnFamily` 后 Handle 仍可对 **已 drop CF** 读写，直到最后一个 Handle 释放——便于滚动升级时排空引用，但运维上容易误判「已删仍在用」。

---

## 五、选项分层：DBOptions 与 ColumnFamilyOptions

RocksDB 3.0 起把 Options 拆成两层（ `include/rocksdb/options.h` ，A 级）：

| 结构 | 作用域 | 典型字段 |
| --- | --- | --- |
| `DBOptions` | 整库 | `max_background_jobs` 、 `wal_dir` 、 `rate_limiter` 、 `statistics` |
| `ColumnFamilyOptions` | 单 CF | `write_buffer_size` 、 `compaction_style` 、 `comparator` 、 `table_factory` |
| `Options` | 继承二者 | 单 CF 或 default CF 的便捷写法 |

`ColumnFamilyDescriptor` = **CF 名 + `ColumnFamilyOptions`** ，在 `Open` 时成批传入。不同 CF 可配置 **不同 leveled/universal 策略、不同 bloom、不同 TTL** （ [第 10–11 篇](https://quant67.com/post/db/rocksdb/10-leveled-compaction/10-leveled-compaction.html) 的 picker 按 CF 独立运行）。

**Comparator 约束** ：同一 DB 内各 CF **可以** 使用不同 comparator（按 CF 配置）； `SstFileWriter` / external ingest 时 comparator 必须与目标 CF **完全一致** （ [第 15 篇](https://quant67.com/post/db/rocksdb/15-checkpoint-ingest/15-checkpoint-ingest.html) ）。

---

## 六、MANIFEST 与多 CF 版本链

[第 6 篇](https://quant67.com/post/db/rocksdb/06-sst-manifest/06-sst-manifest.html) 已述：MANIFEST **全局一份** ， `VersionEdit` 带 **`kColumnFamily`** 区分 CF； `VersionSet::ColumnFamilySet` 维护 `ColumnFamilyData → Version*` 链表。

Flush / compaction 提交时， `LogAndApply` 可一次写入 **多 CF 的 Edit 组** （ `kInAtomicGroup` ），保证 **跨 CF 的元数据视图一致切换** 。读侧每个 CF 的 SuperVersion 独立切换； **不存在** 「一个 CF 看到新 SST、另一个仍见旧 Version」的半套状态（在同一 `GetAndRefSuperVersion(cf)` 调用内）。

---

## 七、Flink 多 state 变量 → 多 Column Family

Flink `EmbeddedRocksDBStateBackend` 的映射规则（Apache Flink 文档 *State Backends* → *Predefined Per-ColumnFamily Options* ，B 级）：

> **当前实现中，算子里的每一种 registered state 对应一个 RocksDB Column Family。**

示例：同一窗口算子注册 `ValueStateDescriptor("count")` 与 `MapStateDescriptor("user-last-seen")` → 该 subtask 的 RocksDB 至少 **两个业务 CF** （另加 RocksDB 内置 `default` ，通常不参与 Flink 状态）。

<svg id="mermaid-diagram-1-1" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 532.390625px;" viewBox="0 0 532.390625 437" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="mermaid-diagram-1-1_flowchart-v2-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-diagram-1-1_flowchart-v2-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-diagram-1-1_flowchart-v2-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-diagram-1-1_flowchart-v2-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><marker id="mermaid-diagram-1-1_flowchart-v2-circleEnd" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-diagram-1-1_flowchart-v2-circleStart" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-diagram-1-1_flowchart-v2-circleEnd-margin" viewBox="0 0 10 10" refY="5" refX="12.25" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-diagram-1-1_flowchart-v2-circleStart-margin" viewBox="0 0 10 10" refX="-2" refY="5" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-diagram-1-1_flowchart-v2-crossEnd" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-diagram-1-1_flowchart-v2-crossStart" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-diagram-1-1_flowchart-v2-crossEnd-margin" viewBox="0 0 15 15" refX="17.7" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" style="stroke-width: 2.5;"></path></marker><marker id="mermaid-diagram-1-1_flowchart-v2-crossStart-margin" viewBox="0 0 15 15" refX="-3.5" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" style="stroke-width: 2.5; stroke-dasharray: 1, 0;"></path></marker><g><g><g id="mermaid-diagram-1-1-RDB" data-look="classic"><rect style="" x="8" y="97" width="516.390625" height="332"></rect><g transform="translate(207.77734375, 97)"><foreignObject width="116.8359375" height="24"><p>subtask RocksDB</p></foreignObject></g></g></g><g><path d="M153.348,62L167.51,74.667C181.672,87.333,209.996,112.667,236.588,127.158C263.18,141.65,288.039,145.3,300.468,147.124L312.898,148.949" id="mermaid-diagram-1-1-L_OP_CFc_0" style=";" data-edge="true" data-et="edge" data-id="L_OP_CFc_0" data-points="W3sieCI6MTUzLjM0Nzc3MDAyNDI3MTg1LCJ5Ijo2Mn0seyJ4IjoyMzguMzIwMzEyNSwieSI6MTM4fSx7IngiOjMxNi44NTU0Njg3NSwieSI6MTQ5LjUzMDMwMDEzMzgxNzYzfV0=" data-look="classic" marker-end="url(#mermaid-diagram-1-1_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M139.877,62L156.284,88.5C172.691,115,205.506,168,229.787,196.812C254.069,225.624,269.818,230.249,277.692,232.561L285.566,234.873" id="mermaid-diagram-1-1-L_OP_CFm_0" style=";" data-edge="true" data-et="edge" data-id="L_OP_CFm_0" data-points="W3sieCI6MTM5Ljg3Njk1MzEyNSwieSI6NjJ9LHsieCI6MjM4LjMyMDMxMjUsInkiOjIyMX0seyJ4IjoyODkuNDA0Mjk2ODc1LCJ5IjoyMzZ9XQ==" data-look="classic" marker-end="url(#mermaid-diagram-1-1_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M182.955,226L192.182,221.833C201.41,217.667,219.865,209.333,241.542,201.511C263.219,193.689,288.118,186.378,300.568,182.722L313.018,179.066" id="mermaid-diagram-1-1-L_WAL_CFc_0" style=";" data-edge="true" data-et="edge" data-id="L_WAL_CFc_0" data-points="W3sieCI6MTgyLjk1NDg1Mjc2NDQyMzEsInkiOjIyNn0seyJ4IjoyMzguMzIwMzEyNSwieSI6MjAxfSx7IngiOjMxNi44NTU0Njg3NSwieSI6MTc3LjkzOTM5OTczMjM2NDczfV0=" data-look="classic" marker-end="url(#mermaid-diagram-1-1_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M160.622,280L173.572,289.333C186.521,298.667,212.421,317.333,239.799,319.303C267.177,321.273,296.033,306.546,310.461,299.182L324.889,291.818" id="mermaid-diagram-1-1-L_WAL_CFm_0" style=";" data-edge="true" data-et="edge" data-id="L_WAL_CFm_0" data-points="W3sieCI6MTYwLjYyMTg5MzgyNTMwMTIsInkiOjI4MH0seyJ4IjoyMzguMzIwMzEyNSwieSI6MzM2fSx7IngiOjMyOC40NTIwNTQ3OTQ1MjA1NiwieSI6MjkwfV0=" data-look="classic" marker-end="url(#mermaid-diagram-1-1_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path></g><g><g><g data-id="L_OP_CFc_0" transform="translate(0, 0)"></g></g><g><g data-id="L_OP_CFm_0" transform="translate(0, 0)"></g></g><g><g data-id="L_WAL_CFc_0" transform="translate(0, 0)"></g></g><g><g data-id="L_WAL_CFm_0" transform="translate(0, 0)"></g></g></g><g><g id="mermaid-diagram-1-1-flowchart-OP-0" data-look="classic" transform="translate(123.16015625, 35)"><rect style="" x="-90.16015625" y="-27" width="180.3203125" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-60.16015625, -12)"><rect></rect><foreignObject width="120.3203125" height="24"><p>WindowOperator</p></foreignObject></g></g><g id="mermaid-diagram-1-1-flowchart-CFc-1" data-look="classic" transform="translate(381.35546875, 159)"><rect style="" x="-64.5" y="-27" width="129" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-34.5, -12)"><rect></rect><foreignObject width="69" height="24"><p>CF: count</p></foreignObject></g></g><g id="mermaid-diagram-1-1-flowchart-CFm-2" data-look="classic" transform="translate(381.35546875, 263)"><rect style="" x="-94.59765625" y="-27" width="189.1953125" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-64.59765625, -12)"><rect></rect><foreignObject width="129.1953125" height="24"><p>CF: user-last-seen</p></foreignObject></g></g><g id="mermaid-diagram-1-1-flowchart-WAL-3" data-look="classic" transform="translate(123.16015625, 253)"><rect style="" x="-63.61328125" y="-27" width="127.2265625" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-33.61328125, -12)"><rect></rect><foreignObject width="67.2265625" height="24"><p>共享 WAL</p></foreignObject></g></g><g id="mermaid-diagram-1-1-flowchart-BC-4" data-look="classic" transform="translate(381.35546875, 367)"><rect style="" x="-118.03515625" y="-27" width="236.0703125" height="54" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-88.03515625, -12)"><rect></rect><foreignObject width="176.0703125" height="24"><p>共享 Block Cache / WBM</p></foreignObject></g></g></g></g></g><defs></defs><defs></defs></svg>

与内核机制的对应关系：

| Flink 概念 | RocksDB 机制 |
| --- | --- |
| 多种 state 变量 | 多 CF，独立 LSM |
| KeyGroup 前缀 | **user key 编码** ，不是 CF 边界（ [stream/12](https://quant67.com/post/db/stream-processing/12-rocksdb-state-backend/12-rocksdb-state-backend.html) ） |
| 增量 checkpoint | 上传 **不可变 SST** ；依赖 CF 内 SST 与全局 MANIFEST 语义（第 15 篇 Checkpoint） |
| `RocksDBOptionsFactory` | 按 CF 名返回不同 `ColumnFamilyOptions` |

**分工** ：stream/12 讲作业布局与 KeyGroup；本篇讲 **为何 Flink 选 CF 而非 key 前缀分 state** ——便于 per-state TTL compact filter、savepoint 元 [数据](#) 对齐、以及缩小单次 Iterator 扫描范围。第 16 篇将把 TiKV / Kafka Streams 一并对照。

---

## 八、API 示例：Open 与跨 CF 原子写

```cpp
#include "rocksdb/db.h"
#include "rocksdb/options.h"

DBOptions db_opts;
std::vector<ColumnFamilyDescriptor> cfs{
    {"default", ColumnFamilyOptions{}},
    {"metrics", ColumnFamilyOptions{}},
};
std::vector<ColumnFamilyHandle*> handles;
rocksdb::DB* db;
auto s = DB::Open(db_opts, "/tmp/cf_demo", cfs, &handles, &db);

WriteBatch batch;
batch.Put(handles[0], "k1", "v1");
batch.Put(handles[1], "m1", "100");
WriteOptions wopts;
s = db->Write(wopts, &batch);  // 单 WAL 记录，原子跨 CF

db->DropColumnFamily(handles[1]);
for (auto* h : handles) delete h;
delete db;
```

（示例仅说明 API 形状；路径与错误处理从简。）

---

## 九、与 LevelDB / 单 CF 心智的对照

| 维度 | LevelDB | RocksDB 多 CF |
| --- | --- | --- |
| WAL | 1 份 | **仍 1 份** ，全 CF 共享 |
| MemTable / SST | 1 套 | **每 CF 一套** |
| MANIFEST | 1 份 | **1 份** ，Edit 带 CF id |
| Open | 无 CF 列表 | 读写须枚举已有 CF |
| 原子批写 | `WriteBatch` | `WriteBatch` + 多 CF handle |

### 9.1 设计争论：CF vs 多 DB

| 方案 | 优点 | 代价 |
| --- | --- | --- |
| **Column Family** （RocksDB Wiki, A 级） | 共享 WAL、 **一次 `WriteBatch` 跨 CF 原子** 、统一 MANIFEST | 共享 `WriteController` stall； **最慢 flush CF 拖 WAL 回收** |
| **多 DB 实例** | CF 间 I/O 与 stall **硬隔离** | 无跨库原子批；运维与文件句柄翻倍 |

TiKV / Flink 选 CF 是为 **模块隔离 + 单进程嵌入** （ [第 16 篇](https://quant67.com/post/db/rocksdb/16-embedded-production/16-embedded-production.html) ），不是论文结论—— **热点 CF L0 爆炸** 仍可能通过共享 stall 影响全局（ [第 11 篇](https://quant67.com/post/db/rocksdb/11-universal-stall/11-universal-stall.html) §7.1）。

**开放问题** ：能否 **per-CF RateLimiter / stall 配额** 实现公平背压？社区 issue 讨论多， **无默认产品行为** 。

---

## 十、小结

- **Column Family** = 共享 WAL + 独立 MemTable/SST/Version/SuperVersion 的逻辑分区。
- **`ColumnFamilyHandle`** 管理 CF 生命周期；Drop 后延迟删数据直至 Handle 归零。
- **`DBOptions` / `ColumnFamilyOptions`** 拆分库级与 CF 级调参；Flink 为 **每种 registered state 建一个 CF** 。
- **WAL 回收** 受最慢 flush 的 CF 牵制； `max_total_wal_size` 用于自动 flush 落后 CF。
- 读路径、compaction、checkpoint 均须在 **正确 CF 上下文** 下理解——后续事务（第 14 篇）与 ingest（第 15 篇）同样依赖 CF 边界。

---

**上一篇** ： [并发 Compaction 与 Rate Limiter](https://quant67.com/post/db/rocksdb/12-concurrent-ratelimit/12-concurrent-ratelimit.html)

**下一篇** ： [事务与 OptimisticTransactionDB](https://quant67.com/post/db/rocksdb/14-transactions/14-transactions.html)

---

## 参考资料

1. RocksDB Wiki, *Column Families* （共享 WAL、flush 与 WAL 删除、 `max_total_wal_size` ；A 级）。
2. RocksDB 9.x 源码： `db/column_family.h` 、 `db/column_family.cc` （ `ColumnFamilyData` 、 `SuperVersion` ）； `db/version_set.cc` （ `ColumnFamilySet` 、 `LogAndApply` ）； `include/rocksdb/options.h` （ `DBOptions` 、 `ColumnFamilyOptions` ）（A 级）。
3. RocksDB 9.x 源码： `include/rocksdb/db.h` （ `Open` 、 `CreateColumnFamily` 、 `DropColumnFamily` 、 `ListColumnFamilies` ）（A 级）。
4. Apache Flink 文档, *State Backends* → *Predefined Per-ColumnFamily Options* （每种 registered state 对应一个 CF；B 级）。
5. [stream-processing 第 12 篇：RocksDB State Backend](https://quant67.com/post/db/stream-processing/12-rocksdb-state-backend/12-rocksdb-state-backend.html) ； [第 6 篇 MANIFEST](https://quant67.com/post/db/rocksdb/06-sst-manifest/06-sst-manifest.html) ； [第 4 篇 WAL](https://quant67.com/post/db/rocksdb/04-wal-writebatch/04-wal-writebatch.html) 。