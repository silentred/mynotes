---
title: 在 Linux 系统中安装与使用 tmux：从入门到精通
source: https://geek-blogs.com/blog/install-tmux-linux/
author:
published: 2025-11-02
created: 2026-06-29
description: 在 Linux 终端操作中，你是否遇到过以下问题：需要同时运行多个命令行程序，却被终端窗口数量限制；远程连接服务器时，意外断开连接导致正在运行的任务中断；或者希望在一个屏幕内高效管理多个工作区？**tmux**（Terminal Multiplexer）正是解决这些问题的利器。tmux 是一款开源的终端复用工具，它允许你在单个终端窗口中创建、访问和控制多个独立的终端会话。即使终端窗口关闭或网络断开，tmux 会话依然可以在后台运行，确保任务持续执行。无论是开发、运维还是日常终端操作，tmux 都能显著提升工作效率。本文将详细介绍如何在 Linux 系统中安装 tmux，从基础用法到高级配置，再到最佳实践，帮助你快速掌握这款工具。
tags:
  - clippings
---
在 Linux 终端操作中，你是否遇到过以下问题：需要同时运行多个命令行程序，却被终端窗口数量限制；远程连接服务器时，意外断开连接导致正在运行的任务中断；或者希望在一个屏幕内高效管理多个工作区？ **tmux** （Terminal Multiplexer）正是解决这些问题的利器。

tmux 是一款开源的终端复用工具，它允许你在单个终端窗口中创建、访问和控制多个独立的终端会话。即使终端窗口关闭或网络断开，tmux 会话依然可以在后台运行，确保任务持续执行。无论是开发、运维还是日常终端操作，tmux 都能显著提升工作效率。

本文将详细介绍如何在 Linux 系统中安装 tmux，从基础用法到高级配置，再到最佳实践，帮助你快速掌握这款工具。

## 目录

## 1\. 什么是 tmux？

tmux 是一个终端复用器（Terminal Multiplexer），它允许用户在单个终端窗口中创建多个“会话”（Session），每个会话可包含多个“窗口”（Window），每个窗口又可分割为多个“面板”（Pane）。核心优势包括：

- **会话持久性** ：会话在后台运行，即使关闭终端或断开 SSH 连接，任务也不会中断。
- **多任务并行** ：在一个屏幕内同时操作多个终端（如编辑代码、运行服务、查看日志）。
- **窗口管理** ：灵活分割屏幕，支持水平/垂直分屏、调整大小、切换布局。
- **可定制性** ：通过配置文件自定义快捷键、外观、行为，甚至扩展功能。

## 2\. 安装 tmux

tmux 支持几乎所有 Linux 发行版，安装方式主要有两种：通过系统包管理器（简单、稳定）或从源码编译（获取最新版本）。

### 2.1 基于包管理器安装（推荐）

不同 Linux 发行版的包管理器命令不同，选择对应命令执行即可：

#### Debian/Ubuntu 或衍生系统（如 Mint、Pop!\_OS）

```bash
# 更新包索引
sudo apt update
# 安装 tmux
sudo apt install -y tmux
```

#### RHEL/CentOS 或衍生系统（如 Rocky Linux、AlmaLinux）

```bash
# CentOS 7 及以下
sudo yum install -y tmux
 
# CentOS 8/Rocky Linux 8+（使用 dnf）
sudo dnf install -y tmux
```

#### Fedora 系统

```bash
sudo dnf install -y tmux
```

#### Arch Linux 或衍生系统（如 Manjaro）

```bash
sudo pacman -Syu tmux  # -Syu 同时更新系统并安装
```

#### openSUSE 系统

```bash
sudo zypper install -y tmux
```

安装完成后，验证版本：

```bash
tmux -V  # 输出示例：tmux 3.2a
```

### 2.2 从源码编译安装（最新版本）

若系统包管理器中的 tmux 版本较旧（如需要使用最新特性），可从源码编译安装。以 Ubuntu 为例，步骤如下：

#### 1\. 安装依赖

tmux 依赖 `libevent` （事件处理库）和 `ncurses` （终端处理库）：

```bash
sudo apt install -y libevent-dev ncurses-dev build-essential
```

#### 2\. 下载源码

从 [tmux 官方 GitHub 仓库](https://github.com/tmux/tmux/releases) 获取最新版本（如 `3.3a` ）：

```bash
# 下载源码包（替换版本号为最新）
wget https://github.com/tmux/tmux/releases/download/3.3a/tmux-3.3a.tar.gz
# 解压
tar -zxvf tmux-3.3a.tar.gz
cd tmux-3.3a
```

#### 3\. 编译与安装

```bash
# 配置编译选项（默认安装到 /usr/local/bin）
./configure
# 编译（-j 4 表示使用 4 核加速）
make -j4
# 安装（需要 sudo 权限）
sudo make install
```

#### 4\. 验证安装

```bash
# 确保新安装的 tmux 在 PATH 中（/usr/local/bin 通常已包含）
tmux -V  # 输出：tmux 3.3a（版本与下载的一致）
```

> **注意** ：若后续需卸载源码安装的 tmux，进入源码目录执行 `sudo make uninstall` 。

## 3\. tmux 基础用法

tmux 的操作依赖 **前缀键** （默认 `Ctrl + b` ，下文简称 `Prefix` ），几乎所有命令都需先按 `Prefix` ，再按快捷键。

### 3.1 启动与退出 tmux

#### 启动 tmux

```bash
tmux  # 直接启动，会话默认命名为数字（如 0、1）
# 或指定会话名称（推荐，便于管理）
tmux new -s <会话名称>  # 示例：tmux new -s dev-session
```

#### 退出 tmux

- **临时离开（保留会话）** ：按 `Prefix + d` （detach，分离会话），会话在后台运行。
- **彻底退出（关闭会话）** ：在 tmux 终端中输入 `exit` 或按 `Ctrl + d` ，所有面板/窗口关闭后会话结束。

### 3.2 会话（Session）管理

会话是 tmux 的核心，所有窗口和面板都在会话中运行。

| 操作 | 命令（终端中执行） | 快捷键（tmux 内） |
| --- | --- | --- |
| 创建会话 | `tmux new -s <名称>` | `Prefix + :new -s <名称>` |
| 列出所有会话 | `tmux ls` 或 `tmux list-sessions` | `Prefix + s` |
| 附加（进入）会话 | `tmux attach -t <名称/ID>` | `Prefix + ( 或 )` （切换最近会话） |
| 重命名会话 | `tmux rename-session -t <旧名称> <新名称>` | `Prefix + $` |
| 关闭会话 | `tmux kill-session -t <名称/ID>` | `Prefix + :kill-session` （当前会话） |
| 切换会话 | `tmux switch-client -t <名称/ID>` | `Prefix + L` （上次会话） |

**示例** ：

```bash
tmux new -s blog  # 创建名为 blog 的会话
tmux ls           # 列出会话：blog: 1 windows (created Wed Aug 23 10:00:00 2023) [159x35]
tmux attach -t blog  # 进入 blog 会话
tmux kill-session -t blog  # 关闭 blog 会话
```

### 3.3 窗口（Window）管理

一个会话可包含多个窗口（类似标签页），每个窗口独立运行，默认全屏显示。

| 操作 | 快捷键（tmux 内） |
| --- | --- |
| 创建新窗口 | `Prefix + c` |
| 列出所有窗口 | `Prefix + w` （按 Enter 切换） |
| 切换到第 N 个窗口 | `Prefix + 0~9` （0 对应第 10 个窗口） |
| 切换到上/下一个窗口 | `Prefix + n` （next）/ `Prefix + p` （previous） |
| 重命名当前窗口 | `Prefix + ,` |
| 关闭当前窗口 | `Prefix + &` （需确认） |

**示例** ：在会话中按 `Prefix + c` 创建新窗口，按 `Prefix + 1` 切换到第 1 个窗口（从 0 开始计数）。

### 3.4 面板（Pane）管理

窗口可分割为多个面板（分屏），实现“一屏多窗”。

| 操作 | 快捷键（tmux 内） |
| --- | --- |
| 垂直分割（左右） | `Prefix + %` （Shift + 5） |
| 水平分割（上下） | `Prefix + "` （Shift + '） |
| 切换面板（方向键） | `Prefix + 方向键` （↑↓←→） |
| 切换面板（ hjkl 键） | `Prefix + h/j/k/l` （需配置，见 4.2） |
| 关闭当前面板 | `Prefix + x` （需确认） |
| 最大化/还原当前面板 | `Prefix + z` |
| 调整面板大小 | `Prefix + Ctrl + 方向键` （按住不放持续调整） |
| 旋转面板布局 | `Prefix + Space` （空格） |
| 显示面板编号 | `Prefix + q` （显示 1 秒） |

**示例** ：按 `Prefix + %` 垂直分屏，左侧编辑代码，右侧运行程序；按 `Prefix + z` 临时最大化当前面板，再按一次还原。

## 4\. tmux 配置文件详解

tmux 的默认配置可能不符合个人习惯，通过配置文件 `~/.tmux.conf` 可自定义几乎所有行为。

### 4.1 配置文件路径与加载

- **默认路径** ： `~/.tmux.conf` （用户级配置）或 `/etc/tmux.conf` （系统级配置，不推荐修改）。
- **创建配置文件** ：
	```bash
	touch ~/.tmux.conf  # 创建空配置
	```
- **加载配置** ：修改配置后，无需重启 tmux，执行以下任一操作：
	```bash
	# 方法 1：在 tmux 内执行命令
	Prefix + :source-file ~/.tmux.conf  # 或缩写 :so ~/.tmux.conf
	 
	# 方法 2：终端中执行
	tmux source-file ~/.tmux.conf
	```

### 4.2 常用配置示例

以下是一个实用的配置文件模板，每行都有注释说明功能：

```bash
# ~/.tmux.conf
 
# -------------------------- 基础设置 --------------------------
# 修改前缀键为 Ctrl + a（替代默认 Ctrl + b，更符合习惯）
set -g prefix C-a
# 解除默认前缀键 Ctrl + b 的绑定（可选）
unbind C-b
# 允许通过 Ctrl + a + a 快速切换到上一个窗口（类似 screen）
bind C-a send-prefix
 
# -------------------------- 窗口/面板导航 --------------------------
# 启用鼠标支持（选择面板、调整大小、切换窗口等）
set -g mouse on
 
# 使用 hjkl 键（Vim 风格）导航面板（替代方向键）
bind h select-pane -L  # 左
bind j select-pane -D  # 下
bind k select-pane -U  # 上
bind l select-pane -R  # 右
 
# 调整面板大小（hjkl 键，每次 5 行/列）
bind -r H resize-pane -L 5  # 向左扩大
bind -r J resize-pane -D 5  # 向下扩大
bind -r K resize-pane -U 5  # 向上扩大
bind -r L resize-pane -R 5  # 向右扩大
# -r 表示允许重复按（按住前缀键 + 方向键持续调整）
 
# -------------------------- 会话/窗口管理 --------------------------
# 新建窗口时自动命名为当前路径（而非默认 "bash"）
set -g automatic-rename on
 
# 窗口编号从 1 开始（默认从 0）
set -g base-index 1
set -g pane-base-index 1  # 面板编号从 1 开始
 
# 关闭窗口时不确认（默认需要按 y 确认）
bind & kill-window
 
# -------------------------- 外观设置 --------------------------
# 状态栏位置（top/bottom，默认 bottom）
set -g status-position bottom
 
# 状态栏样式（背景色、文字色）
set -g status-bg black
set -g status-fg white
 
# 窗口标签样式（当前窗口红色，其他灰色）
setw -g window-status-current-fg red
setw -g window-status-current-bg black
setw -g window-status-current-attr bold  # 加粗
 
# 状态栏显示内容（左：会话名，中：窗口列表，右：时间/日期）
set -g status-left "#[fg=green]Session: #S #[fg=white]"  # #S 表示会话名
set -g status-right "#[fg=cyan]%H:%M:%S #[fg=yellow]%Y-%m-%d"  # 时间+日期
set -g status-left-length 30
set -g status-right-length 40
 
# -------------------------- 其他优化 --------------------------
# 历史缓冲区大小（可回滚查看的行数，默认 2000）
set -g history-limit 10000
 
# 启用 256 色支持（避免终端颜色异常）
set -g default-terminal "screen-256color"
set -as terminal-overrides ',xterm*:sitm=\E[3m'  # 支持斜体
 
# 禁止自动同步面板（默认关闭，避免误触）
unbind ^s  # 解绑 Ctrl + s（可能与终端暂停冲突）
```

将上述内容保存到 `~/.tmux.conf` 并加载，即可获得更友好的使用体验。

## 5\. 高级用法与技巧

### 5.1 会话共享与协作

tmux 支持多用户共享同一个会话（如远程协助），前提是所有用户能通过 SSH 登录同一台服务器并拥有 tmux 权限。

**步骤** ：

1. 用户 A 创建会话： `tmux new -s shared` 。
2. 用户 B 登录服务器后，附加到会话： `tmux attach -t shared` （需与用户 A 同属一个用户组，或会话权限允许）。
3. 两人可实时看到对方操作，实现协作。

### 5.2 自动化与脚本

通过 tmux 命令行接口，可编写脚本自动化会话/窗口/面板创建。例如，创建一个开发环境会话：

```bash
#!/bin/bash
# 脚本名：dev-env.sh
 
# 检查会话是否存在，不存在则创建
if ! tmux has-session -t dev 2>/dev/null; then
  # 创建会话并在后台运行
  tmux new-session -d -s dev -n editor  # -n 窗口名
  
  # 在 editor 窗口中分割面板（垂直分屏，左侧 60% 宽）
  tmux split-window -v -p 40 -t dev:editor  # -v 垂直，-p 40% 高度
  
  # 在新面板中启动日志查看
  tmux send-keys -t dev:editor.2 "tail -f /var/log/app.log" C-m
  
  # 创建第二个窗口（终端）
  tmux new-window -n terminal -t dev
fi
 
# 附加到会话
tmux attach -t dev
```

执行脚本： `bash dev-env.sh` ，自动创建预配置的开发环境。

### 5.3 插件系统（tpm）

tmux 支持通过插件扩展功能，推荐使用 **tpm（tmux plugin manager）** 管理插件。

#### 安装 tpm

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

#### 配置插件（修改 ~/.tmux.conf）

在文件末尾添加：

```bash
# tpm 配置
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'  # 基础优化插件
set -g @plugin 'tmux-plugins/tmux-resurrect'  # 会话保存/恢复插件
 
# 初始化 tpm（必须放在文件末尾）
run '~/.tmux/plugins/tpm/tpm'
```

#### 常用插件推荐

- **tmux-resurrect** ：保存会话状态（窗口、面板布局、命令历史），重启后恢复。
- **tmux-continuum** ：自动保存会话，配合 resurrect 实现“会话持久化”。
- **tmux-yank** ：支持复制面板内容到系统剪贴板（需依赖 `xclip` 或 `xsel` ）。

#### 使用 tpm 管理插件

- 安装插件： `Prefix + I` （大写 i，从 GitHub 克隆插件）。
- 更新插件： `Prefix + U` 。
- 删除插件：编辑 `~/.tmux.conf` 移除插件行，执行 `Prefix + alt + u` 。

## 6\. 常见问题与 troubleshooting

### 问题 1：执行 tmux attach -t <会话> 提示“no sessions”

**原因** ：会话不存在或已被关闭。  
**解决** ：

- 检查会话列表： `tmux ls` ，确认会话名称/ID 是否正确。
- 若会话意外关闭，重新创建： `tmux new -s <名称>` 。

### 问题 2：鼠标无法选择面板或调整大小

**原因** ：未启用鼠标支持或配置冲突。  
**解决** ：

- 在 `~/.tmux.conf` 中添加 `set -g mouse on` ，并加载配置。
- 若使用旧版本 tmux（<2.1），需用 `set -g mode-mouse on` 和 `set -g mouse-resize-pane on` 。

### 问题 3：tmux 内中文显示乱码

**原因** ：终端编码或 tmux 字符集配置问题。  
**解决** ：

- 确保终端（如 iTerm2、GNOME Terminal）编码为 UTF-8。
- 在 `~/.tmux.conf` 中添加：
	```bash
	set -g default-terminal "xterm-256color"
	set -ga terminal-overrides ',*:enacs@:smacs@:rmacs@:lmacs@'
	```

### 问题 4：无法复制 tmux 面板内容到系统剪贴板

**解决** ：

- 安装 `xclip` 或 `xsel` （系统剪贴板工具）： `sudo apt install xclip` 。
- 安装插件 `tmux-yank` ，使用 `Prefix + y` 复制选中内容到剪贴板。

## 7\. 最佳实践

1. **使用有意义的会话名称** ：如 `work` 、 `blog` 、 `dev-project` ，避免默认数字 ID。
2. **版本控制配置文件** ：将 `~/.tmux.conf` 存入 Git 仓库，便于多设备同步（如 `dotfiles` 仓库）。
3. **优先学习快捷键** ：减少对鼠标的依赖，常用快捷键（如 `Prefix + d` 、 `Prefix + %` ）形成肌肉记忆。
4. **定期更新 tmux** ：新版本通常修复 bug 并增加功能，通过包管理器或源码更新。
5. **避免过度定制** ：配置以“提升效率”为目标，过多复杂绑定可能增加记忆负担。
6. **使用插件增强体验** ：如 `resurrect` 防止会话丢失， `tpm` 简化插件管理。

## 8\. 示例：一个典型的 tmux 工作流

假设你是一名开发者，日常工作流如下：

1. **创建会话** ： `tmux new -s backend` （后端开发会话）。
2. **分割面板** ：
	- `Prefix + %` 垂直分屏（左侧编辑器，右侧终端）。
		- `Prefix + "` 水平分屏（右侧下方面板查看日志）。
3. **启动任务** ：
	- 左侧： `vim main.py` （编辑代码）。
		- 右侧上： `python main.py` （运行服务）。
		- 右侧下： `tail -f logs/debug.log` （实时日志）。
4. **临时离开** ： `Prefix + d` 分离会话，关闭终端去吃饭。
5. **恢复工作** ：饭后重新连接服务器， `tmux attach -t backend` 继续编码。
6. **多窗口协作** ： `Prefix + c` 创建新窗口，运行数据库客户端或 SSH 到测试服务器。

## 9\. 参考资料

- **官方文档** ： [tmux GitHub](https://github.com/tmux/tmux) （包含完整手册和源码）。
- **man 手册** ： `man tmux` （终端中查看详细命令和配置说明）。
- **tpm 插件管理器** ： [tmux-plugins/tpm](https://github.com/tmux-plugins/tpm) 。
- **tmux 快捷键 cheat sheet** ： [tmuxcheatsheet.com](https://tmuxcheatsheet.com/) （常用快捷键速查）。
- **进阶教程** ： [《Tmux: Productive Mouse-Free Development》](https://pragprog.com/titles/bhtmux/tmux/) （书籍）。

通过本文的介绍，你已掌握 tmux 的安装、基础用法、配置优化和高级技巧。tmux 上手有一定门槛，但一旦熟悉，将成为终端工作中不可或缺的效率工具。开始尝试用 tmux 管理你的终端吧！