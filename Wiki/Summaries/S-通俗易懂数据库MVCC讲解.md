---
id: S-通俗易懂数据库MVCC讲解
title: InnoDB MVCC：多版本并发控制原理与隔离级别实现
author: 腾讯云开发者社区
source: https://cloud.tencent.com/developer/article/1698716
date: 2026-04-05
tags:
  - database
---

## 核心结论

1. **MVCC 的核心价值**：将"读-写冲突"从悲观锁（互斥阻塞）转化为乐观并发——读操作读取历史快照（不加锁），写操作创建新版本，通过版本链和 Read View 实现读写不互斥，从而大幅提升并发性能。
2. **Read View 是 MVCC 的可见性判断引擎**：快照读时生成 Read View（记录当前活跃事务ID集合），通过 db_trx_id 与 up_limit_id / low_limit_id / trx_ids 的比较，决定当前事务能看到哪个版本的记录——RC 和 RR 的根本区别在于 Read View 的生成时机。
3. **MVCC + 锁 = 完整并发控制**：MVCC 解决读写冲突，悲观锁/乐观锁解决写-写冲突，两者组合才能保证脏读、幻读、不可重复读的同时支持。

## 关键数据

- **隐藏字段**：db_trx_id（最近修改事务ID）、db_roll_pointer（回滚指针，指向 undo 日志链）、db_row_id（隐式主键）、delete_flag（删除标记）
- **版本链**：每条记录通过 db_roll_pointer 串联 undo 日志形成版本链，头节点是最新的记录
- **Read View 字段**：trx_ids（活跃事务ID集合）、low_limit_id（最大事务ID+1）、up_limit_id（最小活跃事务ID）、creator_trx_id（当前事务ID）
- **可见性判断**：
  - db_trx_id < up_limit_id 或 db_trx_id == creator_trx_id → 可见
  - db_trx_id >= low_limit_id → 不可见（事务在当前 Read View 之后启动）
  - db_trx_id 在 trx_ids 中 → 不可见（事务尚未提交）
- **RC vs RR**：RC 每次快照读生成新 Read View → 每次读可看到最新提交；RR 同一事务第一次快照读创建 Read View，后续复用 → 同一事务每次读结果一致

## 疑点 / 待验证

- **MVCC 与事务回滚的交互**：长事务持有旧的 Read View，在回滚段积累大量 undo 日志时，对其他事务的可见性判断性能影响是否有量化数据。
- **Purge 线程的行为**：update undo log 在快照读不再需要时才能被 purge，多个长事务同时存在时 undo 日志保留策略是否会引发存储膨胀。
- **写-写冲突的实际处理**：MVCC 本身不处理写-写冲突（Last Write Wins 或悲观锁），不同数据库（MySQL vs PostgreSQL）的具体处理策略差异。

## 术语表

- **MVCC（Multi-Version Concurrency Control）**：多版本并发控制，为每个数据修改保存一个版本（与事务时间戳关联），读操作只读取事务开始前的数据库快照，实现读-写不互斥。
- **当前读（Current Read）**：读取最新版本的记录，会加锁（悲观锁），如 SELECT ... FOR UPDATE / LOCK IN SHARE MODE。
- **快照读（Snapshot Read）**：读取历史版本，不加锁，性能高，是 MVCC 的具体实现方式，如普通 SELECT。
- **版本链（Version Chain）**：每条记录通过 db_roll_pointer 串联所有历史版本（存储于 undo log），形成从新到旧的单向链表。
- **Undo Log**：记录数据修改前的值，用于事务回滚和快照读的历史版本获取；update undo log 在快照读和回滚都不需要时才能被 purge。
- **Read View（读视图）**：快照读时生成的一致性快照，包含当前活跃事务ID集合和事务ID边界，是 MVCC 可见性判断的核心数据结构。
- **Read Committed（RC）**：每次快照读生成新 Read View，可看到其他事务最新提交的修改。
- **Repeatable Read（RR）**：同一事务首次快照读创建 Read View，后续复用，同一事务内每次读结果一致。

## 原始来源

[[Clippings/通俗易懂数据库MVCC讲解.md]]
