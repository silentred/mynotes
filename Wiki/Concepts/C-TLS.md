---
id: C-TLS
title: TLS
reference: Clippings/TLS完全指南.md
updated: 2026-04-26
---

## 定义

传输层安全协议（Transport Layer Security，TLS）是建立在 TCP 之上的加密通信协议，通过非对称加密协商对称密钥实现高效安全数据传输，结合 CA 数字签名体系验证通信双方身份，是 HTTPS 的安全基础。

## 关联来源

[[Clippings/TLS完全指南.md]]

## 已知边界 / 局限

- CA 信任模型的根本弱点：CA 机构可能说谎（如 CNNIC 争议），信任完全依赖社会声誉
- 自签名证书只能用于封闭网络，公开环境需浏览器/操作系统预装根 CA
- mTLS 在超大规模分布式系统中的证书管理和轮换是工程难点

## 实际案例

- **HTTPS**：浏览器验证 Web 服务器身份，用户通过账号密码进一步验证
- **Kubernetes mTLS**：kubectl 与 apiserver 双向证书验证，所有节点（master/node）预装公司 CA 证书
- **内部微服务通信**：自签名 CA 为每个服务和雇员签发证书，所有机器预装公司 CA 实现信任网络
