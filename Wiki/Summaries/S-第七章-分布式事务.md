---

id: S-第七章-分布式事务

title: 分布式事务：ACID、并发控制与 BASE 理论

author: codedump

source: https://www.codedump.info/dist-system-cn/transaction/

date: 2026-04-08

tags:
  - distributed-sys
  - database
---

## 核心结论

1. **ACID 是单机事务的根基**：原子性依赖 Undo Log 实现回滚、持久性依赖 Redo Log（WAL）实现崩溃恢复；两者共同确保事务"要么全做、要么全不做"
2. **隔离性解决并发问题**：脏读、不可重复读、幻读三大异常；2PL（悲观）、OCC（乐观）、MVCC（多版本）三种并发控制方案；Serializable 为最强隔离级别
3. **分布式事务无银弹**：强一致性方案（2PC/3PC/Spanner）追求 ACID，代价是同步阻塞和单点故障；柔性事务（TCC/SAGA）基于 BASE 理论，放弃强一致性换取高可用性

## 关键数据

- **读未提交 / 读已提交 / 可重复读 / 可串行化**：四种隔离级别，从弱到强，逐级避免脏读→不可重复读→幻读
- **Undo Log + Redo Log**：原子性（失败回滚）和持久性（崩溃恢复）的底层机制
- **2ε Commit Wait**：Google Spanner 的 TrueTime 提交等待时间，ε 通常控制在毫秒级（约 4ms 平均）
- **SSI（可串行化快照隔离）**：PostgreSQL Serializable 级别使用，乐观检测写倾斜

## 疑点 / 待验证

- TCC/SAGA 对业务的侵入性在实际工程中如何权衡——高度标准化的支付/库存场景 vs 需要调用第三方服务的异构场景

## 术语表

- **ACID**：原子性（Atomicity）、一致性（Consistency）、隔离性（Isolation）、持久性（Durability）
- **Undo Log**：回滚日志，记录修改前的值，事务回滚时逆向恢复
- **Redo Log / WAL（预写日志）**：记录修改后的值，崩溃后重放以恢复已提交事务
- **2PL（两阶段锁）**：扩展阶段加锁、收缩阶段释放锁，避免脏读需用 SS2PL
- **OCC（乐观并发控制）**：读写不加锁，提交时验证读写集冲突，适合冲突率低场景
- **MVCC（多版本并发控制）**：读不阻塞写，写不阻塞读；快照隔离下仍有写倾斜问题
- **写倾斜（Write Skew）**：两个事务各自读取并修改不同数据，但全局约束被违反；MVCC 无法自动检测
- **BASE 理论**：基本可用（Basically Available）、柔性状态（Soft State）、最终一致性（Eventually Consistent）
- **2PC / 3PC**：两阶段/三阶段提交，刚性分布式事务代表；3PC 通过 CanCommit 询问阶段缓解部分问题
- **TrueTime**：Google Spanner 的物理时钟区间机制（GPS + 原子钟），ε 通常约 4ms
- **TCC（Try-Confirm-Cancel）**：资源预留型柔性事务，三阶段接口由业务实现；侵入性强但隔离性好
- **SAGA**：补偿型柔性事务，长流程拆分；正向恢复（重试）或反向恢复（补偿）；侵入性低但隔离性弱
- **Commit Wait**：Spanner 写事务提交前必须等待 ε 时间窗口，确保外部一致性

## 原始来源

[[第七章 事务]]
