---
title: "Rockraft：基于 OpenRaft 与 RocksDB 的强一致 KV 存储框架"
source: "https://www.codedump.info/zh/post/20260412-rockraft/"
author:
published: 2026-04-12
created: 2026-04-14
description: "动机 # Redis协议已经成为事实意义上的key-value存储协议标准。除了官方的Redis实现以外，我们看到还有各种兼容Redis协议的实现：Valkey：Linux基金会官方fork的Redis 7.2分支，采用BSD许可证，是Redis更换SSPL许可证后社区推出的真正开源替代方案，完全兼容Redis协议和持久化机制。 Dragonfly：追求极致性能的现代多线程内存数据库，可提供相比Redis高达25倍的吞吐量和更低的尾延迟，但采用BSL许可证（4年后转Apache 2.0）。 KeyDB：Snapchat收购维护的Redis多线程分支，在100%兼容Redis API的基础上增加了主动复制（Active Replication）和Flash存储扩展能力，但更新已放缓。 Kvrocks：Apache顶级项目，基于RocksDB实现数据持久化到磁盘的分布式KV存储，支持数十TB级数据且成本仅为内存方案的1/5-1/10，适合大容量低成本场景。 但是，上面的任何一个实现，都没有在分布式系统的强一致性上走得更远，在这个维度，它们依然采用了Redis原生实现的最终一致性。最开始，我创建coredb项目，是为了利用raft共识算法，实现一个满足强一致性且兼容redis协议的服务。我知道一定有人会有疑问：大家使用Redis类的系统，是为了缓存数据，在这类型的项目里，一般都会选择CAP中的AP，把可用性放在第一位，而非一致性。但是，回到文章最开始的结论：Redis协议已经成为事实意义上的key-value存储协议标准。如果在这个大前提下，它的生态价值不应仅仅局限于传统的内存缓存。通过为其引入强一致性的持久化存储，我们可以赋予它全新的生命力和应用场景——正如 HTTP 协议从早期的网页传输协议，最终演变为无处不在的通信基石一样。最开始，我构建的项目只有coredb，这是一个采用Raft算法+rocksdb的强一致且兼容Redis协议的服务，也就是说，可以继续使用redis客户端访问这个服务，但是它满足强一致性：只要数据写入时返回成功，意味着至少在集群中的半数以上节点写入成功。在开发过程中我意识到，“Raft + RocksDB” 的架构组合具有极高的通用价值。考虑到许多开发者可能也需要这样一套可靠的底层基座，去构建他们自己专属的强一致性存储系统，我便将这部分核心逻辑进行了解耦，单独抽离出了 Rockraft 这个基础框架项目。设计与实现 # Rockraft采用Rust开发，这是我目前最喜欢的系统编程语言：类型安全且内存安全，这两个特性是我最喜欢的Rust语言特性，有了这两个特性在编程时会更加放心。目前Rust语言的常见Raft实现有以下两个：raft-rs Rust生态中最成熟、生产验证最充分的Raft实现，被近千个生产环境采用。它源自etcd的Go实现移植，但完全用Rust重写，保证了线程安全和内存安全。架构特点：核心共识模块：仅提供纯共识算法核心（Raft状态机），不包含日志存储、网络传输或状态机实现 高度可定制：需自行实现Storage Trait（日志存储）和RaftMessage传输层，灵活性极高 多Raft支持：TiKV基于此实现了Multi-Raft架构，支持海量Region分片 功能完整性：✅ Leader选举、日志复制、成员变更（Joint Consensus） ✅ PreVote机制避免网络分区干扰 ✅ Leader Lease读取优化 ✅ Snapshot快照传输 ✅ CheckQuorum检查机制 raft-rs的生产用户包括：TiKV（分布式事务KV数据库）注意：该库已进入维护模式，新功能开发放缓，建议新项目考虑OpenRaft2、OpenRaft 🚀 现代化异步架构设计理念：完全异步事件驱动，不依赖定时tick，消息批处理优化高吞吐。核心亮点：事件驱动架构：基于Raft事件而非轮询，避免空转，大幅提升资源利用率 统一API：单一Raft类型，通过RaftLogStorage、RaftStateMachine、RaftNetwork三个Trait扩展存储和网络层 完善的成员变更：采用更通用的Joint Consensus，支持任意成员变更（单次可增删多节点），而非单步变更 内置可观测性：集成tracing日志和分布式追踪，支持编译时调整日志级别 手动控制：支持手动触发选举(trigger_elect)、快照(trigger_snapshot)、日志清理(purge_log)，便于运维 功能特性：✅ 线性一致性读取(ensure_linearizable) ✅ Learner(Non-voter)角色支持 ✅ 动态心跳/选举开关控制 ⛔️ 不支持单步成员变更（设计取舍，倾向更安全的Joint Consensus） 它的生产用户：Databend（云原生数仓）、CnosDB（时序数据库）、RobustMQ（云原生消息队列）。"
tags:
---
## 动机

Redis协议已经成为事实意义上的key-value存储协议标准。除了官方的Redis实现以外，我们看到还有各种兼容Redis协议的实现：

- [Valkey](https://github.com/valkey-io/valkey) ：Linux基金会官方fork的Redis 7.2分支，采用BSD许可证，是Redis更换SSPL许可证后社区推出的真正开源替代方案，完全兼容Redis协议和持久化机制。
- [Dragonfly](https://github.com/dragonflydb/dragonfly) ：追求极致性能的现代多线程内存数据库，可提供相比Redis高达25倍的吞吐量和更低的尾延迟，但采用BSL许可证（4年后转Apache 2.0）。
- [KeyDB](https://github.com/snapchat/keydb) ：Snapchat收购维护的Redis多线程分支，在100%兼容Redis API的基础上增加了主动复制（Active Replication）和Flash存储扩展能力，但更新已放缓。
- [Kvrocks](https://github.com/apache/kvrocks) ：Apache顶级项目，基于RocksDB实现数据持久化到磁盘的分布式KV存储，支持数十TB级数据且成本仅为内存方案的1/5-1/10，适合大容量低成本场景。

但是，上面的任何一个实现，都没有在分布式系统的强一致性上走得更远，在这个维度，它们依然采用了Redis原生实现的最终一致性。

最开始，我创建 [coredb](https://github.com/lichuang/coredb) 项目，是为了利用raft共识算法，实现一个满足强一致性且兼容redis协议的服务。我知道一定有人会有疑问：大家使用Redis类的系统，是为了缓存数据，在这类型的项目里，一般都会选择 [CAP](https://en.wikipedia.org/wiki/CAP_theorem) 中的AP，把可用性放在第一位，而非一致性。

但是，回到文章最开始的结论：Redis协议已经成为事实意义上的key-value存储协议标准。如果在这个大前提下，它的生态价值不应仅仅局限于传统的内存缓存。通过为其引入强一致性的持久化存储，我们可以赋予它全新的生命力和应用场景——正如 HTTP 协议从早期的网页传输协议，最终演变为无处不在的通信基石一样。

最开始，我构建的项目只有coredb，这是一个采用Raft算法+rocksdb的强一致且兼容Redis协议的服务，也就是说，可以继续使用redis客户端访问这个服务，但是它满足强一致性：只要数据写入时返回成功，意味着至少在集群中的半数以上节点写入成功。

在开发过程中我意识到，“Raft + RocksDB” 的架构组合具有极高的通用价值。考虑到许多开发者可能也需要这样一套可靠的底层基座，去构建他们自己专属的强一致性存储系统，我便将这部分核心逻辑进行了解耦，单独抽离出了 [Rockraft](https://github.com/lichuang/rockraft) 这个基础框架项目。

## 设计与实现

Rockraft采用Rust开发，这是我目前最喜欢的系统编程语言：类型安全且内存安全，这两个特性是我最喜欢的Rust语言特性，有了这两个特性在编程时会更加放心。目前Rust语言的常见Raft实现有以下两个：

1. [raft-rs](https://github.com/tikv/raft-rs)

Rust生态中最成熟、生产验证最充分的Raft实现，被近千个生产环境采用。它源自etcd的Go实现移植，但完全用Rust重写，保证了线程安全和内存安全。

架构特点：

- 核心共识模块：仅提供纯共识算法核心（Raft状态机），不包含日志存储、网络传输或状态机实现
- 高度可定制：需自行实现Storage Trait（日志存储）和RaftMessage传输层，灵活性极高
- 多Raft支持：TiKV基于此实现了Multi-Raft架构，支持海量Region分片

功能完整性：

- ✅ Leader选举、日志复制、成员变更（Joint Consensus）
- ✅ PreVote机制避免网络分区干扰
- ✅ Leader Lease读取优化
- ✅ Snapshot快照传输
- ✅ CheckQuorum检查机制

raft-rs的生产用户包括： [TiKV](https://github.com/tikv/tikv) （分布式事务KV数据库）

注意：该库已进入维护模式，新功能开发放缓，建议新项目考虑OpenRaft

2、 [OpenRaft](https://github.com/databendlabs/openraft) 🚀 现代化异步架构

设计理念：完全异步事件驱动，不依赖定时tick，消息批处理优化高吞吐。

核心亮点：

- 事件驱动架构：基于Raft事件而非轮询，避免空转，大幅提升资源利用率
- 统一API：单一Raft类型，通过RaftLogStorage、RaftStateMachine、RaftNetwork三个Trait扩展存储和网络层
- 完善的成员变更：采用更通用的Joint Consensus，支持任意成员变更（单次可增删多节点），而非单步变更
- 内置可观测性：集成tracing日志和分布式追踪，支持编译时调整日志级别
- 手动控制：支持手动触发选举(trigger\_elect)、快照(trigger\_snapshot)、日志清理(purge\_log)，便于运维

功能特性：

- ✅ 线性一致性读取(ensure\_linearizable)
- ✅ Learner(Non-voter)角色支持
- ✅ 动态心跳/选举开关控制
- ⛔️ 不支持单步成员变更（设计取舍，倾向更安全的Joint Consensus）

它的生产用户： [Databend](https://github.com/databendlabs/databend) （云原生数仓）、 [CnosDB](https://github.com/cnosdb/cnosdb) （时序数据库）、 [RobustMQ](https://github.com/robustmq/robustmq) （云原生消息队列）。

Rockraft最终采用了Openraft做为底层的raft算法库，不仅因为它采用更现代化的异步架构、可定制性强，还因为我就是这个项目的 [贡献者](https://github.com/databendlabs/openraft/pulls/lichuang) 之一:)。

Rockraft 的架构如图所示：

Rockraft 架构图

架构四大核心模块包括：

- RPC / 通信层： 负责承接上层客户端的读写请求，以及集群内部节点之间的通讯（如 Leader 发送心跳、复制日志、Follower 参与选举等）。 RaftNetwork 是 openraft 定义的抽象接口，Rockraft 在此层实现了底层的网络传输逻辑。
- 共识引擎层 (openraft)： 这是节点的大脑（Raft Core），完全基于 openraft 库。它负责维护 Raft 状态机的所有状态转移（Leader、Follower、Candidate、Learner），处理选举倒计时，计算日志的 Commit Index 等。它本身是“无状态”且与存储解耦的。
- 存储抽象适配层： 这是 Rockraft 项目的核心胶水层。openraft 规定了两个核心 Trait：RaftLogStorage 和 RaftStateMachine。 Rockraft 实现了这两个 Trait，告诉 Raft 引擎：“当你需要存日志时，调用我的方法；当你需要把数据应用到业务时，也调用我的方法”。
- 物理存储层 (RocksDB)： 数据的最终落地点。为了追求极致性能，Rockraft 通常会在底层共用同一个 RocksDB 实例，但通过列族 (Column Family, CF) 技术进行物理/逻辑隔离：
	- CF: Raft Logs：专门存放按递增 Index 排列的 Raft 日志，利用 RocksDB 高效的顺序写特性。
		- CF: Hard State：存储 Raft 的硬状态（如当前的 Term、把票投给了谁），保证节点重启后不会发生脑裂。
		- CF: State Machine：存储真正被 Commit 的业务数据。当日志达成多数派共识后，才会将日志中的业务操作在这里执行回放（如 Put/Delete Key）。

## 如何使用

使用Rockraft实现一个强一致服务也很简单，需要在服务的配置中指定一个地址和端口，用于集群内的节点采用Raft协议通信，以对写入行为达成一致。例如Rockraft自带 [HTTP服务](https://github.com/lichuang/Rockraft/blob/main/example/) 例子，它是一个以HTTP协议接口接收用户的请求，服务内部以Rockraft在集群中同步数据。

| 方法 | 端点 | 功能 | 一致性要求 |
| --- | --- | --- | --- |
| **GET** | `/get?key={key}` | 查询指定 key 的值 | 线性一致性读 |
| **POST** | `/set` | 设置 key-value | **仅 Leader** |
| **POST** | `/delete` | 删除指定 key | **仅 Leader** |
| **POST** | `/batch_write` | 原子批量写入（多操作事务） | **仅 Leader** |
| **POST** | `/txn` | 条件事务执行（CAS 支持） | **仅 Leader** |
| **POST** | `/getset` | 原子获取旧值并设置新值 | **仅 Leader** |
| **GET** | `/prefix?prefix={prefix}` | 前缀扫描查询 | 本地读取 |
| **GET** | `/members` | 获取集群成员列表 | 本地读取 |
| **POST** | `/join` | 添加节点到集群 | **仅 Leader** （自动转发） |
| **POST** | `/leave` | 从集群移除节点 | **仅 Leader** （自动转发） |
| **GET** | `/health` | 健康检查（返回 Leader 状态） | 本地读取 |
| **GET** | `/metrics` | 集群指标（任期、日志索引等） | 本地读取 |

以下是通过HTTP接口写入数据的流程：

```
┌─────┐     ┌─────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────────┐
│Client│────►│  Axum   │────►│ RaftNode │────►│   OpenRaft  │────►│RocksLogStorage│
└─────┘     │ Handler │     │ write()  │     │             │     │  Append Log   │
            └─────────┘     └──────────┘     └──────┬──────┘     └──────────────┘
                                                      │
                                                      │ Raft Consensus
                                                      │ (Replicate to Quorum)
                                                      ▼
                                               ┌──────────────┐
                                               │RocksStateMachine
                                               │  Apply Log   │
                                               │              │
                                               │┌────────────┴┐
                                               ││   RocksDB   │
                                               ││  Put Key/Val│
                                               │└─────────────┘
                                               └──────────────┘
```

该服务的 [配置文件](https://github.com/lichuang/Rockraft/blob/main/example/conf/node1.toml) ：

```
node_id = 1
http_addr = "127.0.0.1:8001"

[raft]
address = "127.0.0.1:7001"
advertise_host = "localhost"
join = ["localhost:7002", "localhost:7003"]
```

在这里：

- 127.0.0.1:8001： 是接收HTTP客户端请求的地址端口。
- 127.0.0.1:7001： 用于集群内节点的Raft协议通信的地址端口。
- join：是一个地址列表，其中的都是都是raft.address的地址，表示启动后马上向这些地址发起假如集群的请求，join为空表示系统以单机形式启动。

RaftNode 提供的公共 API 包括：

| 方法 | 说明 |
| --- | --- |
| `write(entry)` | 写入一条日志（经 Raft 复制） |
| `batch_write(req)` | 原子批量写入多个 KV |
| `read(req)` | 读取 KV（从 Leader 状态机读取） |
| `txn(req)` | 执行条件事务 |
| `getset(key, value)` | 原子性地获取旧值并设置新值，这个接口为了实现Redis协议的 [getset命令](https://redis.io/docs/latest/commands/getset/) 而设计 |
| `scan_prefix(req)` | 按前缀扫描 KV |
| `add_node(req)` | 添加节点到集群 |
| `remove_node(req)` | 从集群移除节点 |
| `get_members(req)` | 获取集群成员列表 |
| `shutdown()` | 优雅关闭节点 |

目前，Rockraft支持的条件事务，支持 8 种比较操作：

```rust
enum TxnOp {
    Exists,           // 键存在
    NotExists,        // 键不存在
    Equal(Vec<u8>),   // 值等于
    NotEqual(Vec<u8>),// 值不等于
    Greater(Vec<u8>), // 值大于（字典序）
    Less(Vec<u8>),    // 值小于
    GreaterEqual(Vec<u8>),
    LessEqual(Vec<u8>),
}
```

在 [example](https://github.com/lichuang/Rockraft/tree/main/example) 目录中有一个完整使用Rockraft实现了强一致HTTP协议的key-value服务的例子。

## 结语

[Rockraft](https://github.com/lichuang/rockraft) 仍然在持续进化，目前能想到的优化方向包括：

- 目前raft日志存储在底层rocksdb的一个特殊列族里，也许可以参考 [Raft Engine](https://github.com/tikv/raft-engine) 项目的实现来优化这部分的存储性能。
- Openraft原生目前还不支持多raft组，这部分也许可以在Rockraft中实现。
- 使用 [chaos-mesh](https://github.com/chaos-mesh/chaos-mesh) 等工具，增加chaos测试。

同时，也可以关注基于Rockraft实现的 [coredb](https://github.com/lichuang/coredb) 项目，如我在文章一开始时而言：Redis协议已经是事实意义上的key-value存储通用协议，完全可以基于这个协议做出更多有别于纯内存缓存的事情来，coredb就是其中向CP方向的一个探索。

<iframe title="Comments" allow="clipboard-write" src="https://giscus.app/en/widget?origin=https%3A%2F%2Fwww.codedump.info%2Fzh%2Fpost%2F20260412-rockraft%2F&amp;session=&amp;theme=light&amp;reactionsEnabled=1&amp;emitMetadata=0&amp;inputPosition=top&amp;repo=lichuang%2Flichuang.github.io&amp;repoId=MDEwOlJlcG9zaXRvcnkxNDk2MzEzMjU%3D&amp;category=&amp;categoryId=DIC_kwDOCOsxXc4Crotc&amp;strict=0&amp;description=&amp;backLink=https%3A%2F%2Fwww.codedump.info%2Fzh%2Fpost%2F20260412-rockraft%2F&amp;term=zh%2Fpost%2F20260412-rockraft%2F"></iframe>