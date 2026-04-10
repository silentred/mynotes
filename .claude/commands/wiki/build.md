---
name: "Wiki: Build"
description: 增量构建 Wiki 摘要和概念，并维护索引文件, 记录日志
category: Workflow
tags: [构建, wiki]
---

1. 查找未构建的原始文章，List `Clippings` 目录下的文件，查看哪些文件包含 `clippings` 标签，带有 `clippings`标签的文件是未构建的
2. 处理未构建的文件:
	1. 第一步，将文件内容摘要，生成摘要文件到 `Wiki/Summaries` 目录下，并更新 `Wiki/Summaries/INDEX.md` 文件
	2. 第二步，提取最多1个文章内的重要概念，生成或更新到 `Wiki/Concepts` 目录下, 并更新 `Wiki/Concepts/INDEX.md` 文件
3. 在 `Wiki/Audit/LOG.md` 日志文件新增加一条日志，记录这次编译处理了哪个原始文章，新增或修改了哪些摘要和概念
4. 构建完成后，去除原始文件的 `clippings` 标签