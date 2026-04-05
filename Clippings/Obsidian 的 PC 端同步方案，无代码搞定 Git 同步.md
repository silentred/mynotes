---
title: "Obsidian 的 PC 端同步方案，无代码搞定 Git 同步"
source: "https://utgd.net/article/9642"
author:
  - "[[沨沄极客]]"
published:
created: 2026-04-05
description: "Git 是最不容易出错的文本同步方案，给 Obsidian 用上再合适不过。"
tags:
  - "clippings"
---
注：如果你正在找手机端同步方案 [^1] ，请先阅读本文创建 Git 仓库后，阅读《 [Obsidian 的手机端同步方案，iOS + Git + Shortcuts 实现自动同步](https://utgd.net/article/20315/) 》。

关于 Obsidian 同步这件事，似乎总能让人感到头疼。同步方案不是太少，而是太多。多到你难以辨别哪种方案是最合适自己的。而且有不少同步方法是未经验证的，一些想当然的方案其实并不适合 Obsidian。

这篇文章我想先聊聊 PC 之间的 Obsidian 库同步。也就是不论系统，可以在 Windows、macOS、Linux 之间稳定完成同步的方法：Git 同步方案。

## 看看官方的推荐方案

我们先来看看 Obsidian 的官方文档：

🔗 [Sync your notes across devices - Obsidian Help](https://help.obsidian.md/Getting+started/Sync+your+notes+across+devices)

文档里提到，他们最推荐的是自己的 Obsidian Sync 同步方案，也就是通过官方服务器同步。这需要每月付费。

其次，如果你需要在多个 PC 设备之间跨设备同步，他们也支持多个常规的同步云盘和工具：Dropbox、Google Drive、iCloud Drive、OneDrive、Syncthing 。

这似乎看上去很美好，你用任意一个主流云盘都能完成同步。事情就这么被解决了。

## 网盘实时同步的麻烦事

但实际上，由于 Obsidian 双向链接的特性，每当你在修改一个文件时，就有可能出现“同时修改多个其他文件”的情况。最常见的操作就是修改了某个“被广泛引用的文档的名称”，这会同时让其他文件中的引用链接一并改名。

如果此时你用了这些云盘的同步功能，并且做了一些错误设置和错误操作。比如把同步方案为增量同步到云端，或者在无网络的情况下在两台电脑分别编辑了文件，都会导致同步时出现文件冲突。

我曾经把我写的稿件全部通过 NAS 备份到 OneDrive 上做异地备份，其他编辑器中的 `.md` 文件都可以正常备份。只有 Obsidian 的库出现了大量的重复文件，比如只有一份的 `稿件.md` ，在 OneDrive 上出现了 `稿件 1.md` 、 `稿件 2.md` …… `稿件 21.md` ，多达 21 个重复的文件。

最终实际只有 2000 个文件的 Obsidian 库里，硬生生出现了 60000 多个文件。而 OneDrive 网页版一次只能删除 1000 个文件，而且因为内部文件过多也不让我直接删除整个文件夹。着实让我头疼了很久。

据我所知，通过 WebDAV、iCloud Drive 同步有时也会出现一些编辑冲突问题。频繁删改文件内容时，会出现“闪回”的情况，也就是丢失了最新一次的编辑内容，或者是被其他设备上的修改操作覆盖了修改。

这是由于网盘无法正确识别 Obsidian 更新文件的方式导致的，当用户做了有冲突的操作，网盘只能选择其中一个版本进行保留，或者是两个都保留。而这两种方案恰恰都不是我们想要的。

## 最佳文本处理方案：Git

其实像这样令人头疼的问题，遇到最多的就是开发者群体了。

多人协作开发代码时遇到的冲突，可远比个人笔记的冲突多得多。而 Git 正是最适合文本类内容同步的最佳方案。

通过 Git 同步的优势很明显：

1. 定时同步而非实时同步，可以尽可能减少实时同步造成的冲突和闪回。
2. 两边出现冲突时会提示，可以根据实际情况进行保留。
3. Git 完整保存历史版本，可以通过 Timeline 查看每个文件的变动历史。

## 需要做的准备

你需要先做一个决定，想把你的笔记托付给哪个 Git 平台做管理。

1. 公共的 Git 服务商有两家：海外的 Github、国内的 Gitee
2. 支持私有搭建的 Git 服务也推荐两家：海外的 Gitlab、国内的 Gogs.io 。

使用哪个服务的区别不大，反而是网络对同步速度的影响比较大。如果你只想同步，有一个稳定的体验，那我会推荐国内的 Gitee。如果你英文不错，能够解决大部分与网络有关的问题，那我会推荐 Github [^2] 。两者都可以创建私有仓库，不用担心笔记被别人看到。

而我个人使用的是 Gogs.io 的本地部署版本。较小的系统资源消耗，使其可以稳定运行在 NAS 上。具体搭建方式以后我会单独出一篇文章来介绍。

![Alt text](https://cdn.utgd.net/assets/uploads/2022/00/Pasted%20image%2020221228135551.png)

Gogs 中的仓库

## 所需配置

决定好哪个平台之后，你需要做三件事：

1. 创建一个仓库。
2. 同步仓库到本地。
3. 合并 Obsidian 库和 Git 仓库。
4. 安装 Obsidian Git 插件进行后续的同步。

我这里用 Github 做演示。

### 第一步：创建仓库

创建仓库并不复杂，你需要新建一个 Github 账号，然后在右上角点 New repository。

![Alt text](https://cdn.utgd.net/assets/uploads/2022/00/Pasted%20image%2020221228134249.png)

新建仓库

然后填写仓库名称，其他全部保持默认就可以。

![Alt text](https://cdn.utgd.net/assets/uploads/2022/00/Pasted%20image%2020221228134356.png)

设置仓库选项

### 第二步：同步仓库到本地

如果你熟悉 git ，可以直接通过 `git clone` 命令把仓库拉取到本地，这是最常用的方法。

```shell
git clone [仓库url]
```

注意：如果运行这个代码时报错”'git' 不是内部或外部命令，也不是可运行的程序“，这说明你电脑上还没有安装 git。你需要先在 [Git 官网](https://git-scm.com/downloads) 下载并安装 git 后才能正常进行后续操作。

如果你不熟悉 git，不想学习相关命令也没关系。2022 年了，已经有足够多的图形化工具可以帮你做到这一点。

你可以下载一个 [Github Desktop](https://desktop.github.com/) ，登陆后会显示所有的 Github 仓库，点击“Clone a Repository from the Internet”再选择刚刚创建的仓库，并选择一个本地位置，就可以完成拉取了。

![Alt text](https://cdn.utgd.net/assets/uploads/2022/00/Pasted%20image%2020221228135102.png)

Github Desktop 使用起来很方便

Github Desktop 也支持其他 Git 仓库，比如 Gitee、Gitlab 都可以。在第一步登录中选择 ”Skip this step“ 就可以管理其他 Git 仓库，选择仓库操作则变成了输入仓库链接。

使用图形化工具还有一个好处，看似你只是省了一步 `git clone` ，但如果在未来出现了同步冲突之类的问题，你也可以用 Github Desktop 的图形化界面进行冲突处理。

### 第三步：合并 Obsidian 库和 Git 仓库

将 Git 仓库同步到本地时，Git 仓库里是空的。而看教程的你，应该已经有一个 Obsidian 库了。

而 `git clone` 命令通常只允许你在空目录下执行。

所以你需要将两者合并，要么是手动把现有的 Obsidian 库完整移动到这个文件夹里（不要忘记复制隐藏的.obsidian 文件夹）。要么是把 Git 仓库里的隐藏的.git 目录完整挪到 Obsidian 库里。

**TIP：让 Git 库同时支持 iCloud Drive 的方法**

如果你在用 macOS，Obsidian 库应该位于 \`cd ~/Library/Mobile\\ Documents/iCloud~md~obsidian/Documents\` 这个 iCloud Drive 目录中。

这个目录的位置不建议移动，所以最好的办法就是在一个空目录下执行 \`git clone\` ，然后将隐藏的 \`.git\` 目录转移到上述目录中。

2024-02-23 更新：如果你不仅要在桌面端同步，还需要同步到手机端。同时使用 Git 和 iCloud 有一些值得注意的点，可以参考这篇文章： [《Obsidian 同步，为什么不要同时使用 iCloud 和 Git？》](https://utgd.net/article/20587)

### 第四步：安装 Obsidian Git 插件进行后续的同步

接下来你需要进 Obsidian ，打开这个转移好的目录，并在这个库中，安装一个名为 [Obsidian Git](https://github.com/denolehov/obsidian-git) 的插件。

安装完成后应该会自动出现一个 Git Control View 的侧边栏。如果没有，则按下 Ctrl + P，搜索 `Obsidian Git: Open Source Control View` ，就可以打开这个面板。

![Alt text](https://cdn.utgd.net/assets/uploads/2022/00/Pasted%20image%2020221228141205.png)

Obsidian Git 面板

有了这个插件，以后的同步操作你都可以在 Obsidian 内部进行了。

这个插件顶部的按钮对应了 Git 中最常见的几个操作。如果你对 Git 有一定的了解，应该对这些操作不会陌生。

1. Backup：备份，提交所有的更改，并且执行推送。
2. Commit：确认提交，但不推送。
3. Stage all：存储当前的变更。
4. Unstage all：取消存储变更。
5. Push：推送到远端，可以理解为推送到 Github。
6. Pull：从远端拉取到本地，可以理解为从 Github 拉取最新数据到本地。
7. Change Layout：改变下方文件的排布方式。
8. Refresh：刷新当前的文件变更情况。

如果你不想了解他们具体是干什么的，只想知道怎么做同步，那其实就两个按键有用：

1. Backup，第一个按钮，一次性完成提交并推送到 Github。
2. Pull，第六个按钮，从 Github 同步到本地。

到这一步就完成了所有的配置工作，第一次使用时，点击 Backup 就可以。

### 补充：初次使用 git 时出现报错的解决方法

有读者提到，如果此前从未使用过 git ，直接使用 Github Desktop 进行同步是可行的。

但此时打开 Obsidian 会提示两个错误：

![Alt text](https://cdn.utgd.net/assets/uploads/2023/02/FG-102023-q.png)

Obsidian 错误提示

这两个错误的意思分别是：没有指定分支、没有读取到用户名。所以这是一个账号设置错误。

至于在 Github Desktop 中能够正常使用，在 Obsidian 中却不行。究其原因，是因为授权方式是通过 Github 的账号密码进行登录的。而 Obsidian 用的是命令行，采用的授权方式不同，导致只有 Obsidian 无法访问 Github。

所以解决方法如下：

1. 打开终端，输入 `cd 存储库位置` ，比如 `cd D:\ObsidianLibrary` 来打开存储库。
2. 输入 `git remote show origin` 来检查当前分支情况，依据更详细的报错，可以解决第一个问题。
3. 如果此时尚未登陆，应该会弹出一个登录窗口，提示进行登录，此时输入“账号 + 令牌”，就可以完成登录了。注意这个时候的令牌与密码不同，要用 Github 的个人访问令牌登录。参考文档《 [创建个人访问令牌](https://docs.github.com/zh/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#%E5%88%9B%E5%BB%BA-fine-grained-personal-access-token) 》就可以生成令牌。

你也可以直接使用以下命令来设置全局身份。

```shell
git config --global credential.helper store
```

这行命令的作用是在 git 中全局启用凭证存储，启用后第一次 `git clone` 或者 `git push` 时会提示你输入“账户 + 令牌”。之后执行 git 操作都不再需要密码。

（此段落更新于 2023-02-10，感谢读者“黄师傅”）

## 更多的配置

### 如何启用自动同步

刚开始使用时，你也许不习惯每次手动点一下 Pull 按钮。

那你可以在 Obsidian Git 插件里启用选项 `Auto Backup after file change` ，让它每隔一段时间自动进行同步，默认是 10 分钟进行一次推送。下面有一个 `Auto pull` 的选项，默认 10 分钟进行一次拉取。

### 如何解决文件同步冲突？

如果你在一台电脑上改动了文件，但是忘记同步了，并且在自动同步之前关机了。然后继续在另一台电脑上修改了同一个文件，那么回到这台电脑上做同步时就有可能发生冲突了。

此时你可以选择自己手动解决这些冲突，在 Obsidian Git 界面中，每次提交时都会告诉你这些文件发生了哪些变化。

由于 Git 的应用非常普遍，如果出现了其他报错，根据报错提示进行搜索，往往可以在搜索引擎中找到答案。

### 不想同步布局和某些配置怎么办？

通过调整 Git 仓库目录下的隐藏文件.gitignore 文件，可以选择不同步某些文件。

根据 Obsidian 的官方文档，他们建议你在.gitignore 中添加 `.obsidian/workspace` 。

如果你已经同步了，那就输入这行命令，这会从仓库中删除文件，未来也不再同步到仓库里，但保留本地文件。

```
git rm .obsidian/workspace --cached
```

### 如何查看文件变动 Timeline

Obsidian 的 Obsidian Git 插件，主要作用是进行提交、拉取、推送这些操作。只能列举某次提交产生的所有变化，不能直观地看到单个文件变动的历史情况。

VSCode 内置了一个非常方便的功能：Timeline，它可以清晰的看到每个文件在每次 Git 提交中的变化情况。

你可以在 VSCode 中打开 Obsidian 仓库，在左侧文件目录下方找到“时间线”，就可以回顾这个文件经历了哪些版本了。

![Alt text](https://cdn.utgd.net/assets/uploads/2022/00/Pasted%20image%2020221228141436.png)

VSCode 中的时间线面板

## 局限性

任何方案都有其局限性。哪怕是 Obsidian Sync 官方服务提供的 5 个远程库，也有 10 GB / 个的容量限制（包括版本历史占用的容量） [^3] 。Git 同步也不例外。

Git 方案非常适合文字内容同步。其中的图片和 PDF 也可以被正常同步，只是无法追踪更改和保留历史版本。

但是如果你的 Obsidian 库中包含大量的超大 PDF，达到了 GB 级别，你可能会遇到 Git 服务商的限制。

- [Github 没有容量上限](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) 。但建议单个仓库最好小于 1 GB，强烈建议小于 5 GB。超出时会给你发送邮件。
- [Gitee 单个仓库容量上限为 500MB](https://gitee.com/help/articles/4283) ，用户总仓库容量为 5 GB。 [^4]

而且你也不应该用 Git 同步超大文件。

- Github 的限制是“单个文件不能超过 100MB”，超过 50MB 时会邮件提醒用户。
- Gitee 的限制是“单文件大小上限为 50MB”。

当然，如果你不介意同步的速度，就是想要 All in One，把宇宙万象都存在同一个仓库中。你可以选择自己搭建一个 Gitlab 服务器，本地部署的 Gitlab 允许你自己调整仓库大小为无限制容量、无附件大小限制。

## 小结

正如文章开头所说，同步的方案非常多，但经得起时间考验的却不多。

Git 本身就是一种非常适合文字内容的版本管理方案，不仅实现了同步的需求。也能为 Obsidian 库提供更好的版本管理功能。

---

[^1]: 注：如果你正在找手机端同步方案，请先阅读本文创建 Git 仓库后，阅读《 [Obsidian 的手机端同步方案，iOS + Git + Shortcuts 实现自动同步](https://utgd.net/article/20315/) 》。

[^2]: 目前 Github 在国内的直接访问速度非常慢，如果你不具备调试网络的能力，大概率会出现同步缓慢甚至同步失败的问题，非常影响同步体验。

[^3]: 经读者提醒，目前 Obsidian Sync 容量上限已经更新到 10 GB/仓库。

[^4]: 这里提到的限制，均为个人可以免费使用的 Gitee 社区版的限制，企业版不在本文讨论范围之内。