---
id: C-ColumnFamily
title: Column Family（CF）
reference: Clippings/【RocksDB 内核机制】Column Family：共享 WAL 与独立 LSM.md
updated: 2026-08-17
---

## 定义

Column Family（CF）是 RocksDB 在 LevelDB 单 LSM 模型之上的逻辑分区机制：从 RocksDB 3.0 起，每个 key-value 恰属一个 CF，**WAL 整库共享**，**MemTable / SST / Version 链按 CF 独立**。CF 让多个逻辑数据集共用同一 DB 进程、共享原子写能力，又能各自配置 compaction 策略、comparator、TTL。

## 关联来源

[[Clippings/【RocksDB 内核机制】Column Family：共享 WAL 与独立 LSM.md]]

## 已知边界 / 局限

- **Stall 联动**：共享 `WriteController` 与 WAL 意味着单 CF 写爆炸（如 L0 堆积）会 stall 所有 CF 写入；社区讨论"per-CF RateLimiter"但无默认产品行为。
- **WAL 回收受最慢 CF 牵制**：任一 CF 不 flush 即便其他 CF 早已落盘，旧 WAL 也不能删，对磁盘占用与 checkpoint 时延有放大效应。
- **Open 时必须枚举所有 CF**：`DB::Open(..., vector<ColumnFamilyDescriptor>, handles)` 缺一个 CF 名就报 `InvalidArgument`，新增/删除 CF 需修改调用代码。
- **Drop 延迟删除**：`DropColumnFamily` 后数据延迟删除直至所有 Handle 引用归零，运维监控"何时真的释放磁盘"存在迷惑性。
- **不是多进程隔离**：CF 是同一 `DB*` 下的逻辑分区，不跨进程；磁盘仍共用一个 DB 目录。

## 实际案例

- **TiKV**：每个 Region 本地引擎用 CF 隔离 raft log / kv data / lock 三类数据，共享 WAL 让一次 `WriteBatch` 跨 CF 原子提交，简化事务协议。
- **Apache Flink**：`EmbeddedRocksDBStateBackend` 把算子里每种 registered state 映射到一个 CF，便于 per-state TTL compact filter 与 savepoint 元数据对齐。
- **RocksDB Java/Go binding**：通过 `ColumnFamilyHandle` 暴露的 API 形态成为嵌入式 KV 库的"事实标准"，被 CockroachDB、Dgraph 等数据库采用。
- **Checkpoint/Ingest**：外部 SST 写入（`SstFileWriter`）要求 comparator 与目标 CF 完全一致；Flink 增量 checkpoint 上传不可变 SST 也是建立在 CF 内 SST + 全局 MANIFEST 语义之上。