---
id: S-网络库糟糕设计
title: 网络库常见的糟糕设计
author: Jack
source: https://www.jackarain.org/2024/06/07/network-library-design.html
reference: Clippings/网络库常见的糟糕设计有哪些.md
date: 2024-06-07
tags:
  - cpp
  - network
  - design
---

## 核心内容总结

网络库 copy 用户数据会增加内存消耗和 CPU 负担，更重要的是导致内存使用量失控，放弃 TCP 滑动窗口机制。TCP 滑动窗口机制可以实现生产者和消费者的平衡，协程编程正是基于此完成状态实现背压控制。优秀网络库应让用户指定内存分配器，boost.beast 的 fast 示例全程仅一次堆分配。网络库应支持多种 OS 底层接口（epoll、iocp、io_uring），同步阻塞接口在简单场景下也应是可选项。one-op/one-callback 机制支持协程扩展，上古风格固定回调的做法是愚蠢的。不跨平台和不提供异步接口的网络库没有意义。OS 错误代码应真实传递而非隐藏。Socket 抽象应分层设计（TCP socket → SSL stream → WebSocket）。网络库不应被设计为应用程序框架。

## 关键数据

boost.beast 的 fast 示例在所有网络连接上的内存分配仅此一次，展示了用户指定分配器与最小堆使用的极致结合。

## 简述要点

很多 C++ 网络库设计不得要领，默认用户不会频繁发送数据是错误假设。**零拷贝**设计让用户直接传递数据内存地址，避免复制，同时充分利用 **TCP 滑动窗口** 机制实现生产者和消费者平衡。协程编程（`co_await async_send`）正是基于发送完成状态实现**背压控制**。网络库应支持多种 OS 接口（epoll/iocp/io_uring），提供 **one-op/one-callback** 异步机制，分层抽象 Socket（TCP → SSL → WebSocket），并作为库而非框架存在。

## 疑点 / 待验证

io_uring 在高并发场景下的实际性能收益与兼容性之间的权衡尚未展开。零拷贝实现依赖 Linux sendfile/mmap 等机制，不同平台的具体实现路径差异较大。

## 术语表

- 零拷贝（Zero-Copy）：网络库不复制用户数据，直接持有用户内存地址进行发送，减少内存复制开销。
- TCP 滑动窗口（Sliding Window）：TCP 的流量控制机制，接收端通过窗口大小告知发送端可发送数据量。
- 背压（Backpressure）：下游消费者处理速度跟不上上游生产者时产生的反向压力。
- one-op/one-callback：每次 I/O 操作独立指定回调，支持协程扩展。

## 原始来源

[[Clippings/网络库常见的糟糕设计有哪些]]
