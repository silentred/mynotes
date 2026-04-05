---
title: "raft 工程化案例之 etcd 源码实现"
source: "https://mp.weixin.qq.com/s/jsJ3_E_5IOs4_rPDM5axzQ"
author:
  - "[[小徐先生1212]]"
published:
created: 2026-04-05
description: "近期在和大家一起探讨分布式一致性共识算法中的 raft 算法. 本系列内容分为两篇：第一篇谈及 raft 算法的实现原理；第二篇通过 etcd 项目源码对 raft 算法原理进行论证和补充.\x0d\x0a本文是其中的第二篇"
tags:
  - "clippings"
---
原创 小徐先生1212 *2023年1月25日 16:05*

## 0 前言

近期在和大家一起探讨分布式一致性共识算法中的 raft 算法. 本系列内容分为两篇：第一篇谈及 raft 算法的实现原理；第二篇通过 etcd 项目源码对 raft 算法原理进行论证和补充.

本文是其中的第二篇，在内容上与第一篇具有很强的关联性，所以请大家优先完成第一篇的阅读后，再开启此篇内容的学习.

## 1 etcd 与 raft

etcd 是一个具有强一致性的分布式键值对存储系统，底层基于 raft 协议保证分布式系统数据的一致性和可用性.

etcd 基于 golang 编写，github 开源地址：https://github.com/etcd-io/etcd. 本文走读的源码版本为 tag: v3.1.10.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iaib4wDiagCYb2PicOhwGc6z8G5G3d51840JtQNaGCnBs6bIiaEQoA7HERjw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

etcd 中关于 raft 算法的实现具有很高的还原性，项目中与 raft 有关的代码主要位于：

| **模块** | **目录** |
| --- | --- |
| raft 算法层 | ./raft/\* |
| raft 应用层示例 | ./contrib/raftexample/\* |
| raft 数据结构定义 | ./raft/raftpb |

## 2 术语表

| **中文名** | **英文名** | **说明** |
| --- | --- | --- |
| 算法层 | algorithm module | 内聚了 raft 共识机制的核心模块.代码层面以 sdk 的形式被应用层引入，启动时以独立 goroutine 的形式存在，与应用层通过 channel 通信. |
| 应用层 | application module | 聚合了 etcd 存储、通信能力的模块.启动时是 raft 节点的主 goroutine，既要负责与客户端通信，又要负责和算法层交互，承上启下. |
| 算法层节点 | Node/node | 是 raft 节点在算法层中的抽象，也是应用层与算法层交互的唯一入口. |
| 应用层节点 | raftNode | 是 raft 节点在应用层中的抽象，内部持有算法层节点 Node 的引用，同时提供处理客户端请求以及与集群内其他节点通信的能力. |
| 通信模块 | transport | etcd 中的网络通信模块，为 raft 节点间通信提供服务. |
| 提议 | proposal | 两阶段提交中的第一阶段：提议. |
| 提交 | commit | 两阶段提交中的第二阶段：提交. |
| 应用 | apply | 将已提交的日志应用到数据状态机，使得写请求真正生效. |
| 数据状态机 | data state machine | raft 节点用于存储数据的介质. 为避免与 raft 节点状态机产生歧义，统一命名为数据状态机. |
| 节点状态机 | node state machine | etcd 实现中， raft 节点本质是个大的状态机. 任何操作如选举、提交数据等，最后都会封装成一则消息输入节点状态机中，驱动节点状态发生变化. |

## 3 宏观架构梳理

## 3.1 算法层

算法层是 raft 算法的核心实现模块，负责根据共识机制进行请求内容的正确性校验，预写日志状态的维护和管理，可提交日志的进度推进.

简单来看，算法层本质上类似于一台“拼图机器”. 我们把输入的日志比喻成一块块“拼图碎片”，提交拼图碎片的应用层则像个捣蛋的小孩，他将拼图顺序打乱并在其中掺入一些错误的碎片，然后依次将“碎片”提交给拼图机器（算法层）.

拼图机器（算法层）则依照对图案轮廓的把握和碎片纹理的观察（raft 共识机制），依次纠正碎片的顺序和内容之后进行归还.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iafCygiapGnibIa527tG1AH2n3uXJlkRIVXfDRBIKGiaX5BVSbUclNsPQcQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

## 3.2 应用层

在 etcd 的实现中，算法层只聚焦于 raft 共识机制部分的内容，其中涉及网络通信、预写日志持久化、数据状态机管理的工作均在应用层进行实现；

应用层是 raft 节点中承上启下的主干模块，既扮演了与外部客户端通信的服务端角色，也是下层算法库的使用者，还要负责与各模块交互，串联 raft 节点运行的整体流程.

由于本文探讨的重点集中 raft 共识机制部分，因此应用层不是我们所研究的重点，更多的笔墨会集中在算法层的内容中.

## 3.3 宏观架构

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iaV0aV0I70tD1n7b7x1Dtg1ErYAYFpYqqH9icnmdlcqjLP8BvDHpiabwqQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

etcd 在实现 raft 时,将内容依据职责边界拆分为应用层和算法层两个模块，在引用关系上，算法层是一个被应用层引用的静态库，但在节点启动时，最终应用层和算法层的内容会内聚于两个独立的 goroutine 当中，依据几个 channel 进行模块间的异步通信，两个模块的核心职责点展示如上图.

## 4 算法层核心数据结构

本节对算法层核心数据结构进行介绍，读者在后续流程梳理的章节中，遇到不明确的数据结构内容，可回头进行追溯.

## 4.1 Entry

代码位于./raft/raftpb/raft.pb.go 文件中.

```
type EntryType int32

const (
    EntryNormal     EntryType = 0
    // 配置变更类的日志
    EntryConfChange EntryType = 1
)

type Entry struct {
    Term             uint64    \`protobuf:"varint,2,opt,name=Term" json:"Term"\`
    Index            uint64    \`protobuf:"varint,3,opt,name=Index" json:"Index"\`
    Type             EntryType \`protobuf:"varint,1,opt,name=Type,enum=raftpb.EntryType" json:"Type"\`
    Data             []byte    \`protobuf:"bytes,4,opt,name=Data" json:"Data,omitempty"\`
}
```

一条 Entry 就是一笔预写日志，包含了普通类型（写请求）和配置变更两种类型.

Entry 中包含了任期 Term、索引 Index、内容 Data 三个字段，其中 term 和 index 共同构成了 entry 的全局唯一索引.

## 4.2 Message

代码位于./raft/raftpb/raft.pb.go 文件中.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iaHZPGpx9N2ZeYmOicClCZAFrFsElibe1hoibu9WJFWEMIPBMwN8Tsz6Q1g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)

```
type Message struct {
    Type             MessageType \`protobuf:"varint,1,opt,name=type,enum=raftpb.MessageType" json:"type"\`
    To               uint64      \`protobuf:"varint,2,opt,name=to" json:"to"\`
    From             uint64      \`protobuf:"varint,3,opt,name=from" json:"from"\`
    Term             uint64      \`protobuf:"varint,4,opt,name=term" json:"term"\`
    LogTerm          uint64      \`protobuf:"varint,5,opt,name=logTerm" json:"logTerm"\`
    Index            uint64      \`protobuf:"varint,6,opt,name=index" json:"index"\`
    Entries          []Entry     \`protobuf:"bytes,7,rep,name=entries" json:"entries"\`
    Commit           uint64      \`protobuf:"varint,8,opt,name=commit" json:"commit"\`
    // ...
    Reject           bool        \`protobuf:"varint,10,opt,name=reject" json:"reject"\`
    RejectHint       uint64      \`protobuf:"varint,11,opt,name=rejectHint" json:"rejectHint"\`
    // ...
}
```

3.2 小节有提及，算法层中，raft 节点本质上是一个状态机，由输入的消息体驱动其状态变更. 这里提到的所谓”消息体“ 指的就是这个 Message 类.

在这种消息驱动状态机的设计模式下，一系列状态驱动函数的入参都采用 Message 的类型，这样做简化了协议，但是也不可避免地破坏了 Message 类的职责单一原则.

Message 作为一个大而全的通用结构体，同时耦合了日志同步请求/响应、leader 选举请求/响应、心跳请求/响应等内容，而在每次使用上根据当前流程往往只涉及到其中的少量字段. 综合优劣，个人觉得是一种颇有争议的实现方式.

下面对 Message 中几个核心字段的含义进行说明：

（1）Type：消息类型，宏观上分为请求和响应两大类（结尾带 Resp）；根据流程主线又可以分为日志同步、leader 选举、心跳广播、读请求四类；

```
type MessageType int32

const (
    // 本节点要进行选举
    MsgHup            MessageType = 0
    // MsgBeat不用于节点之间通信，仅用于leader内部HB时间到了让leader发送HB消息
    MsgBeat           MessageType = 1
    // 用户向raft提交数据
    MsgProp           MessageType = 2
    // leader向集群中其他节点同步数据
    MsgApp            MessageType = 3
    // append消息的应答
    MsgAppResp        MessageType = 4
    // 投票消息
    MsgVote           MessageType = 5
    MsgVoteResp       MessageType = 6
    // ...
    MsgHeartbeat      MessageType = 8
    MsgHeartbeatResp  MessageType = 9
    // ...
    MsgReadIndex      MessageType = 15
    MsgReadIndexResp  MessageType = 16
    MsgPreVote        MessageType = 17
    MsgPreVoteResp    MessageType = 18
)
```

（2）To/From：消息的发送方和接收方，都以节点 id 进行标识；

（3）Term：消息发送方当前的任期；

（4）LogTerm、Index：待同步日志的上一笔日志的任期和索引. leader 同步日志时用到这两个字段；

（5）Entries：待完成同步的预写日志；

（6）Commit：leader 已提交的日志索引；

（7）Reject：标识响应结果为拒绝或赞同. 节点响应竞选投票或者响应日志同步时会使用到此字段；

（8）RejectHint：节点上一条预写日志的索引. 节点响应日志同步时使用到此字段.

## 4.3 raftLog

raftLog 代码位于./raft/log.go 文件中.

unstable 代码位于./raft/log\_unstable.go 文件中.

storage 代码位于./raft/storage.go 文件中.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iasvqBgLQlMIRLo4Mcvbr9lwicv1scRstyrLQ0JM93icyVn54mSFA50Ziaw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)

```
type raftLog struct {
    // 用于保存自从最后一次snapshot之后提交的数据
    storage Storage

    // 用于保存还没有持久化的数据和快照，这些数据最终都会保存到storage中
    unstable unstable

    // committed数据索引
    committed uint64

    // committed保存是写入持久化存储中的最高index，而applied保存的是传入状态机中的最高index
    // 即一条日志首先要提交成功（即committed），才能被applied到状态机中
    // 因此以下不等式一直成立：applied <= committed
    applied uint64
    // ...
}
```

raftLog 是算法层中管理预写日志的模块，包含未持久化预写日志读写模块 unstable 和持久化日志查询模块 storage.

实际上，为了优化日志的存储损耗，在 unstable 模块还采用了一套快照机制对预写日志内容进行压缩，但属于主干流程之外的可选优化项，为降低流程复杂度，本文会删去关于这部分内容的介绍.

预写日志产生时，需要经历一个未持久化（内存）-> 已持久化（磁盘）的过程，前者在算法层内由 raftLog.unstable 完成，后者在应用层内完成，并通过 raftLog.storage 为算法层提供已持久化预写日志的查询能力.

（1）storage：持久化日志存储接口，提供了日志的查询能力. storage 是一个抽象接口，可由用户自定义实现，核心 api 如上；

```
type Storage interface {
    // 返回保存的初始状态
    InitialState() (pb.HardState, pb.ConfState, error)
    // 返回索引范围在[lo,hi)之内并且不大于maxSize的entries数组
    Entries(lo, hi, maxSize uint64) ([]pb.Entry, error)
    // 传入一个索引值，返回这个索引值对应的任期号，如果不存在则error不为空，其中：
    // ErrCompacted：表示传入的索引数据已经找不到，说明已经被压缩成快照数据了。
    // ErrUnavailable：表示传入的索引值大于当前的最大索引
    Term(i uint64) (uint64, error)
    // 获得最后一条数据的索引值
    LastIndex() (uint64, error)
    // 返回第一条数据的索引值
    FirstIndex() (uint64, error)
    // ...
}
```

（2）unstable：提供了未持久化预写日志代理能力，可读可写；entries 是还未持久化的预写日志列表；offset 是首笔未持久化预写日志在全局预写日志中的索引偏移量.

```
type unstable struct {
    // ...
    // 还未持久化的数据
    entries []pb.Entry
    // offset用于保存entries数组中的数据的起始index
    offset  uint64
    // ...
}
```

（3）committed：已提交日志的索引；

（4）applied：已应用日志的索引.

## 4.4 Ready

代码位于./raft/node.go 文件中.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iagApTnWjkgA20r6jOKJdibBcVBpB5sOOFgEYXqxCa9VAqvEwgwDx5cmg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)

```
type Ready struct {
    // 软状态是异变的，包括：当前集群leader、当前节点状态
    *SoftState

    // 硬状态需要被保存，包括：节点当前Term、Vote、Commit
    // 如果当前这部分没有更新，则等于空状态
    pb.HardState

    // 需要在消息发送之前被写入到持久化存储中的entries数据数组
    Entries []pb.Entry

    // ...
    // 需要输入到状态机中的数据数组，这些数据之前已经被保存到持久化存储中了
    CommittedEntries []pb.Entry

    // 在entries被写入持久化存储中以后，需要发送出去的数据
    Messages []pb.Message
}
```

Ready 是算法层与应用层交互的数据格式. 每当算法层执行完一轮处理逻辑后,会往一个 channel 中（readyc） 传入一个 Ready 结构体，其中封装了算法层处理好的结果.

（1）SoftState：raft 节点的软状态，包含了节点的 leader 和角色状态两部分信息，由于都是容易发生改变且通过通信可重新恢复的信息，因此无需进行持久化存储；

```
type SoftState struct {
    Lead      uint64 // must use atomic operations to access; keep 64-bit aligned.
    RaftState StateType
}
```

其中，节点的角色状态包含跟随者 Follower、候选人 Candidate 和领导者 Leader 三大类. 而 candidate 由根据竞选 vote 和预竞选 preVote，进一步拆分为 candidate 和 preCandidate 两个状态；

```
type StateType uint64

const (
    StateFollower StateType = iota
    StateCandidate
    StateLeader
    StatePreCandidate
)
```

（2）HardState：raft 节点的当前任期、投票归属和已提交日志索引，这些信息都需要持久化存储，节点宕机后重启亦可恢复如初；

```
type HardState struct {
    Term             uint64 \`protobuf:"varint,1,opt,name=term" json:"term"\`
    Vote             uint64 \`protobuf:"varint,2,opt,name=vote" json:"vote"\`
    Commit           uint64 \`protobuf:"varint,3,opt,name=commit" json:"commit"\`
}
```

（3）Entries：

本轮算法层产生的预写日志，此时还未持久化，需要传输到应用层，由应用层完成持久化.

```
Entries []pb.Entry
```

（4）CommittedEntries

本轮算法层已提交的预写日志，需要传输到应用层，由应用层将其应用到状态机.

```
CommittedEntries []pb.Entry
```

（5）Messages

本轮算法层需要发出的消息，由应用层调用网络通信模块发出.

```
Messages []pb.Message
```

## 4.5 Node 接口

代码位于./raft/node.go 文件中.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iaAZl4UgJ4hQ8D4OBwkFqNVOjtpd9MBAPBYhKheyb7DVibxIHnBXVqoibw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=6)

Node 是算法层中 raft 节点的抽象，也是应用层与算法层交互的唯一入口，应用层持有Node 作为算法层 raft 节点的引用，通过调用 Node 接口的几个 api，完成与算法层的 channel 通信.

```
// Node represents a node in a raft cluster.
type Node interface {
    Tick()
    Propose(ctx context.Context, data []byte) error
    ProposeConfChange(ctx context.Context, cc pb.ConfChange) error
    ApplyConfChange(cc pb.ConfChange) *pb.ConfState
    ReadIndex(ctx context.Context, rctx []byte) error
    Step(ctx context.Context, msg pb.Message) error
    Ready() <-chan Ready
    Advance()
    // ...
}
```

Node 接口的核心 api 包括：

（1）Tick：传送定时驱动信号，每次调用 Tick 方法的时间间隔是固定的，称为一个 tick，是 raft 节点的最小计时单位，后续 leader 节点的心跳计时和 leader/candidate 的选举计时也都是以 tick 作为时间单位；

下面查看 node 实现类中，该方法的内容：

```
func (n *node) Tick() {
    select {
    case n.tickc <- struct{}{}:
    // ...
    }
}
```

实际上，该方法为应用层向 node.tickc channel 中传入一个信号，而算法层的 goroutine 是处于时刻监听该 channel 状态的，获取到信号后就会驱动 raft 节点进行定时函数处理；

（2）Propose：

应用层调用 Node.Propose 方法，向算法层发起一笔写数据的请求.

实现类中该方法的内容：

```
func (n *node) Propose(ctx context.Context, data []byte) error {
    return n.step(ctx, pb.Message{Type: pb.MsgProp, Entries: []pb.Entry{{Data: data}}})
}
```
```
func (n *node) step(ctx context.Context, m pb.Message) error {
    ch := n.recvc
    if m.Type == pb.MsgProp {
        ch = n.propc
    }

    select {
    case ch <- m:
        return nil
    // ...
    }
}
```

应用层调用 Propose 方法，最终会往 node.propc channel 中传入一条类型为 MsgProp 的消息. 算法层 goroutine 通过读 channel 获取到消息后，会驱动 raft 节点进入写请求提议流程.

（3）ProposeConfChange

```
func (n *node) ProposeConfChange(ctx context.Context, cc pb.ConfChange) error {
    data, err := cc.Marshal()
    if err != nil {
        return err
    }
    return n.step(ctx, pb.Message{Type: pb.MsgProp, Entries: []pb.Entry{{Type: pb.EntryConfChange, Data: data}}})
}
```

应用层调用该方法，通过 node.propc hannel 向算法层发送一则消息类型为 MsgProp、日志类型为 EntryConfChange 的消息，推动 raft 节点进入配置变更流程.

（4）ApplyConfChange

```
func (n *node) ApplyConfChange(cc pb.ConfChange) *pb.ConfState {
    var cs pb.ConfState
    select {
    // 向配置更新channel写入要更新的配置
    case n.confc <- cc:
    // ...
    }
    // ...
    return &cs
}
```

应用层调用该方法的时机是在配置变更提议已经通过两阶段提交之后，该方法会通过 node.confc 向算法层发送配置变更内容，算法层 goroutine 接收到后会直接应用，使得变更即时生效.

（5）ReadIndex：

```
func (n *node) ReadIndex(ctx context.Context, rctx []byte) error {
    return n.step(ctx, pb.Message{Type: pb.MsgReadIndex, Entries: []pb.Entry{{Data: rctx}}})
}
```

应用层调用 node.ReadIndex 方法向算法层发起读数据请求. 实际上会往 node.recvc channel 中传入一条类型为 MsgReadIndex 的消息.

（6）Step：

```
func (n *node) Step(ctx context.Context, m pb.Message) error {
    // ignore unexpected local messages receiving over network
    if IsLocalMsg(m.Type) {
        // TODO: return an error?
        return nil
    }
    return n.step(ctx, m)
}

func IsLocalMsg(msgt pb.MessageType) bool {
    return msgt == pb.MsgHup || msgt == pb.MsgBeat 
}
```

应用层调用 Node.Step 方法，可以向算法层 goroutine 传送一条自由指定类型的消息，但类型不能是 MsgHup（驱动本节点进行选举）或者 MsgBeat（驱动本 leader 节点进行心跳广播），因为这些动作应该是由定时器驱动，而非人为调用.

（7）Ready 和 Advance：

```
func (n *node) Ready() <-chan Ready { 
    return n.readyc 
}

func (n *node) Advance() {
    select {
    case n.advancec <- struct{}{}:
    // ...
    }
}
```

应用层调用 Node.Ready 方法返回 node.readyc channel 用于监听，当应用层从 readyc 中读取到 Ready 信号时，说明算法层已经产生了新一轮的处理结果，应用层需要进行响应处理；

当应用层处理完毕后，需要调用 Node.Advance 方法，通过向 node.advancec channel 中发送信号的方式，示意应用层已处理完毕，算法层可以进入下一轮调度循环.

因此，Node.Ready 和 Node.Advance 方法是成对使用的，当两个方法各被调用一次，意味着应用层与算法层之间完成了一轮交互，紧接着会开启下一轮，周而复始，循环往复.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iapl1SyS3pGEeKic479IgRiar7A4quF6rXdjiaftbRBfg4iaA3ygJpodjHibw/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=7)

## 4.6 readOnly

代码位于./raft/read\_only.go 文件.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iaaOogXlIYV1On5P4k5p4rJRichibeX3SAiaxIZHoJTuia4TGicIoiaTDLdm9A/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=8)

```
type readOnly struct {
    // 使用entry的数据为key，保存当前pending的readIndex状态
    pendingReadIndex map[string]*readIndexStatus
    // 保存entry的数据为的队列，pending的readindex状态在这个队列中进行排队
    readIndexQueue   []string
}
```

readOnly 是挂起的读请求队列，由 raft 节点持有.

pendingReadIndex：是一系列还未处理的读请求，通过 map 的形式存储，建立读请求 id 与读请状态间的映射关系；

readIndexQueue：读请求 id 数组，本质上是个队列，根据读请求到达的时间顺序先进先出.

```
type readIndexStatus struct {
    // 保存原始的readIndex请求消息
    req   pb.Message
    // 保存收到该readIndex请求时的leader commit索引
    index uint64
    // 保存有什么节点进行了应答，从这里可以计算出来是否有超过半数应答了
    acks  map[uint64]struct{}
}
```

readIndexStatus 是一笔读请求的状态信息：

req：封装读请求的原始消息，消息类型为 MsgReadIndex；

index：收到读请求时，leader 节点的已提交日志索引；

acks：对 leader 节点而言，响应读请求前需要证实自己身份的合法性，所以会给所有节点广播一轮特殊的心跳请求，并通过此处的 acks map 记录有哪些节点进行了响应，当达到多数派，就可以对读请求作出响应.

## 4.7 Progress

代码位于./raft/progress.go 文件.

```
type Progress struct {
    Match, Next uint64
}
```

Progress 是 leader 记录其他节点日志同步进度的载体，Match 是该节点已同步日志的索引；Next 是 leader 下一次向节点同步日志时的日志索引.

## 4.8 raft

代码位于./raft/raft.go.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iadrfW5uxLSQciaPCUW8fO9IKMTrlcdZc0qgG6odlITwC3fWcnwEmNqvA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=9)

```
type raft struct {
    id uint64
    // 任期号
    Term uint64
    // 投票给哪个节点ID
    Vote uint64
    raftLog *raftLog
    prs         map[uint64]*Progress
    state StateType
    // 该map存放哪些节点投票给了本节点
    votes map[uint64]bool
    msgs []pb.Message
    lead uint64
    // 标识当前还有没有applied的配置数据
    pendingConf bool
    readOnly *readOnly
    electionElapsed int
    heartbeatElapsed int
    preVote     bool
    heartbeatTimeout int
    electionTimeout  int
    randomizedElectionTimeout int
    // tick函数，在到期的时候调用，不同的角色该函数不同
    tick func()
    step stepFunc
}

type stepFunc func(r *raft, m pb.Message)
```

raft 类是 raft 共识算法的抽象,几乎囊括了一个 raft 节点正常运行时所必备的全部信息.

（1）id：节点 id；

（2）Term：节点当前的任期号；

（3）raftLog：日志管理模块；

（4）prs：记录了其他节点的日志同步进度；

（5）state：当前节点的角色状态：

```
type StateType uint64

const (
    StateFollower StateType = iota
    StateCandidate
    StateLeader
    StatePreCandidate
)
```

（6）votes：当前节点角色为 candiate 时会使用到，记录有哪些节点给当前节点投了票；

（7）msgs：当前节点需要发送的消息，最终会通过 Ready 结构体传给应用层进行发送；

（8）lead：节点的 leader id；

（9）pendingConf：标识当前节点是否有还没有被应用的配置变更数据；

（10）readOnly：挂起的读请求队列；

（11）preVote：标识当前节点是否处于预竞选状态；

（12）electionElapsed：选举计时，单位为 tick；

（13）heartbeatElapsed：心跳计时，单位为 tick；

（14）heartbeatTimeout：leader 广播心跳的时间间隔，单位 tick；

（15）electionTimeout：candidate/follower 进行选举的时间间隔，单位 tick；

（16）randomizedElectionTimeout：新增随机扰动后的选举时间间隔，范围在 \[electionTimeout, 2\* electionTimeout - 1\] 之间，每次切换节点身份时，这个随机扰动值会被重置一次；

（17）tick：节点的定时处理函数，不同角色的处理函数不同，leader 是广播心跳的 tickHeartbeat 函数，follower 和 candidate 是发起竞选的 tickElection 函数；

（18）step：节点的状态机处理函数，不同角色的状态机函数不同，分为 stepLeader、stepCandidate 和 stepFollower 三类.

## 5 应用层核心数据结构

本节中，以 etcd 提供的 raft 运行示例作为参照，学习应用层的代码架构和实现细节. 为了使得整个流程更加连贯和立体，此处还会简单谈及的 kvStore（数据状态机）和 httpapi（客户端）的一些内容.

## 5.1 raftNode

代码位于./contrib/raftexample/raft.go.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iaVT6dJTPrDWOYibIYRFxMPib6bpribEmvyaUZRzhibjXupvY6BVRk3rR8rQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=10)

```
type raftNode struct {
    proposeC    <-chan string            // proposed messages (k,v)
    confChangeC <-chan raftpb.ConfChange // proposed cluster config changes
    commitC     chan<- *string           // entries committed to log (k,v)
    // ...
    id          int      // client ID for raft session
    peers       []string // raft peer URLs
    // ...

    appliedIndex  uint64

    // raft backing for the commit/error channel
    node        raft.Node
    raftStorage *raft.MemoryStorage

    // ...
    transport *rafthttp.Transport
    // ...
}
```

raftNode 是在应用层中额外封装了一层的 raft 节点，处理持有算法层的入口之外，还包含了与客户端、数据状态机、预写日志持久化模块、通信模块交互的一些能力.

（1）proposeC：用于接收客户端发送的写请求；

（2）confChangeC：用于接收客户端发送的配置变更请求；

（3）commitC：用于将已提交的日志应用到数据状态机；

（4）id：raft 节点 id；

（5）peers：同一集群内其他 raft 节点的标识信息；

（6）appliedIndex：本节点已应用到状态机的日志索引；

（7）node：算法层入口，即 4.5 小节中重点介绍的 Node 接口；

（8）raftStorage：持久化预写日志存储模块；

（9）transport: raft 集群通信模块.

## 5.2 kvStore

代码位于./contrib/raftexample/kvstore.go.

```
type kvstore struct {
    proposeC    chan<- string // channel for proposing updates
    mu          sync.RWMutex
    kvStore     map[string]string // current committed key-value pairs
}
```

kvstore 是一个乞丐版的键值对存储模块，用于以小见大，模拟还原 etcd 存储系统与 raft 节点间的交互模式.

（1）proposeC：与 raftNode.proposeC 是同一个 channel，负责向 raftNode 发送来自客户端的写数据请求；

（2）mu：读写锁，保证数据并发安全；

（3）kvStore：键值对存储介质，可以理解为，它就是数据状态机.

```
func newKVStore(snapshotter *snap.Snapshotter, proposeC chan<- string, commitC <-chan *string, errorC <-chan error) *kvstore {
    s := &kvstore{proposeC: proposeC, kvStore: make(map[string]string), snapshotter: snapshotter}
   
    // read commits from raft into kvStore map until error
    go s.readCommits(commitC, errorC)
    return s
}
```

kvstore 模块启动时，会注入一个 commitC channel，和 raftNode.commitC 是同一个 channel.

kvstore 会持续监听该 channel，获取到 raftNode 提交的日志数据，将其应用到数据状态机：

```
func (s *kvstore) readCommits(commitC <-chan *string, errorC <-chan error) {
    for data := range commitC {
        // ...
        var dataKv kv
        dec := gob.NewDecoder(bytes.NewBufferString(*data))
        if err := dec.Decode(&dataKv); err != nil {
            log.Fatalf("raftexample: could not decode message (%v)", err)
        }
        s.mu.Lock()
        s.kvStore[dataKv.Key] = dataKv.Val
        s.mu.Unlock()
    }
    // ...
}
```

此外，kvstore 提供了 Propose 方法供客户端发送写请求，kvstore 随之通过 proposeC 将请求发送给 raftNode 处理.

```
func (s *kvstore) Propose(k string, v string) {
    var buf bytes.Buffer
    if err := gob.NewEncoder(&buf).Encode(kv{k, v}); err != nil {
        log.Fatal(err)
    }
    s.proposeC <- string(buf.Bytes())
}
```

## 5.3 httpapi

代码位于./contrib/raftexample/httpapi.go.

```
type httpKVAPI struct {
    store       *kvstore
    confChangeC chan<- raftpb.ConfChange
}

func (h *httpKVAPI) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    key := r.RequestURI
    switch {
    case r.Method == "PUT":
        v, err := ioutil.ReadAll(r.Body)
        // ...
        h.store.Propose(key, string(v))
    // ...
    case r.Method == "POST":
        url, err := ioutil.ReadAll(r.Body)
        // ...

        cc := raftpb.ConfChange{
            Type:    raftpb.ConfChangeAddNode,
            NodeID:  nodeId,
            Context: url,
        }
        h.confChangeC <- cc

    // ...
    case r.Method == "DELETE":
        // ...

        cc := raftpb.ConfChange{
            Type:   raftpb.ConfChangeRemoveNode,
            NodeID: nodeId,
        }
        h.confChangeC <- cc
    // ...
}
```

httpapi 是一个 http server，可以理解为低配版客户端模块.

服务运行时，如果接收到 PUT 请求，则视为一个写数据请求，会通过 kvstore.Propose api 进行转发处理；如果是 POST 请求，会视为添加节点的配置变更请求；如果是 DELETE 请求，会视为删除节点的集群配置变更请求.

## 6 应用层与算法层交互流程

## 6.1 应用层运行

应用层封装的 raft 节点定义为 raftNode 类，随着 raftNode.startRaft 方法的调用，一个 raft 节点真正启用了，其中包含了应用层和算法层两个部分的初始化和启动过程.

代码位于./conrib/raft/example/raft.go.

```
func (rc *raftNode) startRaft() {
    // ...

    rpeers := make([]raft.Peer, len(rc.peers))
    for i := range rpeers {
        rpeers[i] = raft.Peer{ID: uint64(i + 1)}
    }
    c := &raft.Config{
        ID:              uint64(rc.id),
        ElectionTick:    10,
        HeartbeatTick:   1,
        Storage:         rc.raftStorage,
    }

    startPeers := rpeers
    rc.node = raft.StartNode(c, startPeers)

    // ...

    rc.transport = &rafthttp.Transport{
        ID:          types.ID(rc.id),
        ClusterID:   0x1000,
        Raft:        rc,
        ServerStats: ss,
        LeaderStats: stats.NewLeaderStats(strconv.Itoa(rc.id)),
        ErrorC:      make(chan error),
    }

    rc.transport.Start()
    for i := range rc.peers {
        if i+1 != rc.id {
            rc.transport.AddPeer(types.ID(i+1), []string{rc.peers[i]})
        }
    }

    go rc.serveRaft()
    go rc.serveChannel
}
```

（1）获取集群内其他 raft 节点的信息：

```
rpeers := make([]raft.Peer, len(rc.peers))
    for i := range rpeers {
        rpeers[i] = raft.Peer{ID: uint64(i + 1)}
    }
    startPeers := rpeers
```

（2）创建一份 raft 节点配置，其中 leader 的心跳时间间隔默认为 tick，follower/candidate 的选举时间间隔默认为 10 个 tick.

```
c := &raft.Config{
        ID:              uint64(rc.id),
        ElectionTick:    10,
        HeartbeatTick:   1,
        Storage:         rc.raftStorage,
    }
```

（3）启动算法层的一个 Node，此处这是算法层与应用层的分水岭，后续 6.2 小节会顺延该方法展开介绍.

```
rc.node = raft.StartNode(c, startPeers)
```

（4）启动通信模块，本文不细说.

```
rc.transport = &rafthttp.Transport{
        ID:          types.ID(rc.id),
        ClusterID:   0x1000,
        Raft:        rc,
        // ...
    }

    rc.transport.Start()
    for i := range rc.peers {
        if i+1 != rc.id {
            rc.transport.AddPeer(types.ID(i+1), []string{rc.peers[i]})
        }
    }

    go rc.serveRaft()
```

（5）异步开启 raftNode 的主循环，用于与算法层的 goroutine 建立持续通信的关系.

```
go rc.serveChannels()
```

下面展开 raftNode.serveChannels 方法的详细内容：

```
func (rc *raftNode) serveChannels() {
    // ...

    ticker := time.NewTicker(100 * time.Millisecond)
    defer ticker.Stop()

    go func() {
        var confChangeCount uint64 = 0

        for rc.proposeC != nil && rc.confChangeC != nil {
            select {
            case prop, ok := <-rc.proposeC:
                if !ok {
                    rc.proposeC = nil
                } else {
                    // blocks until accepted by raft state machine
                    rc.node.Propose(context.TODO(), []byte(prop))
                }

            case cc, ok := <-rc.confChangeC:
                if !ok {
                    rc.confChangeC = nil
                } else {
                    confChangeCount += 1
                    cc.ID = confChangeCount
                    rc.node.ProposeConfChange(context.TODO(), cc)
                }
            }
        }
        // client closed channel; shutdown raft if not already
        close(rc.stopc)
    }()

    // event loop on raft state machine updates
    for {
        select {
        case <-ticker.C:
            rc.node.Tick()

        // store raft entries to wal, then publish over commit channel
        case rd := <-rc.node.Ready():
            // ...
            rc.raftStorage.Append(rd.Entries)
            rc.transport.Send(rd.Messages)
            if ok := rc.publishEntries(rc.entriesToApply(rd.CommittedEntries)); !ok {
                rc.stop()
                return
            }
            rc.node.Advance()

        // ...
        }
}
```

serveChannels 方法又可以拆解为并发运行的两部分内容：

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8ia5EyibMGygdM5jxNBVmDa8ddODt5LY425wR2PG10laJLb5aNtK7eyXug/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=11)

（1）Propose & ProposeConfChange：

```
go func() {
        // ...
        for {
            select {
            case prop := <-rc.proposeC:
                 rc.node.Propose(context.TODO(), []byte(prop))
            case cc, ok := <-rc.confChangeC:
                  cc.ID = confChangeCount
                  rc.node.ProposeConfChange(context.TODO(), cc)
            }
        }
        // client closed channel; shutdown raft if not already
        close(rc.stopc)
   }
```

raftNode 会持续监听 proposeC 和 confChangeC 两个 channel，从而接收到来自客户端的写数据和配置变更请求，然后调用 Node 接口的 api 将其发送给算法层；

（2）Tick&Ready&Advance

```
ticker := time.NewTicker(100 * time.Millisecond)
    defer ticker.Stop()
    
    // event loop on raft state machine updates
    for {
        select {
        case <-ticker.C:
            rc.node.Tick()

        case rd := <-rc.node.Ready():
            // ...
            rc.raftStorage.Append(rd.Entries)
            rc.transport.Send(rd.Messages)
            if ok := rc.publishEntries(rc.entriesToApply(rd.CommittedEntries)); !ok {
                rc.stop()
                return
            }
            
            rc.node.Advance()
            // ...
        }
    }
```

raftNode 会启动一个定时器，每个 tick 默认为 100ms，然后定时调用 Node.Tick 方法驱动算法层执行定时函数：

```
ticker := time.NewTicker(100 * time.Millisecond)
    defer ticker.Stop()
    for{
        select {
        case <-ticker.C:
            rc.node.Tick()
    }
```

此外，raftNode 会通过 Node.Ready 和 Node.Advance 方法与算法层循环交互.

注意到，当应用层通过 Node.Ready 方法接收到来自算法层的处理结果后，raftNode 需要将待持久化的预写日志（Ready.Entries）进行持久化，需要调用通信模块为算法层执行消息发送动作（Ready.Messages），需要与数据状态机交互，应用算法层已确认提交的预写日志.

当以上步骤处理完成时，raftNode 会调用 Node.Advance 方法对算法层进行响应.

当 Node.Ready 和 Node.Advance 方法各完成一次调用，则意味着应用层与算法层完成了一轮交互.

```
case rd := <-rc.node.Ready():
            // ...
            rc.raftStorage.Append(rd.Entries)
            rc.transport.Send(rd.Messages)
            if ok := rc.publishEntries(rc.entriesToApply(rd.CommittedEntries)); !ok {
                rc.stop()
                return
            }
            // ...
            rc.node.Advance()
```

补充说明一下，raftNode 将已提交日志应用到数据状态机的过程. 对应的方法是 raftNode.publishEntries.

倘若已提交日志是正常的写数据请求，则通过 commitC 将数据传送给 kvstore，并 kvstore 的消费 goroutine 将其真正写入数据状态机，可见 5.2 小节；

倘若已提交日志是配置变更请求，则需要调用 Node.ApplyConfChange 方法，将其真正作用于算法层.

```
func (rc *raftNode) publishEntries(ents []raftpb.Entry) bool {
    for i := range ents {
        switch ents[i].Type {
        case raftpb.EntryNormal:
            s := string(ents[i].Data)
        // ...  
            rc.commitC <- &s:
        // ...
        case raftpb.EntryConfChange:
        // ...
            rc.confState = *rc.node.ApplyConfChange(cc)    
        // ...
        }

        // after commit, update appliedIndex
        rc.appliedIndex = ents[i].Index
        }
    }
    return true
}
```

## 6.2 算法层运行

下面聊聊算法层 raft 节点的启动过程.

代码内容位于./raft/node.go.

```
func StartNode(c *Config, peers []Peer) Node {
    r := newRaft(c)
    // 初次启动以term为1来启动
    r.becomeFollower(1, None)
    for _, peer := range peers {
        cc := pb.ConfChange{Type: pb.ConfChangeAddNode, NodeID: peer.ID, Context: peer.Context}
        d, err := cc.Marshal()
        if err != nil {
            panic("unexpected marshal error")
        }
        e := pb.Entry{Type: pb.EntryConfChange, Term: 1, Index: r.raftLog.lastIndex() + 1, Data: d}
        r.raftLog.append(e)
    }
    
    r.raftLog.committed = r.raftLog.lastIndex()
    
    for _, peer := range peers {
        r.addNode(peer.ID)
    }

    n := newNode()
    go n.run(r)
    return &n
}
```

（1）newRaft：启动 node 时，先要初始化一个 raft 共识机制的抽象结构，类型介绍见 4.8 小节;

```
r := newRaft(c)
```

（2）节点刚启动时，都统一置为 follower，把任期设置为 1（1 是最小的任期，哪怕任期暂时滞后，也可以随着通信逐渐恢复），把 leader 置为 None；

```
r.becomeFollower(1, None)
```

（3）把集群中的其他节点都封装成添加节点的配置变更信息，添加到非持久化预写日志当中；

```
for _, peer := range peers {
        cc := pb.ConfChange{Type: pb.ConfChangeAddNode, NodeID: peer.ID, Context: peer.Context}
        d, err := cc.Marshal()
        if err != nil {
            panic("unexpected marshal error")
        }
        e := pb.Entry{Type: pb.EntryConfChange, Term: 1, Index: r.raftLog.lastIndex() + 1, Data: d}
        r.raftLog.append(e)
    }
```

（4）启动之初的配置变更日志直接视为已提交：

```
r.raftLog.committed = r.raftLog.lastIndex()
```

（5）将集群中其他节点的日志同步进度添加到进度 map prs 当中：

```
for _, peer := range peers {
        r.addNode(peer.ID)
    }
```
```
func (r *raft) addNode(id uint64) {
    // 重置pengdingConf标志位
    r.pendingConf = false
    // 检查是否已经存在节点列表中
    if _, ok := r.prs[id]; ok {
        return
    }

    // 这里才真的添加进来
    r.setProgress(id, 0, r.raftLog.lastIndex()+1)
}

func (r *raft) setProgress(id, match, next uint64) {
    r.prs[id] = &Progress{Next: next, Match: match}
}
```

（6）初始化节点：

```
n := newNode()
```
```
func newNode() node {
    return node{
        propc:      make(chan pb.Message),
        recvc:      make(chan pb.Message),
        confc:      make(chan pb.ConfChange),
        readyc:     make(chan Ready),
        advancec:   make(chan struct{}),
        tickc:  make(chan struct{}, 128),
    }
}
```

（7）异步调用 node.run 方法，启动算法层 raft 节点 goroutine，未来正是这个 goroutine 持续与应用层进行通信交互：

```
go n.run(r)
```
```
func (n *node) run(r *raft) {
    var propc chan pb.Message
    var readyc chan Ready
    var advancec chan struct{}
    var prevLastUnstablei, prevLastUnstablet uint64
    var havePrevLastUnstablei bool
    var rd Ready

    lead := None
    prevSoftSt := r.softState()
    prevHardSt := emptyState

    for {
        if advancec != nil {
            // advance channel不为空，说明还在等应用调用Advance接口通知已经处理完毕了本次的ready数据
            readyc = nil
        } else {
            rd = newReady(r, prevSoftSt, prevHardSt)
            if rd.containsUpdates() {
                // 如果这次ready消息有包含更新，那么ready channel就不为空
                readyc = n.readyc
            } else {
                // 否则为空
                readyc = nil
            }
        }
        
        // ...
        select {
        case m := <-propc:
            // 处理本地收到的提交值
            m.From = r.id
            r.Step(m)
        case m := <-n.recvc:
            // 处理其他节点发送过来的提交值
            // filter out response message from unknown From.
            if _, ok := r.prs[m.From]; ok || !IsResponseMsg(m.Type) {
                // 需要确保节点在集群中或者不是应答类消息的情况下才进行处理
                r.Step(m) // raft never returns an error
            }
        case cc := <-n.confc:
            // 接收到配置发生变化的消息
            if cc.NodeID == None {
                // NodeId为空的情况，只需要直接返回当前的nodes就好
                r.resetPendingConf()
                select {
                case n.confstatec <- pb.ConfState{Nodes: r.nodes()}:
                case <-n.done:
                }
                break
            }
            switch cc.Type {
            case pb.ConfChangeAddNode:
                r.addNode(cc.NodeID)
            case pb.ConfChangeRemoveNode:
                // 如果删除的是本节点，停止提交
                if cc.NodeID == r.id {
                    propc = nil
                }
                r.removeNode(cc.NodeID)
            // ...
            }
            // ...
        case <-n.tickc:
            r.tick()
        case readyc <- rd:
            // 通过channel写入ready数据
            // 以下先把ready的值保存下来，等待下一次循环使用，或者当advance调用完毕之后用于修改raftLog的
            if rd.SoftState != nil {
                prevSoftSt = rd.SoftState
            }
            if len(rd.Entries) > 0 {
                // 保存上一次还未持久化的entries的index、term
                prevLastUnstablei = rd.Entries[len(rd.Entries)-1].Index
                prevLastUnstablet = rd.Entries[len(rd.Entries)-1].Term
                havePrevLastUnstablei = true
            }
            if !IsEmptyHardState(rd.HardState) {
                prevHardSt = rd.HardState
            }
            // ...
            r.msgs = nil
            r.readStates = nil
            // 修改advance channel不为空，等待接收advance消息
            advancec = n.advancec
        case <-advancec:
            // 收到advance channel的消息
            if prevHardSt.Commit != 0 {
                // 将committed的消息applied
                r.raftLog.appliedTo(prevHardSt.Commit)
            }
            advancec = nil
            // ...
    }
}
```

（1）通过 channel 指针替换，保证在 select 多路复用的模式下，Node.Ready （readyc）和 Node.Advance（advancec） 方法是被成对调用的：

```
// ...
    for {
        if advancec != nil {
            // advance channel不为空，说明还在等应用调用Advance接口通知已经处理完毕了本次的ready数据
            readyc = nil
        } 
        
        // ...
        select {
        // ...
        case readyc <- rd:
            // 通过channel写入ready数据
            // ...
            // 修改advance channel不为空，等待接收advance消息
            advancec = n.advancec
        case <-advancec:
            // 收到advance channel的消息
            // ...
            advancec = nil
            // ...
        }
   }
```

（2）保证算法层没有新结果产生时，不会通过 readyc 向应用层提交 Ready 消息，避免流程空转：

```
rd = newReady(r, prevSoftSt, prevHardSt)
            if rd.containsUpdates() {
                // 如果这次ready消息有包含更新，那么ready channel就不为空
                readyc = n.readyc
            } else {
                // 否则为空
                readyc = nil
            }
```
```
func (rd Ready) containsUpdates() bool {
    return rd.SoftState != nil || !IsEmptyHardState(rd.HardState) || !IsEmptySnap(rd.Snapshot) || len(rd.Entries) > 0 ||
len(rd.CommittedEntries) > 0 || len(rd.Messages) > 0 || len(rd.ReadStates) != 0
}
```

（3）接收到来自应用层的消息时，会步入 raft.step 方法中：

```
select{
        case m := <-propc:
            // 处理本地收到的提交值
            m.From = r.id
            r.Step(m)
         case m := <-n.recvc:
            // 处理其他节点发送过来的提交值
            if _, ok := r.prs[m.From]; ok || !IsResponseMsg(m.Type) {
                // 需要确保节点在集群中或者不是应答类消息的情况下才进行处理
                r.Step(m) // raft never returns an error
           }        
  }
```

（4）接收到已经确认可应用的配置变更数据时，会对集群配置发起变更：

```
select{
            case cc := <-n.confc:
            switch cc.Type {
            case pb.ConfChangeAddNode:
                r.addNode(cc.NodeID)
            case pb.ConfChangeRemoveNode
                // 如果删除的是本节点，停止提交
                if cc.NodeID == r.id {
                    propc = nil
                }
                r.removeNode(cc.NodeID)
            // ...
            }  
  }
```

（5）接收到应用层的定时 Tick 调用时，会根据 raft 节点的角色，使用其对应的 tick 函数进行处理：

```
select{
        case <-n.tickc:
            r.tick()
        // ...
  }
```

（6）Node.Ready（readyc） 与 Node.Advance（advancec）交互流程：

算法层有处理结果后会投递到 readyc 当中，供应用层 raftNode 接收，并更新一些状态变量；

应用层处理完成后会往 advancec 中发送信号量，算法层会更新 applied index，并开启新一轮循环.

```
select{     
        case readyc <- rd:
            // 通过channel写入ready数据
            // 以下先把ready的值保存下来，等待下一次循环使用，或者当advance调用完毕之后用于修改raftLog的
            if rd.SoftState != nil {
                prevSoftSt = rd.SoftState
            }
            if len(rd.Entries) > 0 {
                // 保存上一次还未持久化的entries的index、term
                prevLastUnstablei = rd.Entries[len(rd.Entries)-1].Index
                prevLastUnstablet = rd.Entries[len(rd.Entries)-1].Term
                havePrevLastUnstablei = true
            }
            if !IsEmptyHardState(rd.HardState) {
                prevHardSt = rd.HardState
            }
            // ...
            r.msgs = nil
            // 修改advance channel不为空，等待接收advance消息
            advancec = n.advanc
        case <-advancec:
            // 收到advance channel的消息
            if prevHardSt.Commit != 0 {
                // 将committed的消息applied
                r.raftLog.appliedTo(prevHardSt.Commit)
            }
            advancec = nil
    }
```

## 6.3 算法层处理流程梳理

算法层处理应用层提交请求的方法链路如下图所示：

（1）应用层 raftNode 在 raftNode.serveChannels 方法调用 Node.Propose 方法，进一步通过 Node.step 方法往 channel 中投递消息；

（2）算法层 goroutine 在 node.run 方法中消费到消息，然后步入通用状态机函数 raft.Step 中进行通用环节前置处理，最后再根据当前节点的角色，切换到对应的状态机函数 raft.step 中进行定制化处理.

  

算法层处理应用层定时调用的方法链路如下图所示：

（1）应用层 raftNode 在 raftNode.serveChannels 方法调用 Node.Tick 方法，往 tickc channel 中投递消息；

（2）算法层 goroutine 在 node.run 方法中消费到消息，然后根据当前节点的角色，切换到对应的定时函数 raft.tick 中进行定制化处理.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iaXic1uDJ9oicJVj5Tcf2ccRBbJksyotOtccsMRibMAJP8hG4hhrGPSDDaQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=12)

在算法层中，还有一项很重要的步骤，就是组装消息，封装到 Ready 结构体中发送给应用层.

首先，组装消息体现在方法 raft.send 当中，位于./raft/raft.go 文件：

```
func (r *raft) send(m pb.Message) {
    m.From = r.id
    if m.Type != pb.MsgProp && m.Type != pb.MsgReadIndex && m.Type != pb.MsgVote && msg.Type != pb.MsgPreVote {
            m.Term = r.Term
    }
    // 注意这里只是添加到msgs中
    r.msgs = append(r.msgs, m)
}
```

这里会对拉票、读、写请求之外的消息填充任期信息，并且将消息体填充 raft.msgs 数组中.

算法层在与应用层交互时，会有一个基于 raft 类构造 Ready 结构体的过程，此时，会将 msgs 填充到 Ready 结构体：

```
func newReady(r *raft, prevSoftSt *SoftState, prevHardSt pb.HardState) Ready {
    rd := Ready{
        // entries保存的是没有持久化的数据数组
        Entries:          r.raftLog.unstableEntries(),
        // 保存committed但是还没有applied的数据数组
        CommittedEntries: r.raftLog.nextEnts(),
        // 保存待发送的消息
        Messages:         r.msgs,
    }
    if softSt := r.softState(); !softSt.equal(prevSoftSt) {
        rd.SoftState = softSt
    }
    if hardSt := r.hardState(); !isHardStateEqual(hardSt, prevHardSt) {
        rd.HardState = hardSt
    }
return rd
}
```

每一轮算法层投递完 Ready 后，会把 raft.msgs 置为空，保证消息不被重复发送到应用层：

```
select{
      case readyc <- rd:
      // ...
        r.msgs = nil
      // 修改advance channel不为空，等待接收advance消息
        advancec = n.advanc
        // ...
    }
```

## 7 角色切换流程

本节以 raft 节点角色切换为主线，进行源码串联走读，首先我们回顾一下各角色之间的 切换机制，如下图所示.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iaYPLHqibFibNKu9PiaPUfotic1jiaz3ibZPqvUSrtl4Y3c4IReiaib0j2HZAGwA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=13)

所谓的节点角色切换，除了对 4.8 小节所述的 raft 数据结构进行一些状态信息更新外，还有一项很核心的内容，就是对定时函数 raft.tick 和状态机函数 raft.step 进行切换，对于 leader 而言，定时函数中的任务是要向集群中的其他节点广播心跳；对于 follower 和 candidate 而言，定时函数的任务是发起竞选；此外，对于不同角色，在接收到消息时的处理模式也不尽相同，这部分区别会在角色专属的状态机函数中体现.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iarHFtjmECmMr8icvcpIsuQBROmlDMA7Fw7iaCJJhuM4ib1XTpU4ial3CWQQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=14)

## 7.1 通用状态机函数

算法层 goroutine 在处理来自应用层的请求时，会先步入 raft.Step 方法，进行通用的消息前处理，后续才会根据角色进入定制的状态机函数中.

代码内容位于./raft/raft.go 文件中.

```
func (r *raft) Step(m pb.Message) error {
    switch {
    case m.Term == 0:
        // 来自本地的消息
    case m.Term > r.Term:
        // 消息的Term大于节点当前的Term
        lead := m.From
        if m.Type == pb.MsgVote || m.Type == pb.MsgPreVote {
            // 如果收到的是投票类消息
            // 否则将lead置为空
            lead = None
        }
        switch {
        case m.Type == pb.MsgPreVote:
            // 收到一笔任期大于自己的预竞选请求，暂时不变 follower
        case m.Type == pb.MsgPreVoteResp && !m.Reject:
            // 处理预竞选的响应时，对方未拒绝自己，暂时不变 follower
        default:
            // 其他情形下，收到任期更大的消息，都变成follower状态
            r.becomeFollower(m.Term, lead)
        }

    case m.Term < r.Term:
        // 消息的Term小于节点自身的Term，同时消息类型是心跳消息或者是append消息
        if r.checkQuorum && (m.Type == pb.MsgHeartbeat || m.Type == pb.MsgApp) {
            // 收到了一个节点发送过来的更小的term消息。这种情况可能是因为消息的网络延时导致，但是也可能因为该节点由于网络分区导致了它递增了term到一个新的任期。
            // ，这种情况下该节点不能赢得一次选举，也不能使用旧的任期号重新再加入集群中。如果checkQurom为false，这种情况可以使用递增任期号应答来处理。
            // 但是如果checkQurom为True，
            // 此时收到了一个更小的term的节点发出的HB或者APP消息，于是应答一个appresp消息，试图纠正它的状态
            // send 方法中会统一加上任期信息
            r.send(pb.Message{To: m.From, Type: pb.MsgAppResp})
        } else {
            // 除了上面的情况以外，忽略任何term小于当前节点所在任期号的消息
        }
        // 在消息的term小于当前节点的term时，不往下处理直接返回了
        return nil
    }

    // 能走到这里意味着消息的任期是大于等于本节点的
    switch m.Type {
    case pb.MsgHup:
        // 收到HUP消息，说明准备进行选举
        if r.state != StateLeader {
            // 当前不是leader
            // 取出[applied+1,committed+1]之间的消息，即得到还未进行applied的日志列表
            ents, err := r.raftLog.slice(r.raftLog.applied+1, r.raftLog.committed+1, noLimit)
            if err != nil {
                panic(err)
            }
            // 如果其中有config消息，并且commited > applied，说明当前还有没有apply的config消息，这种情况下不能开始竞选
            if n := numOfPendingConf(ents); n != 0 && r.raftLog.committed > r.raftLog.applied {
                return nil
            }

            // 进行选举，分为预竞选和竞选两步
            if r.preVote {
                r.campaign(campaignPreElection)
            } else {
                r.campaign(campaignElection)
            }
        } 

    case pb.MsgVote, pb.MsgPreVote:
        // 收到投票类的消息
        if (r.Vote == None || m.Term > r.Term || r.Vote == m.From) && r.raftLog.isUpToDate(m.Index, m.LogTerm) {
            // 如果当前没有给任何节点投票（r.Vote == None）或者投票的节点term大于本节点的（m.Term > r.Term）
            // 或者是之前已经投票的节点（r.Vote == m.From）
            // 同时还满足该节点的消息是最新的（r.raftLog.isUpToDate(m.Index, m.LogTerm)），那么就接受这个节点的投票
            r.send(pb.Message{To: m.From, Type: voteRespMsgType(m.Type)})
            if m.Type == pb.MsgVote {
                // 重置竞选超时计时器
                // 保存下来给哪个节点投票了
                r.electionElapsed = 0
                r.Vote = m.From
            }
        } else {
            // 否则拒绝投票
            r.send(pb.Message{To: m.From, Type: voteRespMsgType(m.Type), Reject: true})
        }

    default:
        // 其他情况下进入各种状态下自己定制的状态机函数
        r.step(r, m)
    }
    return 
}
```

通用状态机函数 raft.Step 做了以下几件事情：

（1）如果接收到一条任期大于自身的消息，需要判断是否需要退位回 follower 状态.

```
case m.Term > r.Term:
        // 消息的Term大于节点当前的Term
        lead := m.From
        if m.Type == pb.MsgVote || m.Type == pb.MsgPreVote {
            // 如果收到的是投票类消息
            lead = None
        }
        switch {
        case m.Type == pb.MsgPreVote:
            // 收到一笔任期大于自己的预竞选请求，暂时不变 follower
        case m.Type == pb.MsgPreVoteResp && !m.Reject:
            // 处理预竞选的响应时，对方未拒绝自己，暂时不变 follower
        default:
            // 其他情形下，收到任期更大的消息，都变成follower状态
            r.becomeFollower(m.Term, lead)
        }
```

（2）倘若收到了一条任期小于自身的消息，需要对心跳或者日志同步请求回复自身的任期，帮助老 leader 尽快退位.

需要注意的是，如果收到更小的消息，一定会在此分支拦截，不会走到后续的角色定制状态机函数中.

```
case m.Term < r.Term:
        // 消息的Term小于节点自身的Term，同时消息类型是心跳消息或者是append消息
        if r.checkQuorum && (m.Type == pb.MsgHeartbeat || m.Type == pb.MsgApp) {
            // 收到了一个节点发送过来的更小的term消息。这种情况可能是因为消息的网络延时导致，但是也可能因为该节点由于网络分区导致了它递增了term到一个新的任期。
            // ，这种情况下该节点不能赢得一次选举，也不能使用旧的任期号重新再加入集群中。如果checkQurom为false，这种情况可以使用递增任期号应答来处理。
            // 但是如果checkQurom为True，
            // 此时收到了一个更小的term的节点发出的HB或者APP消息，于是应答一个appresp消息，试图纠正它的状态
            // send 方法中会统一加上任期信息
            r.send(pb.Message{To: m.From, Type: pb.MsgAppResp})
        } 
        // 在消息的term小于当前节点的term时，不往下处理直接返回了
        return nil
```

（3）收到一条推进选举的消息时，会推进当前节点发起竞选，分为 preVote 和 vote 两步，通过 raft.campaign 方法实施；

```
case pb.MsgHup:
        // 收到HUP消息，说明准备进行选举
        if r.state != StateLeader {
            // 取出[applied+1,committed+1]之间的消息，即得到还未进行applied的日志列表
            ents, err := r.raftLog.slice(r.raftLog.applied+1, r.raftLog.committed+1, noLimit)
            if err != nil {
                panic(err)
            }
            // 如果其中有config消息，并且commited > applied，说明当前还有没有apply的config消息，这种情况下不能开始投票
            if n := numOfPendingConf(ents); n != 0 && r.raftLog.committed > r.raftLog.applied {
                return nil
            }

            // 进行选举
            if r.preVote {
                r.campaign(campaignPreElection)
            } else {
                r.campaign(campaignElection)
            }
        }
```

（4）收到任期大于等于自身的竞选拉票消息时，需要根据其日志数据的新旧程度，判断做出投票结果.

```
case pb.MsgVote, pb.MsgPreVote:
        // 收到投票类的消息
        if (r.Vote == None || m.Term > r.Term || r.Vote == m.From) && r.raftLog.isUpToDate(m.Index, m.LogTerm) {
            // 如果当前没有给任何节点投票（r.Vote == None）或者投票的节点term大于本节点的（m.Term > r.Term）
            // 或者是之前已经投票的节点（r.Vote == m.From）
            // 同时还满足该节点的消息是最新的（r.raftLog.isUpToDate(m.Index, m.LogTerm)），那么就接受这个节点的投票
            r.send(pb.Message{To: m.From, Type: voteRespMsgType(m.Type)})
            if m.Type == pb.MsgVote {
                // 重置竞选超时计时器
                // 保存下来给哪个节点投票了
                r.electionElapsed = 0
                r.Vote = m.From
            }
        } else {
            // 否则拒绝投票
            r.send(pb.Message{To: m.From, Type: voteRespMsgType(m.Type), Reject: true})
        }
```
```
func (l *raftLog) isUpToDate(lasti, term uint64) bool {
    return term > l.lastTerm() || (term == l.lastTerm() && lasti >= l.lastIndex())
}
```

（4）至此，通用处理模块结束，接下来会步入基于角色定制的状态机函数中.

```
default:
        // 其他情况下进入各种状态下自己定制的状态机函数
        r.step(r, m)
```

## 7.2 becomeLeader

当节点需要切换至 leader 的身份时，会调用 raft.becomeLeader 方法：

```
func (r *raft) becomeLeader() {
    if r.state == StateFollower {
        panic("invalid transition [follower -> leader]")
    }
    r.step = stepLeader
    r.reset(r.Term)
    r.tick = r.tickHeartbeat
    r.lead = r.id
    r.state = StateLeader
    ents, err := r.raftLog.entries(r.raftLog.committed+1, noLimit)
    if err != nil {
        r.logger.Panicf("unexpected error getting uncommitted entries (%v)", err)
    }

    // 变成leader之前，这里还有没commit的配置变化消息
    nconf := numOfPendingConf(ents)
    if nconf > 1 {
        panic("unexpected multiple uncommitted config entry")
    }
    if nconf == 1 {
        r.pendingConf = true
    }

    r.appendEntry(pb.Entry{Data: nil})
}
```

（1）切换定时函数和状态机函数：

```
r.step = stepLeader
  r.tick = r.tickHeartbeat
```

（2）切换节点角色状态：

```
r.state = StateLeader
```

（3）批量重置节点状态信息，包括 term、lead、心跳计时、选举计时、竞选票箱、读请求队列、其他节点日志进度等内容；

```
func (r *raft) reset(term uint64) {
    if r.Term != term {
        // 如果是新的任期，那么保存任期号，同时将投票节点置空
        r.Term = term
        r.Vote = None
    }
    r.lead = None

    r.electionElapsed = 0
    r.heartbeatElapsed = 0
    // 重置选举超时
    r.resetRandomizedElectionTimeout()
   
    r.votes = make(map[uint64]bool)
    // 似乎对于非leader节点来说，重置progress数组状态没有太多的意义？
    for id := range r.prs {
        r.prs[id] = &Progress{Next: r.raftLog.lastIndex() + 1
        if id == r.id {
            r.prs[id].Match = r.raftLog.lastIndex()
        }
    }
    r.pendingConf = false
    r.readOnly = newReadOnly(r.readOnly.option)
}
```

其中，每次 reset 时都会对选举时间间隔添加随机扰动，产生一个新的随机值：

```
func (r *raft) resetRandomizedElectionTimeout() {
    r.randomizedElectionTimeout = r.electionTimeout + globalRand.Intn(r.electionTimeout)
}
```

（4）倘若有已提交未应用的配置变更内容，需要通过 raft.pendingConf 标识阻塞后续的配置变更请求.

```
// 变成leader之前，这里还有没commit的配置变化消息
    nconf := numOfPendingConf(ents)
    if nconf > 1 {
        panic("unexpected multiple uncommitted config entry")
    }
    
    if nconf == 1 {
        r.pendingConf = true
    }
```

（5）立即提交一笔当前任期内的空日志，以规避本系列第一篇中 7.6 小节所提及的”提交仍回滚“的问题.

```
r.appendEntry(pb.Entry{Data: nil})
```

## 7.3 becomeFollower

当节点角色需要变更为 follower，会调用 raft.becomeFollower 方法，位于./raft/raft.go 文件：

```
func (r *raft) becomeFollower(term uint64, lead uint64) {
    r.step = stepFollower
    r.reset(term)
    r.tick = r.tickElection
    r.lead = lead
    r.state = StateFollower
}

func (r *raft) tickElection() {
    r.electionElapsed++

    if r.promotable() && r.pastElectionTimeout() {
        // 如果可以被提升为leader，同时选举时间也到了
        r.electionElapsed = 0
        // 发送HUP消息是为了重新开始选举
        r.Step(pb.Message{From: r.id, Type: pb.MsgHup})
    }
}
```

此时会将节点的定时处理函数置为驱动竞选函数 tickElection、将状态机函数更为 stepFollower、调用 7.2 小节谈及的 raft.reset 方法、更新节点的 leader 和 state 信息.

## 7.4 becomePreCandidate

当节点需要发起预选举，需要变更为 preCandidate 角色，会调用 raft.becomePreCandidate 方法，位于./raft/raft.go 文件：

此时会将节点的定时处理函数置为驱动竞选函数 tickElection、将状态机函数更为 stepCandidate、更新节点的 leader 和 state 信息.

需要注意的是，在预选举流程中，不会对 term 进行自增.

```
func (r *raft) becomePreCandidate() {
    // TODO(xiangli) remove the panic when the raft implementation is stable
    if r.state == StateLeader {
        panic("invalid transition [leader -> pre-candidate]")
    }
    // Becoming a pre-candidate changes our step functions and state,
    // but doesn't change anything else. In particular it does not increase
    // r.Term or change r.Vote.
    // prevote不会递增term，也不会先进行投票，而是等prevote结果出来再进行决定
    r.step = stepCandidate
    r.tick = r.tickElection
    r.state = StatePreCandidate
    r.logger.Infof("%x became pre-candidate at term %d", r.id, r.Term)
}
```

## 7.5 becomeCandidate

当节点角色需要变更为 candidate，会调用 raft.becomeCandidate 方法，位于./raft/raft.go 文件：

此时会将节点的定时处理函数置为驱动竞选函数 tickElection、将状态机函数更为 stepCandidate、调用 7.2 小节谈及的 raft.reset 方法、更新节点的 leader 和 state 信息.

```
func (r *raft) becomeCandidate() {
    if r.state == StateLeader {
        panic("invalid transition [leader -> candidate]")
    }
    r.step = stepCandidate
    // 因为进入candidate状态，意味着需要重新进行选举了，所以reset的时候传入的是Term+1
    r.reset(r.Term + 1)
    r.tick = r.tickElection
    // 给自己投票
    r.Vote = r.id
    r.state = StateCandidate
}
```

需要注意的是，与预选举不同，在正式的选举流程中，需要对 term 进行自增：

```
r.reset(r.Term + 1)
```

## 7.6 leader -> follower

下面我们以 leader 切换至 follower 的角色变更流程为主线，追溯源码中的方法调用链路：

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8ia57J97wZbzPRgwbPQIXBjRFUhicF9zk25JqALOKsHfj9D9HuxqWjsoow/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=15)

（1）leader 在处理请求时，会先走进通用的状态机函数 raft.Step 中，此时发现消息任期更大，不会自动退回 follower：

```
func (r *raft) Step(m pb.Message) error {
    switch {
    case m.Term == 0:
        // local message
        // 来自本地的消息
    case m.Term > r.Term:
        // ...
        switch {
        // 注意Go的switch case不做处理的话是不会默认走到default情况的
        case m.Type == pb.MsgPreVote:
            // Never change our term in response to a PreVote
            // 在应答一个prevote消息时不对任期term做修改
        case m.Type == pb.MsgPreVoteResp && !m.Reject:
             // ...
        default:
            // 变成follower状态
            r.becomeFollower(m.Term, lead)
        }
        // ...
     }
}
```

（2）leader 处理消息时会步入 leader 专属的状态机函数 stepLeader 中，此时 leader 倘若发现自己已经和集群的多数派断开联系，也会退回 follower：

```
func stepLeader(r *raft, m pb.Message) {
    switch m.Type {
    // ...
    case pb.MsgCheckQuorum:
        // 检查集群可用性
        if !r.checkQuorumActive() {
            // 如果超过半数的服务器没有活跃
            // 变成follower状态
            r.becomeFollower(r.Term, None)
        }
        return
    }
    // ...
}
```

## 7.6 follower -> candidate

下面我们以 follower 切换至 candidate 的角色变更流程为主线，追溯源码中的方法调用链路：

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iaIYlgpUt4ypCO2Ntq2VptqJiaDdRTZXZBrfgJLl0LmZzoLmlGWNaztPg/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=16)

（1）首先，应用层定时调用 Node.Tick 函数驱动算法层调用定时函数. 倘若算法层 raft 节点角色为 follower 或者 candidate，其定时函数是 tickElection：

```
func (r *raft) tickElection() {
    r.electionElapsed++
    if r.promotable() && r.pastElectionTimeout() {
        // 如果可以被提升为leader，同时选举时间也到了
        r.electionElapsed = 0
        // 发送HUP消息是为了重新开始选举
        r.Step(pb.Message{From: r.id, Type: pb.MsgHup})
    }
}
```

（2）每次调用 tickElection 会把竞选计时器 raft.electionElasped 的 tick 数累加 1 ，倘若超过了选举时间间隔，则会给本节点推一条 MsgHup 类型的消息发起选举；

```
func (r *raft) pastElectionTimeout() bool {
    return r.electionElapsed >= r.randomizedElectionTimeout
}
```

（3）在通用状态机函数中，会对 MsgHup 类型的消息进行响应，调用 raft.campaign 方法发起选举；

```
func (r *raft) Step(m pb.Message) error {
    // ...
    switch m.Type {
    case pb.MsgHup:
        // 收到HUP消息，说明准备进行选举
        if r.state != StateLeader {
            // ...
            // 进行选举
            if r.preVote {
                r.campaign(campaignPreElection)
            } else {
                r.campaign(campaignElection)
            }
        } 
        // ...
    return nil
}
```

（4）最终调用 raft.campaign 方法进行竞选，最终调用 raft.becomePreCandidate 和 raft.becomeCandidate 方法切换角色状态.

```
func (r *raft) campaign(t CampaignType) {
    var term uint64
    var voteMsg pb.MessageType
    if t == campaignPreElection {
        r.becomePreCandidate()
        voteMsg = pb.MsgPreVote
        term = r.Term + 1
    } else {
        r.becomeCandidate()
        voteMsg = pb.MsgVote
        term = r.Term
    }
    // ...
    // 向集群里的其他节点发送投票消息
    for id := range r.prs {
        if id == r.id {
            // 过滤掉自己
            continue
        }

        var ctx []byte
        // ...
        r.send(pb.Message{Term: term, To: id, Type: voteMsg, Index: r.raftLog.lastIndex(), LogTerm: r.raftLog.lastTerm(), Context: ctx})
}
```

最后，成为 candidate 之后，需要向其他节点广播竞选拉票请求：

```
// 向集群里的其他节点发送投票消息
    for id := range r.prs {
        if id == r.id {
            // 过滤掉自己
            continue
        }

        var ctx []byte
        // ...
        r.send(pb.Message{Term: term, To: id, Type: voteMsg, Index: r.raftLog.lastIndex(), LogTerm: r.raftLog.lastTerm(), Context: ctx})
   }
```

## 7.7 candidate -> follower/leader

下面盘一下 candidate 切换至 follower 或者 leader 的方法调用链路：

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iabvGE6PkAo4DPKmyibiblFzicP8NP9QOg5WJDR2vl8oGHfibaic7IONibXfYQ/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=17)

（1）倘若 candidate 在竞选期间，收到了任期更大的消息，就会退回 follower，这部分处理逻辑在通用状态机函数中，和 leader 退位回 follower 的处理路径相同：

```
func (r *raft) Step(m pb.Message) error {
    switch {
    case m.Term == 0:
        // local message
        // 来自本地的消息
    case m.Term > r.Term:
        // ...
        switch {
        // 注意Go的switch case不做处理的话是不会默认走到default情况的
        case m.Type == pb.MsgPreVote:
            // Never change our term in response to a PreVote
            // 在应答一个prevote消息时不对任期term做修改
        case m.Type == pb.MsgPreVoteResp && !m.Reject:
             // ...
        default:
            // 变成follower状态
            r.becomeFollower(m.Term, lead)
        }
        // ...
     }
}
```

（2）倘若 candidate 收到了半数以上的拒绝票，则会退回 follower，倘若收到了半数以上的赞同票，则会进位为 leader. 这部分处理在 candidate 的定制状态机函数 stepCandidate 当中：

```
func stepCandidate(r *raft, m pb.Message) {
    var myVoteRespType pb.MessageType
    if r.state == StatePreCandidate {
        myVoteRespType = pb.MsgPreVoteResp
    } else {
        myVoteRespType = pb.MsgVoteResp
    }
    
    switch m.Type{
        // ...
    case myVoteRespType:
        // 计算当前集群中有多少节点给自己投了票
        gr := r.poll(m.From, m.Type, !m.Reject)
        switch r.quorum() {
        switch r.quorum() {
        case gr:    // 如果进行投票的节点数量正好是半数以上节点数量
            if r.state == StatePreCandidate {
                r.campaign(campaignElection)
            } else {
                // 变成leader
                r.becomeLeader()
                r.bcastAppend()
            }
        case len(r.votes) - gr: // 如果是半数以上节点拒绝了投票
            // 变成follower
            r.becomeFollower(r.Term, None)
        }
     // ...
    }
}
```

其中，统计加入最新一笔选票同时统计当前选票结果的方法是 raft.poll:

```
func (r *raft) poll(id uint64, t pb.MessageType, v bool) (granted int) {
    // 如果id没有投票过，那么更新id的投票情况
    if _, ok := r.votes[id]; !ok {
        r.votes[id] = v
    }
    // 计算下都有多少节点已经投票给自己了
    for _, vv := range r.votes {
        if vv {
            granted++
        }
    }
    return granted
}

func (r *raft) quorum() int { 
  return len(r.prs)/2 + 1 
}
```

## 8 写流程

## 8.1 整体流程

raft 节点处理写请求需要经历一个两阶段提交的流程，下面拆成三个部分描述：

（1）当前节点为leader，应用层调用 Node.Propose 发送写请求给算法层的，算法层添加一系列同步日志的消息到 Ready 结构体中，通过 Node.Ready 方法让应用层消费到，应用层调用通信模块转发给其他节点，之后调用 Node.Advance 开启下一轮交互；

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iaQHicsLtazm22gx1RIBgsicnS0XOl3ic5iaHYSEoZqvjcVwtjUS8AdDerYA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=18)

（2）当前节点为 follower，应用层接收到来自 leader 的同步日志请求，会调用 Node.Step 将请求发给算法层，算法层同步日志后，将响应结果封装到 Ready 结构体，通过 Node.Ready 方法让应用层消费到；应用层通过通信模块转发给 leader，之后调用 Node.Advance 开启下一轮交互；

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iaZ1y4n4afzJLH4rtRr8IFfshmHIT9icC21OZDCwgRb2UnjtV2SY8IFGA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=19)

（3）当前节点为 leader，应用层接收到来自 follower 的同步日志响应，会调用 Node.Step 将请求发给算法层，算法层会更新日志同步进度，当被多数派完成同步后，对应日志会提交，新的日志提交索引会封装到 Ready 结构体，通过 Node.Ready 方法让应用层消费到. 应用层会将已提交日志应用到状态机，之后调用 Node.Advance 开启下一轮交互.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iamicIJOw654icQ63pbkia0IjCKKL9tbaUvtEHHXCZ0wia3P6mIXXrzfSNWA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=20)

## 8.2 应用层发送写请求

首先，客户端向应用层提交写数据请求，raftNode 调用 Node.Propose 方法将请求传到算法层的 propc channel 中，消息的类型为 MsgProp.

```
func (rc *raftNode) serveChannels() {
    // ...
    go func() {
        var confChangeCount uint64 = 0

        for rc.proposeC != nil && rc.confChangeC != nil {
            select {
            case prop:= <-rc.proposeC:
                
                    // blocks until accepted by raft state machine
                 rc.node.Propose(context.TODO(), []byte(prop))
             // ...
            }
        }
        // client closed channel; shutdown raft if not already
        close(rc.stopc)
    }()
}

func (n *node) Propose(ctx context.Context, data []byte) error {
    return n.step(ctx, pb.Message{Type: pb.MsgProp, Entries: []pb.Entry{{Data: data}}})
}

func (n *node) step(ctx context.Context, m pb.Message) error {
    ch := n.recvc
    if m.Type == pb.MsgProp {
        ch = n.propc
    }

    select {
    case ch <- m:
        return nil
    // ...
    }
}
```

## 8.3 follower 转发请求至 leader

算法层接收到消息后，步入通用状态机处理函数，然后进一步步入不同角色的定制状态机处理函数中.

```
func (n *node) run(r *raft) {
    // ...

    for {
        // ...
        select {
        case m := <-propc:
            // 处理本地收到的提交值
            m.From = r.id
            r.Step(m)
         // ...
        }
    }
}
```

如果节点角色是 candidate，会直接无视 MsgProp 类型的消息.

```
func stepCandidate(r *raft, m pb.Message) {
    // ...
    switch m.Type {
    case pb.MsgProp:
        // 当前没有leader，所以忽略掉提交的消息
        return
     // ...
    }
}
```

如果是 follower，会将请求转给 leader.

```
func stepFollower(r *raft, m pb.Message) {
    switch m.Type {
    case pb.MsgProp:
        // 本节点提交的值
        if r.lead == None {
            // 没有leader则提交失败，忽略
            return
        }
        // 向leader进行redirect
        m.To = r.lead
        r.send(m)
     // ...
    }
}
```

## 8.4 算法层 leader 封装日志同步消息

leader 接收到 MsgProp 类型的消息时，会在定制状态机函数中处理：首先将请求封装成日志，添加到未持久化预写日志列表中，然后组装好一系列的同步日志消息，封装到 Ready 结构体中传送给应用层.

```
func stepLeader(r *raft, m pb.Message) {
    switch m.Type {
    // ...
    case pb.MsgProp:
       // ...
        // 添加数据到log中
        r.appendEntry(m.Entries...)
        // 向集群其他节点广播append消息
        r.bcastAppend()
        return
     // ...
    }
}

func (r *raft) bcastAppend() {
    for id := range r.prs {
        if id == r.id {
            continue
        }
        r.sendAppend(id)
    }
}
```

在 sendAppend 方法中，会这部分 propose 的日志类型会更改为 MsgApp：

```
func (r *raft) sendAppend(to uint64) {
    pr := r.prs[to]
    // ...
    m := pb.Message{}
    m.To = to

    // 从该节点的Next的上一条数据获取term
    term, errt := r.raftLog.term(pr.Next - 1)
    // 获取从该节点的Next之后的entries，总和不超过maxMsgSize
    ents, erre := r.raftLog.entries(pr.Next, r.maxMsgSize)

     // 否则就是简单的发送append消息
        m.Type = pb.MsgApp
        m.Index = pr.Next - 1
        m.LogTerm = term
        m.Entries = ents
        // append消息需要告知当前leader的commit索引
        m.Commit = r.raftLog.committed
        // ...
    }
    r.send(m)
}
```

## 8.5 应用层持久化日志与广播日志同步消息

调用 raftStorage.Append 方法，将待持久化预写日志进行持久化；

调用 transport.Send 方法，广播日志同步消息.

```
func (rc *raftNode) serveChannels() {
    // ...
    for {
        select {
        // ...
        case rd := <-rc.node.Ready():
            // ...
            rc.raftStorage.Append(rd.Entries)
            rc.transport.Send(rd.Messages)
            // ...
            rc.node.Advance()
        // ...
    }
}
```

## 8.6 应用层发送同步日志请求

调用 Node.Step 方法，直接将同步日志请求消息原封不动地发送到算法层.

```
func (rc *raftNode) Process(ctx context.Context, m raftpb.Message) error {
    return rc.node.Step(ctx, m)
}
```

## 8.7 follower/candidate 处理同步日志提议

candidate 和 follower 在定制化的状态机函数中处理同步日志提议.

candidate 收到任期大于等于自己竞选任期的同步日志请求后，会退回 follower，然后会尝试将日志追加到非持久化日志列表中；

```
func stepCandidate(r *raft, m pb.Message) {
    // ...
    switch m.Type {
    // ...
    case pb.MsgApp:
        // 收到append消息，说明集群中已经有leader，转换为follower
        r.becomeFollower(r.Term, m.From)
        // 添加日志
        r.handleAppendEntries(m)
    }
    // ...
}
```

follower 收到同步日志请求后，会将选举计时器置为 0，然后会尝试将日志追加到非持久化日志列表中.

```
func stepFollower(r *raft, m pb.Message) {
    switch m.Type {
    // ...
    case pb.MsgApp:
        // append消息
        // 收到leader的app消息，重置选举tick计时器，因为这样证明leader还存活
        r.electionElapsed = 0
        r.lead = m.From
        r.handleAppendEntries(m)
        // ...
   }
}
```

follower 和 candidate 同步日志时，会数据匹配，如果待同步消息的上一条日志能和节点已同步日志的最后一条日志匹配上，则接受新日志的同步，否则拒绝.

```
func (r *raft) handleAppendEntries(m pb.Message) {
    // 尝试添加到日志模块中
    if mlastIndex, ok := r.raftLog.maybeAppend(m.Index, m.LogTerm, m.Commit, m.Entries...); ok {
        // 添加成功，返回的index是添加成功之后的最大index
        r.send(pb.Message{To: m.From, Type: pb.MsgAppResp, Index: mlastIndex})
    } else {
        r.send(pb.Message{To: m.From, Type: pb.MsgAppResp, Index: m.Index, Reject: true, RejectHint: r.raftLog.lastIndex()})
    }
}
```
```
func (l *raftLog) maybeAppend(index, logTerm, committed uint64, ents ...pb.Entry) (lastnewi uint64, ok bool) {
    if l.matchTerm(index, logTerm) {
        // 首先需要保证传入的index和logTerm能匹配的上才能走入这里，否则直接返回false

        // 首先得到传入数据的最后一条索引
        lastnewi = index + uint64(len(ents))
        // 查找传入的数据从哪里开始找不到对应的Term了
        ci := l.findConflict(ents)
        switch {
        case ci == 0:
            // 没有冲突，忽略
        case ci <= l.committed:
            // 找到的数据索引小于committed，都说明传入的数据是错误的
            l.logger.Panicf("entry %d conflict with committed entry [committed(%d)]", ci, l.committed)
        default:
            // ci > 0的情况下来到这里
            offset := index + 1
            // 从查找到的数据索引开始，将这之后的数据放入到unstable存储中
            l.append(ents[ci-offset:]...)
        }
        // 选择committed和lastnewi中的最小者进行commit
        l.commitTo(min(committed, lastnewi))
        return lastnewi, true
    }
    return 0, false
}
```

## 8.8 应用层发送同步日志响应

与 8.6 小节类似，leader 节点在应用层会调用 Node.Step 方法将请求发送到算法层.

## 8.9 leader 提交日志

leader 每次收到同步日志的请求时， 会在定制状态机函数中做出响应.

倘若 follower 是因为日志进度滞后而拒绝，则会根据 Message.RejectHint 对缺失的日志进行补发.

倘若 follower 接收了同步日志的提议，leader 会在 raft.maybeUpdate 方法中更新对应节点的日志进度 Progress，并且在 raft.maybeCommit 中基于多数派原则更新已提交日志的索引.

```
func stepLeader(r *raft, m pb.Message) {
    // 检查消息发送者当前是否在集群中
    pr, prOk := r.prs[m.From]
    if !prOk {
        r.logger.Debugf("%x no progress available for %x", r.id, m.From)
        return
    }
    switch m.Type {
    case pb.MsgAppResp: // 对append消息的应答
        if m.Reject {   // 如果拒绝了append消息，说明term、index不匹配
            // ...
            if pr.maybeDecrTo(m.Index, m.RejectHint) {  // 尝试回退关于该节点的Match、Next索引
                // 再次发送append消息
                r.sendAppend(m.From)
            }
        } else {    // 通过该append请求
            if pr.maybeUpdate(m.Index) {    // 如果该节点的索引发生了更新
                // ...

                if r.maybeCommit() {
                    // 如果可以commit日志，那么广播append消息
                    r.bcastAppend()
                } 
                // ...
            }
        }
       // ...
    }
}
```

raft.maybeCommit 方法会基于各节点 Progress.Match 组成数组并进行逆序排列，最终下中位数的日志索引就是获得了多数派认可、已经可以提交的日志索引.

```
func (r *raft) maybeCommit() bool {
    // TODO(bmizerany): optimize.. Currently naive
    mis := make(uint64Slice, 0, len(r.prs))
    // 拿到当前所有节点的Match到数组中
    for id := range r.prs {
        mis = append(mis, r.prs[id].Match)
    }
    // 逆序排列
    sort.Sort(sort.Reverse(mis))
    // 排列之后拿到中位数的Match，因为如果这个位置的Match对应的Term也等于当前的Term
    // 说明有过半的节点至少comit了mci这个索引的数据，这样leader就可以以这个索引进行commit了
    mci := mis[r.quorum()-1]
    // raft日志尝试commit
    return r.raftLog.maybeCommit(mci, r.Term)
}
```

## 8.10 应用层应用已提交日志到状态机

应用层获得 Ready 结构体后感知到已提交日志索引发生了更新，则会调用 raftNode.publishEntries 方法将其应用到数据状态机当中.

```
func (rc *raftNode) serveChannels() {
    // ...
    for {
        select {
        // ...
        case rd := <-rc.node.Ready():
            // ...
            if ok := rc.publishEntries(rc.entriesToApply(rd.CommittedEntries)); !ok {
                rc.stop()
                return
            }
            // ....
            rc.node.Advance()
        // ...
        }
    }
}
```

## 9 读流程

## 9.1 整体流程

raft 节点处理读请求的流程为：

（1）当前节点为 leader，应用层调用 Node.Propose 发送读请求给算法层，leader 封装一轮带有读请求标识的心跳广播消息，通过 通过 Node.Ready 方法让应用层消费到，应用层调用通信模块转发给其他节点；之后调用 Node.Advance 开启下一轮交互；

（2）当前节点为 follower，应用层接收到来自 leader 的心跳请求，会调用 Node.Step 将请求发给算法层，算法层会将心跳响应结果封装到 Ready 结构体，通过 Node.Ready 方法让应用层消费到；应用层通过通信模块转发给 leader，之后调用 Node.Advance 开启下一轮交互；

（3）当前节点为 leader，应用层调用 Node.Propose 发送心跳响应给算法层，leader 接收到半数以上节点的 ack 则判断自身身份合法，封装读请求响应消息通过 Node.Ready 方法让应用层消费到，应用层收到消息后会读取数据状态机，对客户端的读请求进行响应.

![图片](https://mmbiz.qpic.cn/mmbiz_png/3ic3aBqT2ibZtfraTLrbaf4jIRxYndbL8iarJ3WicJy25GuAV72tfHV3OFcmvPQLDgOEKZWz9RYHOa0ItZcFlrAZPA/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=21)

## 9.2 应用层发送读请求

应用层 raftNode 调用 Node.ReadIndex 方法，通过 recvc 向算法层 goroutine 发送一条类型为 ReadIndex 的消息.

```
func (n *node) ReadIndex(ctx context.Context, rctx []byte) error {
    return n.step(ctx, pb.Message{Type: pb.MsgReadIndex, Entries: []pb.Entry{{Data: rctx}}})
}
```

## 9.3 follower 转发请求至leader

如果是 follower 接收到读请求，则会将请求转发给 leader：

```
func stepFollower(r *raft, m pb.Message) {
    switch m.Type {
    // ...
    case pb.MsgReadIndex:
        if r.lead == None {
            return
        }
        // 向leader转发此类型消息
        m.To = r.lead
        r.send(m)
    // ...
    }
}
```

## 9.4 leader 身份自验证

当 leader 接收到读请求后，会先将读请求添加到 readOnly 的读请求队列中，然后向所有节点广播心跳，并在心跳的 context 中带上读请求的 id，标识这是一笔特殊的心跳请求.

```
func stepLeader(r *raft, m pb.Message) {
    // These message types do not require any progress for m.From.
    switch m.Type {
    // ...
    case pb.MsgReadIndex:    
        // 把读请求到来时的committed索引保存下来
        r.readOnly.addRequest(r.raftLog.committed, m)
        // 广播消息出去，其中消息的CTX是该读请求的唯一标识
        // 在应答是Context要原样返回，将使用这个ctx操作readOnly相关数据
        r.bcastHeartbeatWithCtx(m.Entries[0].Data)
        return
    // ...
    }
    // ...
 }
```

## 9.5 leader 响应读请求

leader 接收到其他节点对于心跳请求的响应后，会通过读请求 id 将 ack 添加到 readOnly 中对应读请求状态 readIndexStatus 当中. 当一笔读请求已经拿到半数以上的心跳 ack 后，说明 leader 至少在收到这笔读请求的时刻，具有合法的身份，拥有最新的数据，因此会对这笔请求及之前挂起的读请求批量做出响应.

```
func stepLeader(r *raft, m pb.Message) {
  // ...
  // 检查消息发送者当前是否在集群中
  pr, prOk := r.prs[m.From]
  if !prOk {
      return
  }

  switch m.Type {
  // ...
    case pb.MsgHeartbeatResp:
    // ...
    // 收到应答调用recvAck函数返回当前针对该消息已经应答的节点数量
    ackCount := r.readOnly.recvAck(m)
    if ackCount < r.quorum() {
    // 小于集群半数以上就返回不往下走了
      return
    }

    // 调用advance函数尝试丢弃已经被确认的read index状态
    rss := r.readOnly.advance(m)
    for _, rs := range rss { // 遍历准备被丢弃的readindex状态
       req := rs.req
       // 否则就是来自外部，需要应答
       r.send(pb.Message{To: req.From, Type: pb.MsgReadIndexResp, Index: rs.index, Entries: req.Entries})
    }
   }
}
```

至此，全文结束，感谢费时阅读，欢迎批评交流.

继续滑动看下一个

小徐先生的编程世界

向上滑动看下一个