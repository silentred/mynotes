---
title: "vim列删除、列修改"
source: "https://www.cnblogs.com/bistu/p/16900719.html"
author:
  - "[[ThinkStu]]"
published: 2022-11-17
created: 2026-08-10
description: "vim 块操作 一、列修改 首先进入 vim ，按下快捷键 ctrl + v进入块操作模式。然后按上下键选中你想要批量修改的文..."
tags: []
---
> vim 块操作

## 一、列修改

1. 首先进入 vim ，按下快捷键 `ctrl + v` 进入 `块操作模式` 。
2. 然后按 `上下键` 选中你想要批量修改的文本列。
3. 在 Esc 模式下输入大写的 `I ` 进入修改模式，输入要插入的内容，最后按 Esc 退出。 ==注意== ：在插入文本时，vim 会自动切换为一行编辑模式（ **这不是错误** ！），在你按 Esc 退出之后，vim会自动在这几行前面添加相同的内容。
```bash
#test1

#test2

#test3
```

## 二、列删除

1. 首先进入 vim ，按下快捷键 `ctrl + v` 进入 `块操作模式` 。
2. 然后按 `上下键` 选中你想要批量删除的列文本内容。
3. 在 Esc 模式下输入小写的 `d` 删除选中的列文本，输入大写的 `D` 删除选中的所有行。

---

范例：

```bash
# Settings for a TLS enabled server.

#

#    server {

#        listen       443 ssl http2;

#        listen       [::]:443 ssl http2;

#        server_name  _;

#        root         /usr/share/nginx/html;

#

#        ssl_certificate "/etc/pki/nginx/server.crt";

#        ssl_certificate_key "/etc/pki/nginx/private/server.key";

#        ssl_session_cache shared:SSL:1m;

#        ssl_session_timeout  10m;

#        ssl_ciphers PROFILE=SYSTEM;

#        ssl_prefer_server_ciphers on;

#

#        # Load configuration files for the default server block.

#        include /etc/nginx/default.d/*.conf;

#

#        error_page 404 /404.html;

#            location = /40x.html {

#        }

#

#        error_page 500 502 503 504 /50x.html;
```