---
id: C-信任链与CA
title: 信任链与CA
reference: Clippings/TLS完全指南.md
updated: 2026-04-26
---

## 定义

数字证书生态中，CA（证书颁发机构）以分层签名构建信任链：根 CA 自签名，中间 CA 由根 CA 签署，最终实体证书由中间 CA 签署，浏览器预置根 CA 公钥作为信任锚点验证整条链的真实性。

## 关联来源

[[Clippings/TLS完全指南.md]]

## 已知边界 / 局限

- 根 CA 被植入操作系统/浏览器，权限极大，一旦根 CA 私钥泄露或被滥用，整个 PKI 体系崩溃
- 自签名 CA 不被公共浏览器信任，仅适用于企业内部私有 PKI
- 信任链验证是链式依赖，任何中间环节出问题都会导致最终实体证书不可信

## 实际案例

- HTTPS 网站证书：由 Digicert、Let's Encrypt 等商业或公益 CA 签署，浏览器自动验证
- Kubernetes mTLS：企业自签名 CA（如 cfssl）签署所有服务证书，Istio 等服务网格自动实现双向认证
- GitHub/GitLab SSH 证书：用户自签名后手动添加信任
