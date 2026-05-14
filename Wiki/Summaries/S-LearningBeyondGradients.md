---
id: S-LearningBeyondGradients
title: "Learning Beyond Gradients：Heuristic Learning 下一个范式"
author: Jiayi Weng
source: https://trinkle23897.github.io/learning-beyond-gradients/#zh
reference: Clippings/Learning Beyond Gradients.md
date: 2026-05-14
tags:
  - AI
  - Continual Learning
  - Coding Agent
  - RL
  - Heuristic Learning
---

## 核心内容总结

1. Coding Agent（GPT-5.4）不训练神经网络，通过持续"写代码→看失败→改策略→加测试→看回放"的循环，在 Breakout（864 满分）、MuJoCo Ant（6146+）、HalfCheetah（11836.7）、Atari57（批量 342 条轨迹，1M 步时中位数 HNS 远超 PPO 早期曲线）等任务上达到/超越 Deep RL 水平，核心突破是**改变了 heuristic 维护成本曲线**。
2. 提出 **Heuristic Learning（HL）** 概念：学习主体由程序代码而非神经网络参数构成，Coding Agent 通过修改代码（policy、检测器、测试、配置、memory）而非反向传播来迭代策略；长期维护的对象称为 **Heuristic System（HS）**，包含程序策略、状态表示、反馈入口、实验记录、回放/测试、memory 及更新机制。
3. HL 相比 Deep RL 有可解释性、样本效率（一次有效代码更新直接跳到新策略）、可回归验证（旧能力固化为测试/replay/golden case）、可约束过拟合、避免部分灾难性遗忘等优势。
4. 健康 HS 必须同时执行两个操作：**吸收反馈**（把新失败、新日志写回系统）和**压缩历史**（把局部补丁折成更简单的表示）——只增长不压缩的 HS 终将腐化为屎山代码。
5. 下一个范式预言：Pretrain → RLHF → Large-scale RL/RLVR → **HL**。最有前景的方向是 HL + 神经网络结合：HL 处理在线数据快速生成可回归经验，周期性更新神经网络（System 1/2 分工：NN/HL 负责感知和安全边界，LLM Agent 负责反馈和改进）。

## 关键数据

- **Breakout**：387 → 507 → 839 → **864**（理论最高分），纯图像版本 14.5K 策略本地步达满分
- **MuJoCo Ant**：2291 → 6146+（CPG+PD → residual MPC + 终端速度代价 + 热启动计划）
- **HalfCheetah**：5 seeds 均值 **11836.7**（staged-tree MPC）
- **VizDoom D3**：10 seeds 均值 **557.0**（纯 CV，无 NN）
- **Atari57**：342 条无人值守轨迹，1M 步 native_obs HNS 中位数 **0.32**（远高于同期 PPO 曲线），到 9.7M 步达 **0.81**
- **Atari57 对比 PPO**：best single run Codex median HNS **1.18** > CleanRL PPO 0.98 > OpenAI PPO2 0.80

## 简述要点

Jiayi Weng（EnvPool 作者）发现 Coding Agent 不训练神经网络，仅维护一套持续迭代的软件系统，就能在多个任务上达到 Deep RL 量级表现，由此提出 Heuristic Learning。核心洞察：**过去 heuristic 看起来没用，不是因为它弱，而是没人养得起**——coding agent 改变的是维护成本曲线。Breakout 策略从 387 分爬到满分 864，每一步都有代码版本记录、视频回放、失败模式分析和简化回归。Atari57 的 342 条批量轨迹证明该方法在完全无人工介入下依然有效，Montezuma 揭示了 HS 的边界：需要宏动作、可恢复搜索状态和长期 memory 等新程序形态。HL 不是要替代神经网络，而是与 RL 形成互补：HL 生成数据，NN 内化经验——凡是可以被持续迭代的，都开始能被解决。

## 疑点 / 待验证

- HL 能否在更复杂感知任务（如 ImageNet 级别视觉）上证明可行性
- Montezuma 暴露的表达力问题——可组合宏动作、可恢复状态的具体接口设计尚无成熟方案
- HL 与神经网络结合的 post-training 管道，具体实现细节（数据筛选、周期性更新策略）仍未展开

## 术语表

- **Heuristic Learning（HL）**：以程序代码为主体、通过 Coding Agent 修改代码而非反向传播来迭代策略的学习范式；更新走代码路径（policy、检测器、测试、配置、memory）
- **Heuristic System（HS）**：HL 的长期维护对象，包含程序策略、状态表示、反馈入口、实验记录、回放/测试、memory 及 Coding Agent 更新机制；单条规则不够，需全部接起来
- **耦合复杂度（Couping Complexity）**：Coding Agent 一次更新需同时照顾的相互牵连状态、规则、测试、反馈和历史量；由模块边界、测试覆盖、工具质量、模型能力共同决定
- **灾难性遗忘（Catastrophic Forgetting）**：Deep RL 中新任务参数覆盖旧能力；HL 缓解方式是将旧能力固化为测试、replay、golden case，而非依赖模型自己记忆
- **Monteuma's Revenge 反例**：需要 86 个宏动作的开环执行才能得分，说明普通 policy.py 状态机无法装下长期规划类任务
- **System 1/2 + HL 分工**：专用 NN（System 1，感知/分类）+ HL（System 1，规则/安全/memory）+ LLM Agent（System 2，反馈 + 周期性提取 HL 数据更新 NN）

## 原始来源

[[Clippings/Learning Beyond Gradients.md]]
