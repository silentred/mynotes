---
id: C-HeuristicLearning
title: Heuristic Learning
reference: Clippings/Learning Beyond Gradients.md
updated: 2026-05-14
---

## 定义

Heuristic Learning（HL）是一种以程序代码而非神经网络参数为主体的学习范式：Coding Agent 通过修改代码（策略、状态检测器、测试、配置、memory）而非反向传播来迭代系统。它将 Deep RL 的"状态-动作-反馈-更新"闭环保留，但更新对象从梯度变成了代码维护，突破了传统 heuristic 无法规模化的维护成本瓶颈。

## 关联来源

[[Clippings/Learning Beyond Gradients.md]]

## 已知边界 / 局限

- **表达力上限**：纯代码无法处理复杂感知（如 ImageNet 级别视觉）和长程规划（Montezuma 需 86 个宏动作的组合才能得分，普通 policy.py 状态机装不下）
- **只增长不压缩会腐化**：HS 若不执行"压缩历史"操作，会积累大量局部补丁变成屎山代码，维护能力随之崩溃
- **Monteuma 反例**：说明需要可组合宏动作、可恢复搜索状态、长期 memory 等新程序形态，HL 当前框架未给出具体实现

## 实际案例

- **Breakout 864**（Jiayi Weng，Codex gpt-5.4）：从几何检测到卡住循环打破，从 fast_low_ball_lead 到后期"卡住偏移逐步收掉"，每步都有代码版本、视频回放、简化回归
- **MuJoCo Ant 6146+**：CPG+PD 节律步态 → residual MPC（6~8 步视窗）+ 终端速度代价 + 热启动计划衰减
- **Atari57 批量**：57 游戏 × 2 输入 × 3 seeds = 342 条无人值守轨迹，中位数 HNS 在 1M 步时远超同期 PPO 曲线
- **System 1/2 分工愿景**：专用 NN 负责感知/分类，HL 负责最新数据处理/规则/memory，LLM Agent 负责反馈并周期性从 HL 生成数据更新 NN
