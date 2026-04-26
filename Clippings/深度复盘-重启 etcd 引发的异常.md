---
title: "深度复盘-重启 etcd 引发的异常"
source: "https://zhuanlan.zhihu.com/p/606087721"
author:
  - "[[黑洞https://cloudmesh.top/]]"
published:
created: 2026-04-12
description: "唐聪、王超凡，腾讯云原生产品中心技术专家，负责腾讯云大规模 TKE 集群和 etcd 控制面稳定性、性能和成本优化工作。 王子勇，腾讯云专家级工程师， 腾讯云计算产品技术服务专家团队负责人。 概况作为当前中国广泛…"
tags:
---
[唐聪](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E5%94%90%E8%81%AA&zhida_source=entity) 、王超凡，腾讯云原生产品中心技术专家，负责腾讯云大规模 TKE 集群和 etcd 控制面稳定性、性能和成本优化工作。

王子勇，腾讯云专家级工程师， 腾讯 [云计算](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E4%BA%91%E8%AE%A1%E7%AE%97&zhida_source=entity) 产品技术服务专家团队负责人。

## 概况

作为当前中国广泛使用的云视频会议产品， [腾讯会议](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E8%85%BE%E8%AE%AF%E4%BC%9A%E8%AE%AE&zhida_source=entity) 已服务超过 3 亿用户，能 [高并发](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E9%AB%98%E5%B9%B6%E5%8F%91&zhida_source=entity) 支撑千万级用户同时开会。腾讯会议数百万核心服务都部署在腾讯云 TKE 上，通过全球多地域多集群部署实现高可用容灾。在去年用户使用最高峰期间，为了支撑更大规模的并发在线会议的人数，腾讯会议与 TKE 等各团队进行了一轮新的扩容。

然而，在这过程中，一个简单的 [etcd](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=2&q=etcd&zhida_source=entity) 进程重启操作却触发了一个的诡异的 K8s 故障（不影响用户开会，影响新一轮后台扩容效率），本文介绍了我们是如何从问题现象、到问题分析、大胆猜测排除、再次复现、严谨验证、根治隐患的，从 Kubernetes 到 etcd 底层原理，从 TCP RFC 草案再到内核 TCP/IP [协议栈](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E5%8D%8F%E8%AE%AE%E6%A0%88&zhida_source=entity) 实现，一步步定位并解决问题的详细流程（最终定位到是特殊场景触发了 [内核](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=2&q=%E5%86%85%E6%A0%B8&zhida_source=entity) Bug）。希望通过本文，让大家对 etcd、Kubernetes 和内核的复杂问题定位有一个较为深入的了解，掌握相关方法论，同时也能让大家更好的了解和使用好 TKE，通过分享我们的故障处理过程，提升我们的透明度。

## 背景知识

首先给大家简要介绍下腾讯会议的简要架构图和其使用的核心产品 TKE Serverless 架构图。

腾讯会议极简架构图如下:

![](https://picx.zhimg.com/v2-8737575cd53dcda623866a9a01c3448d_1440w.jpg)

腾讯会议重度使用的 TKE Serverless 架构如下:

![](https://pic3.zhimg.com/v2-a745b88ef943f3bcbf170ab5147a6544_1440w.jpg)

腾讯会议几乎全部业务都跑在 TKE Serverless 产品上，Master 组件部署在我们metacluster 中（K8s in K8s)，超大集群可能有10多个 APIServer，etcd 由服务化的 etcd 平台提供，APIServer 访问 etcd 链路为 svc -> cluster-ip -> etcd endpoint。业务各个 Pod 独占一个轻量级的 [虚拟机](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E8%99%9A%E6%8B%9F%E6%9C%BA&zhida_source=entity) ，安全性、隔离性高，业务无需关心任何 Kubernetes Master、Node 问题，只需要专注业务领域的开发即可。

## 问题现象

在一次资源扩容的过程中，腾讯会议的研发同学晚上突然在群里反馈他们 [上海](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E4%B8%8A%E6%B5%B7&zhida_source=entity) 一个最大集群出现了业务扩容失败，收到反馈后研发同学，第一时间查看后，还看到了如下异常:

● 部分 Pod 无法创建、销毁

● 某类资源 Get、list 都是超时

● 个别组件出现了 Leader Election 错误

● 大部分组件正常，少部分控制器组件有如下 list pvc 资源超时日志

`k8s.io/client-go/informers/factory.go:134:Failedtowatch *v1.PersistentVolumeClaim:failedtolist *v1.PersistentVolumeClaim:theserverwasunabletoreturna responseinthetimeallotted,butmaystillbeprocessingthe request(getpersistentvolumeclaims) `

然而 APIServer 负载并不高，当时一线研发同学快速给出了一个控制面出现未知异常的结论。随后 TKE 团队快速进入攻艰模式，开始深入分析故障原因。

## 问题分析

研发团队首先查看了此集群相关变更记录，发现此集群在几个小时之前，进行了重启 etcd 操作。变更原因是此集群规模很大，在之前的多次扩容后，db size 使用率已经接近 80%，为了避免 etcd db 在业务新一轮扩容过程中被写满，因此系统进行了一个经过审批流程后的，一个常规的调大 etcd db quota 操作，并且变更后系统自检 etcd 核心指标正常。

我们首先分析了 etcd 的接口延时、带宽、watch 监控等指标，如下图所示，

etcd P99 延时毛刺也就 500ms，节点带宽最大的是平均 100MB/s 左右，初步看并未发现任何异常。

![](https://pica.zhimg.com/v2-eeec04ee7d3fc1302969417338956bd2_1440w.jpg)

随后又回到 APIServer，一个在请求在 APIServer 内部经历的 **各个核心阶段(如下图所示)**:

![](https://pica.zhimg.com/v2-532ddadf048cbb180189eb69dd46825a_1440w.jpg)

● [鉴权](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E9%89%B4%E6%9D%83&zhida_source=entity) （校验用户 token、证书是否正确）

● 审计

● 授权 （检查是否用户是否有权限访问对应资源）

● 限速模块 （1.20 后是优先级及公平管理）

● mutating [webhook](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=webhook&zhida_source=entity)

● validating webhook

● storage/cache

● storage/etcd

请求在发往 APIServer 前，client 可能导致请求慢的原因:

● client-go 限速， [client-go](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=3&q=client-go&zhida_source=entity) 默认 qps 5, 如果触发限速，则日志级别 4 以上（高版本 client-go 日志级别 3 以上）可以看到客户端日志中有打印 Throttling request took 相关日志

那到底是哪个阶段出现了问题，导致 list pvc 接口超时呢？

● 根据 client QPS 很高、并且通过 kubectl 连接异常实例也能复现，排除了 client-go 限速和 client 到 apiserver 网络连接问题

● 通过 [审计日志](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E5%AE%A1%E8%AE%A1%E6%97%A5%E5%BF%97&zhida_source=entity) 搜索到不少 PVC 资源的 Get 和 list 5XX 错误，聚集在其中一个实例

● 通过 APIServer Metrics 视图和 trace 日志排除 webhook 导致的超时等

● 基于 APIServer 访问 etcd 的 Metrics、Trace 日志确定了是 storage/etcd 模块耗时很长，但是只有一个 APIServer 实例、某类资源有问题

![](https://pic4.zhimg.com/v2-de871aba84dc8587d03926ba71ce7471_1440w.jpg)

那为什么 etcd 侧看到的监控延时很低，而 APIServer 访问 etcd 延时很高，而且只是某类资源出现问题，不是所有资源呢？

首先，我们查看下 APIServer 的 etcd 延时统计上报代码 (以 Get 接口为例)：

![](https://pic3.zhimg.com/v2-1b853199eda0f04a6a8d0934165e6786_1440w.jpg)

它统计的是整个 Get 请求(实际调用的是 etcd Range 接口)从 client 发出到收到结果的耗时， **包括了整个 [网络链路](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E7%BD%91%E7%BB%9C%E9%93%BE%E8%B7%AF&zhida_source=entity) 和 etcd RPC 逻辑处理耗时** 。

而 etcd 的 P99 Range 延时是基于 gRPC [拦截器](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E6%8B%A6%E6%88%AA%E5%99%A8&zhida_source=entity) 机制实现的，etcd 在启动 gRPC Server 的时候，会注册一个一元拦截器实现延时统计，在 RPC 请求入口和执行 RPC 逻辑完成时上报延时， **也就是它并不包括 RPC 请求在数据接收和发送过程中的耗时** ，相关逻辑封装在 monitor 函数中，简要逻辑如下所示:

![](https://pic3.zhimg.com/v2-62b52cc4c0b86eaa50cb6695c3b23258_1440w.jpg)

最后一个疑问为什么是某类资源出现问题?

APIServer 在启动的时候，会根据 Kubernetes 中的每个资源和版本创建一个独立etcd client，并根据配置决定是否开启 watch cache，每个 client 一般 1 个 TCP 连接，一个 APIServer 实例会高达上百个 etcd 连接。etcd client 与 etcd server 通信使用的是 gRPC 协议，而 gRPC 协议又是基于 HTTP/2 协议的。

PVC 资源超时，Pod、Node 等资源没超时，这说明是 PVC 资源对应的底层 TCP 连接/ [应用层](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E5%BA%94%E7%94%A8%E5%B1%82&zhida_source=entity) HTTP/2 连接出了问题。

![](https://picx.zhimg.com/v2-fa1de3fce724dc2eb4ff3807a2160f71_1440w.jpg)

在 HTTP/2 协议中，消息被分解独立的帧（Frame），交错发送，帧是最小的 [数据单位](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E5%8D%95%E4%BD%8D&zhida_source=entity) 。每个帧会标识属于哪个流（Stream），流由多个数据帧组成，每个流拥有一个唯一的 ID，一个 [数据流](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E6%B5%81&zhida_source=entity) 对应一个请求或响应包。如上图所示，client 正在向 server 发送数据流 5 的帧，同时 server 也正在向 client 发送数据流 1 和数据流 3 的一系列帧。一个连接上有并行的三个数据流，HTTP/2 可基于帧的流 ID 将并行、交错发送的帧重新组装成完整的消息。

也就是，通过 HTTP/2 的 [多路复用机制](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E5%A4%9A%E8%B7%AF%E5%A4%8D%E7%94%A8%E6%9C%BA%E5%88%B6&zhida_source=entity) ，一个 etcd HTTP/2 连接，可以满足高并发情况下各种 client 对 PVC 资源的查询、创建、删除、更新、Watch 请求。

那到底是这个连接出了什么问题呢？

明确是 APIServer 和 etcd 的网络链路出现了异常之后，我们又有了如下猜测：

● 异常实例 APIServer 所在节点出现异常

● etcd [集群](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=8&q=%E9%9B%86%E7%BE%A4&zhida_source=entity) 3 个节点底层网络异常

● etcd HTTP/2 连接最大 [并发流](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E5%B9%B6%E5%8F%91%E6%B5%81&zhida_source=entity) 限制 （单 HTTP/2 连接最大同时打开的并发流是有限制的）

● TCP 连接触发了内核未知 bug，连接疑似 hang 住一样

●.....

然而我们对 APIServer 和 etcd 节点进行了详细的系统诊断、网络诊断，除了发现 etcd 节点出现了少量毛刺丢包，并未发现其他明显问题，当前 etcd 节点也仅使用了 1/3 的节点带宽，但是请求依然巨慢，因此基本可以排除带宽超限导致的请求超时。

etcd HTTP/2 连接最大并发流限制的特点是此类资源含有较大的 [并发请求数](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E5%B9%B6%E5%8F%91%E8%AF%B7%E6%B1%82%E6%95%B0&zhida_source=entity) 、同时应有部分成功率，不应全部超时。然而通过我们一番深入排查，通过审计日志、Metrics 监控发现 PVC 资源的请求绝大部分都是 5XX 超时错误，几乎没有成功的，同时我们发现了一个 CR 资源也出现了连接异常，但是它的并发请求数很少。基于以上分析，etcd HTTP/2 连接最大并发流限制猜测也被排除。

问题再次陷入未知，此刻，就要寄出终极杀器——抓包大法，来分析到底整个 TCP [连接链路](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E8%BF%9E%E6%8E%A5%E9%93%BE%E8%B7%AF&zhida_source=entity) 发生了什么。

要通过抓包来分析具体请求，首先我们就要面临一个问题，当前单个 APIServer 到 etcd 同时存在上百个连接，我们该如何缩小范围，定位到具体异常的 TCP 连接呢？要定位到具体的异常连接，主要会面临以下几个问题：

1\. 数据量大：APIServer 大部分连接都会不停的向 etcd 请求数据，而且部分请求的数据量比较大，如果抓全量的包分析起来会比较困难。

2\. 新建连接无法复现：该问题只影响个别的资源请求，也就是只影响存量的几个长链接，增量连接无法复现。

3\. APIServer 和 etcd 之间使用 https 通信，解密困难，无法有效分析包的内容：由于长链接已经建立，已经过了 tls 握手阶段，同时节点安全管控限制，短时间不允许使用 [ebpf](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=ebpf&zhida_source=entity) 等 hook 机制，因此无法拿到解密后的内容。

为了定位到具体的异常连接，我们做了以下几个尝试：

1\. 首先针对响应慢的资源，不经过 Loadbalancer，直接请求 APIServer对应的 RS，将范围缩小到具体某一个 APIServer 副本上

2\. 针对异常的 APIServer 副本，先将它从 Loadbalancer 的后端摘掉，一方面可以尽快恢复业务，另一方面也可以避免有新的流量进来，可以降低抓包数据量（PS：摘掉 RS 的同时，Loadbalancer 支持发双向 RST，可以将客户端和 APIServer 之间的长链接也断掉）。

3\. 对异常的 APIServer 副本进行抓包，抓取 APIServer 请求 etcd 的流量，同时通过脚本对该异常的 APIServer发起并发查询，只查询响应慢的资源，然后对抓包数据进行分析，同一时间点 APIServer 对 etcd 有大量并发请求的长连接即为异常连接。

定位到异常连接后，接下来就是分析该连接具体为什么异常，通过分析我们发现 etcd 回给 APIServer 的包都很小，每个 TCP 包都是 100 字节以下：

![](https://picx.zhimg.com/v2-14aad2aec3422d8e00df94dc66b944e7_1440w.jpg)

通过 ss 命令查看连接的 TCP 参数，发现 MSS 居然只有 48 个字节：

![](https://picx.zhimg.com/v2-3085090559f6e87d76e5b74f40548ee1_1440w.jpg)

这里简单介绍下 TCP MSS(maximum segment size)参数, 中文名 [最大分段大小](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E6%9C%80%E5%A4%A7%E5%88%86%E6%AE%B5%E5%A4%A7%E5%B0%8F&zhida_source=entity) ，单位是字节，它限制每次 [网络传输](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E7%BD%91%E7%BB%9C%E4%BC%A0%E8%BE%93&zhida_source=entity) 的 [数据包](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E5%8C%85&zhida_source=entity) 的大小，一个请求由多个数据包组成，MSS 不包括 TCP 和 IP 协议包头部分。TCP 中还有一个跟包大小的参数是 MTU(maximum transmission unit)，中文名是最大传输单位，它是互联网设备（路由器等）可以接收的最大数据包的值，它包括 TCP 和 IP [包头](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=2&q=%E5%8C%85%E5%A4%B4&zhida_source=entity) ，以及 MSS。

受限于 MTU 值大小（最大1500），MTU 减去 TCP 和 IP 包头，云底层网络转发所使用的协议包头，MSS 一般在 1400 左右。然而在我们这里，如下图所示，对 ss [统计分析](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E7%BB%9F%E8%AE%A1%E5%88%86%E6%9E%90&zhida_source=entity) 可以看到，有 10 几个连接 MSS 只有 48 和 58。任意一个请求尤其是查询类的，都会导致请求被拆分成大量小包发送，应用层必定会出现各类超时错误，client 进而又会触发各种重试，最终整个连接出现完全不可用。

![](https://pic3.zhimg.com/v2-65957a57867742efa0676006d89f1bfe_1440w.jpg)

在确定是 MSS 值过小导致上层各种诡异超时现象之后，我们进一步思考，是什么地方改掉了 MSS。然而 MSS 协商是在三次握手中建立的，存量的异常连接比较难找到相关信息。

## 内核分析过程

### 抓包分析

为了进一步搞清楚问题发生的根本原因，我们在风险可控的情况下，在业务低峰期，凌晨1点，主动又做了一次相似的变更，来尝试复现问题。从抓到的包看 TCP 的选项，发现 MSS 协商的都是比较大，没有特别小的情况：

![](https://pica.zhimg.com/v2-33c0a588aa8a847d442846fb6bcd5d2a_1440w.jpg)

仅 SYN， SYN+ack 包带有 MSS 选项，并且值都大于 1000， 排除底层网络设备篡改了 MSS 造成的问题。

### 内核分析

那内核当中，什么地方会修改 MSS 的值？

假设一开始不了解 [内核代码](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E5%86%85%E6%A0%B8%E4%BB%A3%E7%A0%81&zhida_source=entity) ，但是我们能知道这个 MSS 字段是通过 ss 命令输出的，那么可以从 ss 命令代码入手。该命令来自于 iproute2 这个包，搜索下 MSS 关键词， 可知在 ss 程序中，通过内核提供的 sock\_diag netlink 接口， 查询到的信息。在 `tcp_show_info` 函数中做解析展示：

![](https://pic2.zhimg.com/v2-23e5b307294e733b48c30f848f3bdaf3_1440w.jpg)

可知 MSS 字段来自内核的 tcpi\_snd\_mss。

之后，从内核里面查找该值赋值的地方：

`22749net/ipv4/tcp.c<<tcp_get_info>> info->tcpi_snd_mss=tp->mss_cache; `

继续找 mss\_cache 的赋值位置：

![](https://picx.zhimg.com/v2-a100f208472250d82d5c761855dd8575_1440w.jpg)

只有 2 处，第一处是 tcp\_init\_sock 中调用，当中的赋值是初始值 `tcp_mss_DEFAULT 536U`, 与抓到的现场不匹配，直接可忽略。

第二处：

![](https://picx.zhimg.com/v2-0bd8d2b86631922474a3b20cbecb6597_1440w.jpg)

这里面可能 2 个地方会影响，一个是pmtu, 另外一个是 tcp\_bound\_to\_half\_wnd.

抓包里面没明显看到 MTU 异常造成的流异常反馈信息。聚焦在窗口部分：

![](https://pic4.zhimg.com/v2-8ad11797b20ca8a6f4e0ab1d28cf5133_1440w.jpg)

这里有个很可疑的地方。若是窗口很小，那么最后会取窗口与68字节 -tcp\_header\_len 的最大值，tcp\_header\_len 默认 20 字节的话，刚好是 48 字节。和咱们抓包看到的最小的 MSS 为 48 一致， 嫌疑很大。

那什么地方会修改最大窗口大小？

TCP 修改的地方并不多， `tcp_rcv_synsent_state_process` 中收到 SYN 包修改(状态不符合我们当前的 case），另外主要的是在 `tcp_ack_update_window` 函数中，收 ack 之后去更新：

![](https://pic4.zhimg.com/v2-d6b279e8d2b143a671a84c0798cb064f_1440w.jpg)

分析收到的 ack 包，我们能发现对方通告的窗口, 除了 SYN 之外，都是 29 字节：

![](https://pic4.zhimg.com/v2-f91bfc3e172f96d68e009f0979cdcc71_1440w.jpg)

SYN 包里面能看到 [放大因子](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E6%94%BE%E5%A4%A7%E5%9B%A0%E5%AD%90&zhida_source=entity) 是：

![](https://pic2.zhimg.com/v2-fbbfa66c83b6c806eec207e4989b55f1_1440w.jpg)

按理说，计算出来的窗口按照

`if(likely(!tcp_hdr(skb)->syn)) nwin<<=tp->rx_opt.snd_wscale; `

计算，应该是14848字节，但是从 MSS 的体现看，似乎这个 scale 丢失了。实际上，对比正常和异常的连接，发现确实 TCP 的 scale 选项在内核里面，真的丢了：

![](https://pic2.zhimg.com/v2-499a15fc90bd9b128fbe9fbf9943d2e5_1440w.jpg)

从 ss 里面对比正常和异常的连接看，不仅仅是 window scale 没了，连 timestamp, sack 选项也同时消失了！很神奇！

我们来看看 ss 里面获取的这些字段对应到内核的什么值：

ss 代码：

![](https://pic4.zhimg.com/v2-c1750edc8c566fe6ef969ce1d2ba798b_1440w.jpg)

![](https://pic3.zhimg.com/v2-577c0c9c5782949e4c708072d6229ebe_1440w.jpg)

对应到内核 tcp\_get\_info 函数的信息：

![](https://pic3.zhimg.com/v2-78ed11a38b20d676c966eb88b4c19052_1440w.jpg)

那内核什么地方会清空 window scale 选项？

搜索把 `wscale_ok` 改为 0 的地方，实际上并不多，我们可以比较轻易确定是 `tcp_clear_options` 函数干的：

`staticinlinevoidtcp_clear_options(structtcp_options_received*rx_opt) { rx_opt->tstamp_ok=rx_opt->sack_ok=0; rx_opt->wscale_ok=rx_opt->snd_wscale=0; } `

他同时会清空 ts, sack, scale 选项， 和我们的场景再匹配不过。

搜索 tcp\_clear\_options 的调用方，主要在tcp\_v4\_conn\_request和cookie\_check\_timestamp 两个地方，具体调用位置的逻辑都和 SYN cookie 特性有较强关联性。

`if(want_cookie&&!tmp_opt.saw_tstamp) tcp_clear_options(&tmp_opt); ``boolcookie_check_timestamp(structtcp_options_received*tcp_opt, structnet*net,bool*ecn_ok) { /*echoedtimestamp,lowestbitscontainoptions*/ u32options=tcp_opt->rcv_tsecr&TSMASK;  if(!tcp_opt->saw_tstamp){ tcp_clear_options(tcp_opt); returntrue; } `

两个条件都比较一致，看起来是 SYN cookie 生效的情况下，对方没有传递 timestamp 选项过来（实际上，按照 SYN cookie 的原理，发送给对端的回包中，会保存有编码进 tsval 字段低 6 位的选项信息），就会调用 tcp\_clear\_options， 清空窗口放大因子等选项。

从 [系统日志](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E7%B3%BB%E7%BB%9F%E6%97%A5%E5%BF%97&zhida_source=entity) 里面，我们也能观察到确实触发了 SYN cookie 逻辑：

![](https://pic4.zhimg.com/v2-9bd00406195430e68968a6b6fe4a29f3_1440w.jpg)

所以，根因终于开始明确，etcd 重启，触发了大量 APIServer 瞬间到 etcd 的新建连接，短时间的大量新建连接触发了 SYN cookie 保护检查逻辑。但是因为客户端没有在后续包中将 timestamp 选项传过来，造成了窗口放大因子丢失，影响传输性能

客户端为什么不在每一个包都发送 timestamp，而是只在第一个 SYN 包发送？

首先，我们来看看 RFC 规范，协商了 TCP timestamp 选项后，是应该选择性的发？还是每一个都发？

![](https://pic3.zhimg.com/v2-b9c9d529396f7fe366f0f0d36c390494_1440w.jpg)

答案是，后续每一个包 TCP 包都需要带上 [时间戳](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E6%97%B6%E9%97%B4%E6%88%B3&zhida_source=entity) 选项。

那么，我们的内核中为什么 SYN 包带了 TCP timestamp 选项，但是后续的包没有了呢？

搜索 tsval 关键词：

![](https://pic2.zhimg.com/v2-483b1cdbbcd8e89062801b4f9ee437d7_1440w.jpg)

可以看到 tcp\_syn\_options函数中，主动建连时候，会根据 sysctl\_tcp\_timestmps 配置选项决定是否开启时间戳选项。

查看客户端系统，该选项确实是打开的，符合预期：

`net.ipv4.tcp_timestamps=1 `

那为什么别的包都不带了呢？客户端角度，发了 SYN，带上时间戳选项，收到 [服务端](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E6%9C%8D%E5%8A%A1%E7%AB%AF&zhida_source=entity) SYN+ack 以及时间戳，走到 tcp\_rcv\_synsent\_state\_process 函数中，调用 tcp\_parse\_options 解析 TCP 选项：

![](https://pic1.zhimg.com/v2-0e7d3fb2152fc4dba67243fd7689a35c_1440w.jpg)

这里，就算服务端回包带了 TCP 时间戳选项，本机也要看两个 sysctl：

● sysctl\_tcp\_timestamps 这个比较好理解。内核标准的。

● sysctl\_tcp\_wan\_timestamps 这个看起来是针对外网打开时间戳的选项？很诡异。

此处就会有坑了，如果 wan\_timestamps 选项没打开，saw\_tstamp 不会设置为1， 后续也就不会再发送 TCP 时间戳选项。

查看 wan\_timestamps 设置，确实默认是关闭的：

`net.ipv4.tcp_wan_timestamps=0 `

所以这里真相也就明确了：因为 tcp\_timestamps 选项打开，所以内核建连是会发送时间戳选项协商，同时因为 tcp\_wan\_timestamps 关闭，在使用非私有网段的情况下，会造成后续的包不带时间戳（ [云环境](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E4%BA%91%E7%8E%AF%E5%A2%83&zhida_source=entity) 容器管控特殊网段的原因）。

和 SYN cookie 的场景组合在一起，最终造成了 MSS 很小，性能较差的问题。

tcp\_wan\_timestamps 是内部的特性，是为了解决外网时间戳不正确而加的特性，TKE 团队发现该问题后已反馈给相关团队优化，当前已经优化完成。

## 总结

本文问题表象，APIServer 资源请求慢，看似比较简单，实则在通过 APIServer Metrics 指标、etcd Metrics 指标、APIServer 和 etcd Trace 日志、审计日志、APIServer 和 etcd 源码深入分析后，排除了各种可疑原因，最后发现是一个非常底层的网络问题。

面对底层网络问题，在找到稳定复现的方法后，我们通过抓包神器 tcpdump，丰富强大的网络工具 iproute2 包（iproute2 包中的 ss 命令，能够获取 TCP 的很多底层信息，比如 rtt，窗口因子，重传次数等，对诊断问题很有帮助），再结合TCP RFC、linux 源码（代码面前无秘密，不管是 [用户态](https://zhida.zhihu.com/search?content_id=222817686&content_type=Article&match_order=1&q=%E7%94%A8%E6%88%B7%E6%80%81&zhida_source=entity) 工具还是内核态），多团队的协作，成功破案。

通过此案例，更让我们深刻体会到，永远要对现网生产环境保持敬畏之心，任何操作都可能会引发不可预知的风险，监控系统不仅要检测变更服务核心指标，更要对主调方的核心指标进行深入检测。
