## 目录职责

| 目录               | 职责                          | 谁维护       |
| ---------------- | --------------------------- | --------- |
| `Clippings/`     | 原始资料，只进不改                   | 人工 ingest |
| `Wiki/Articles`  | 目录下有多个分类的子目录，文章摘要分类后保存在子目录下 | LLM 维护    |
| `Wiki/Summaries` | 文章总结                        | LLM 维护    |
| `Wiki/INDEX.md`  | 文章摘要的索引文件                   | LLM 维护    |

---

## 摘要格式（wiki/Summaries/）

文件命名：`S-<article-name>-.md` 

```yaml

---

id: S-XXX

title: 摘要标题

source: 来源

date: YYYY-MM-DD

tags:

  - 标签

---

## 核心结论

（3 条以内，每条一句话）

## 关键数据

（有数字/来源的结论，加粗关键数字）

## 疑点 / 待验证

（尚无定论的问题）

## 术语表

- 术语：定义

## 原始来源

[【raw/research/...】]

```

---

## 概念条目格式（wiki/concepts/）

文件命名：`C-XXX-<概念名>.md`（三位序号）

```yaml

---

id: C-XXX

title: 概念名称

updated: YYYY-MM-DD

---

## 定义

（1-2 句精准定义）

## 关联来源

- [【S-XXX 摘要标题】]

## 已知边界 / 局限

（该概念的适用范围、不适用场景）

## 版本 / 演进

（概念随时间的变化，如有）

```

---


## 索引维护（wiki/indexes/）

### All-Sources.md
所有 raw 文档的清单：

| ID | 文件路径 | 主题 | 日期 | 是否已编译 |
|----|----------|------|------|-----------|

### All-Concepts.md
所有概念条目的清单：

| ID | 概念名 | 关联来源数 | 最近更新 |
|----|--------|-----------|---------|

---

## 增量编译规则

1. 检查 `wiki/indexes/All-Sources.md`，找出「是否已编译 = ❌」的条目
2. 只处理未编译的 raw 文件
3. 完成后更新 All-Sources.md 对应条目为 ✅
4. 新增概念自动添加到 All-Concepts.md

---

## Q&A 存档格式（outputs/qa/）

文件命名：`QA-YYYY-MM-DD-<slug>.md`

```yaml
---
question: "问题原文"
asked_at: YYYY-MM-DD
sources:
  - [【S-XXX 摘要】]
  - [【C-XXX 概念】]
---

## TL;DR
（1-2 句结论）

## 结论
（详细推导）

## 证据
（链接回原始来源）

## 不确定性
（哪些地方还需验证）
```

---

## 健康检查规则（outputs/health/）

每周运行，检查三项，报告存 `outputs/health/YYYY-WXX.md`：

1. **一致性**：wiki/concepts/ 中是否有同一概念定义冲突
2. **完整性**：哪些概念条目缺定义、缺来源、缺例子
3. **孤岛**：哪些 wiki 文件入链 + 出链均少于 2

---
