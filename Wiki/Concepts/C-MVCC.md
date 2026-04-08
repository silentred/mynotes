---
id: C-MVCC
title: MVCC 多版本并发控制
updated: 2026-04-08
---

## 定义

MVCC（Multi-Version Concurrency Control）是一种通过为每次数据修改保存一个版本（与事务时间戳关联），使读操作读取历史快照而不阻塞写操作的并发控制机制。InnoDB 通过版本链（db_roll_pointer 串联 undo log）和 Read View（记录活跃事务ID集合）实现，使读-写操作真正并行，大幅提升数据库并发性能。

## 关联来源

[[Clippings/通俗易懂数据库MVCC讲解.md]]

## 已知边界 / 局限

- **MVCC 不解决写-写冲突**：Last Write Wins 或悲观锁由上层机制处理，MVCC 只负责读视角的可见性
- **长事务的危害**：持有旧 Read View 会阻止 undo 日志被 purge，导致回滚段膨胀；长事务还会阻止其他事务看到最新提交的数据
- **RC vs RR 的选择**：RC 的每次新 Read View 可看到最新提交但可能出现幻读；RR 的同一 Read View 保证可重复读但可能导致读到较旧的数据
- **只解决了脏读/幻读/不可重复读**：无法解决"写-写更新丢失"问题，需要额外的锁机制（悲观锁 SELECT FOR UPDATE 或乐观锁版本号）

## 版本 / 演进

- **PostgreSQL MVCC**：采用 SSI（Serializable Snapshot Isolation）实现可串行化隔离级别，在 MVCC 基础上引入危险结构检测防止幻读
- **MySQL InnoDB MVCC**：基于隐藏字段（db_trx_id + db_roll_pointer）和 undo log 版本链，RC 和 RR 隔离级别下实现不同
- **SI（Snapshot Isolation）**：Oracle 和 PostgreSQL 早期使用，与 Read Committed 类似但快照基于事务开始时间
