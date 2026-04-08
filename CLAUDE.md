## 目录职责

| 目录                        | 职责                                                     | 谁维护    |
| ------------------------- | ------------------------------------------------------ | ------ |
| `Clippings/`              | 原始资料，只进不改                                              | 人工 维护  |
| `Wiki/Articles`           | 目录下包含多个md文件，文件使用Tag名称命名，内部使用 dataview 查询语句列出包含 Tag 的文章 | 人工  维护 |
| `Wiki/Summaries`          | 存放文章总结的 md 文件                                          | LLM 维护 |
| `Wiki/Summaries/INDEX.md` | 存放文章总结索引文件                                             | LLM 维护 |
| `Wiki/Concepts`           | 存放概念名称和简述的 md 文件                                       | LLM 维护 |
| `Wiki/Concepts/INDEX.md`  | 存放概念的索引文件                                              | LLM 维护 |

---

## 摘要格式（Wiki/Summaries/）

文件命名：`S-<article-name>-.md` 

```yaml
---

id: S-<article-name>
title: 摘要标题
author: 作者
source: 来源
date: YYYY-MM-DD
tags:
  - 标签
---

## 核心结论

（3 条以内，每条一句话）

## 关键数据

（有数字/来源的结论，加粗关键数字）

## 疑点 / 待验证

（尚无定论的问题）

## 术语表

- 术语：定义

## 原始来源

[[Clippings/<artical-name>.md]]

```

---

## 概念条目格式（Wiki/Concepts/）

文件命名：`C-<concept-name>.md`

```yaml
---

id: C-<concept-name>

title: 概念名称

updated: YYYY-MM-DD

---

## 定义

（1-2 句精准定义）

## 关联来源

[[Clippings/<artical-name>.md]]

## 已知边界 / 局限

（该概念的适用范围、不适用场景）

## 版本 / 演进

（概念随时间的变化，如有）

```

---


## 索引维护

### Wiki/Summaries/INDEX.md
所有 Clippings 文档的清单：

| ID  | 文件路径 | 主题  | 更新时间 |
| --- | ---- | --- | ---- |

### Wiki/Concepts/INDEX.md
所有概念条目的清单：

| ID  | 概念名 | 关联来源数 | 更新时间 |
| --- | --- | ----- | ---- |

---

## 增量编译规则

1. List `Clippings` 下的文件，查看哪些文件包含 `clippings` 标签，这些文件是未编译的
2. 处理未编译的文件:
	1. 第一步，将文件内容摘要，生成摘要文件到 `Wiki/Summaries` 目录下
	2. 第二步，提取最多2个文章内的重要
3. 完成后更新 All-Sources.md 对应条目为 ✅
4. 新增概念自动添加到 All-Concepts.md

---
