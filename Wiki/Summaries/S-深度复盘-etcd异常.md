---
id: S-深度复盘-etcd异常
title: 深度复盘：重启 etcd 引发的 K8s 异常
author: 唐聪、王超凡、王子勇（腾讯云）
source: https://zhuanlan.zhihu.com/p/606087721
reference: Clippings/深度复盘-重启 etcd 引发的异常.md
date: 2026-04-12
tags:
  - etcd
  - Kubernetes
  - 故障复盘
  - TCP
  - 内核
---

## 核心内容总结

1. 腾讯会议扩缩容期间重启 etcd，触发 APIServer 部分资源（PVC 等）请求超时，但 etcd P99 监控指标显示正常。
2. 问题根源定位为：etcd 重启后大量 APIServer 瞬间新建连接，触发了 SYN Cookie 保护机制，同时客户端 `tcp_wan_timestamps=0` 导致后续包不带时间戳选项，两者共同作用使 MSS 塌缩至 48 字节。
3. 内核在 SYN Cookie 场景下若未收到客户端时间戳回传，会调用 `tcp_clear_options` 清空 window scale、timestamp、SACK 等选项，导致接收窗口大幅缩小。
4. 最终修复方案由 TKE 团队反馈给相关团队完成优化，云环境容器特殊网段配置是关键触发条件。
5. 经验教训：对现网保持敬畏，监控系统不仅要检测变更服务核心指标，更要对主调方的核心指标进行深入检测。

## 关键数据

- **etcd db size 警戒线**：接近 80% 时需提前干预
- **MSS 正常值**：~1400 字节（MTU 1500 - TCP/IP 头部 - 云网络协议头）
- **MSS 异常值**：仅 **48 字节**（窗口因子丢失后塌缩结果）
- **TCP 包异常特征**：每个返回包 <100 字节
- **诊断工具**：`tcpdump`（抓包）、`iproute2`/`ss`（TCP 参数分析）、内核源码（`tcp_get_info`、`tcp_clear_options`）

## 简述要点

在腾讯会议扩缩容期间，上海最大 K8s 集群出现部分 Pod 无法创建销毁、某些资源 Get/List 超时等问题。一线研发初步判断为控制面异常。TKE 团队深入排查后发现，变更记录显示几个小时前进行了 etcd 重启（db size 接近 80% 触发调大 quota）。表面上看 etcd P99 延时仅 500ms，带宽充足，但深入分析 APIServer 到 etcd 的 metrics 发现只有一个实例、某一类资源（PVC）的连接耗时异常高。进一步确认为 APIServer 与 etcd 之间特定 HTTP/2 长连接出现问题——抓包分析发现 MSS 仅 48 字节，大量小包导致上层应用超时。通过内核源码追踪定位到根因：etcd 重启触发大量短时新建连接，SYN Cookie 保护被激活，但客户端因 `tcp_wan_timestamps=0` 在非私有网段后续包不带时间戳，内核因此调用 `tcp_clear_options` 清空了 window scale 选项，使 MSS 计算塌缩至 48 字节。最终多团队协作，结合 tcpdump、iproute2、RFC 规范与 Linux 内核源码三重视角成功破案，并推动上游完成修复。

## 疑点 / 待验证

- `tcp_wan_timestamps` 特性在云环境容器中的默认配置是否有更优方案
- 此类 SYN Cookie 与 TCP Option 丢失的组合触发场景在超大规模集群中的普适性

## 术语表

- **MSS**（Maximum Segment Size）：TCP 最大分段大小，限制每次网络传输的数据包有效载荷，不含 TCP/IP 包头
- **MTU**（Maximum Transmission Unit）：最大传输单元，互联网设备可接收的最大数据包（含包头）
- **SYN Cookie**：一种防御 SYN 洪泛攻击的机制，通过将连接状态编码到 SYN+ACK 的序列号中，服务器无需保存半开连接状态
- **Window Scale**：TCP 窗口扩大因子，用于在高带宽高延迟网络中突破 16 位窗口字段的 65KB 限制
- **tcp_wan_timestamps**：内核参数，控制是否在外网（非私有网段）场景下发送 TCP 时间戳选项
- **tcp_clear_options**：内核函数，在特定场景（SYN Cookie 协商失败）下清空 timestamp、window scale、SACK 等选项
- **HTTP/2 Multiplexing**：HTTP/2 的多路复用机制，单个 TCP 连接上可并行交错传输多个数据流（Stream），每个流拥有唯一 ID

## 原始来源

[[Clippings/深度复盘-重启 etcd 引发的异常.md]]
