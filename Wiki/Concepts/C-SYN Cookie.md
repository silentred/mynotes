---
id: C-SYN Cookie
title: SYN Cookie
reference: Clippings/深度复盘-重启 etcd 引发的异常.md
updated: 2026-04-12
---

## 定义

SYN Cookie 是一种防御 SYN 洪泛攻击的 TCP 协议扩展，通过将连接状态信息编码到服务端发送的 SYN+ACK 序列号中（cookie），使服务器无需保存半开连接状态，从而在遭受攻击时仍能维持服务。

## 关联来源

[[Clippings/深度复盘-重启 etcd 引发的异常.md]]

## 已知边界 / 局限

- **窗口扩大因子（Window Scale）丢失**：当 SYN Cookie 生效时，若客户端后续包未携带时间戳选项（`tcp_wan_timestamps=0` 或非私有网段场景），内核会调用 `tcp_clear_options` 清空 window scale、timestamp、SACK 等选项，导致有效接收窗口大幅缩小。
- **MSS 塌缩风险**：window scale 丢失后，MSS 计算结果可从正常的 ~1400 字节塌缩至 48 字节（`max(接收窗口, 48)` 逻辑），严重影响 TCP 传输效率。
- **适用场景**：短时大量新建连接触发保护（`tcp_syncookies`），而非持续攻击。
- **不适用场景**：正常负载下的连接建立，或客户端已正确协商所有 TCP 选项。

## 实际案例

**腾讯会议 K8s 集群 etcd 重启故障**（2023）：etcd 重启触发大量 APIServer 瞬间重连，短时新建连接高峰激活 SYN Cookie 保护。客户端因云环境容器特殊网段配置（`tcp_wan_timestamps=0`）后续包不带时间戳，内核清空 window scale 选项，导致 APIServer 到 etcd 的 HTTP/2 连接 MSS 塌缩至 48 字节，大量小包使 PVC 等资源请求持续超时，最终影响业务扩缩容。最终由 TKE 团队定位并推动上游完成修复。
