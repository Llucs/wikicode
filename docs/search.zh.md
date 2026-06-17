---
title: 搜索 wiki
description: 如何搜索 WikiCode。
created: 2026-06-03
tags:
  - meta
  - reference
status: stable
---

# 搜索 wiki

WikiCode 是完全可搜索的。搜索索引在部署时构建，完全在浏览器中运行，因此查询是即时的，并且没有数据离开你的机器。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">创建时间：2026-06-03</span>
<span class="wikicode-meta-updated">最后更新：自动 (git)</span>
</div>

## 如何搜索

<div class="grid cards" markdown>

- :material-magnify: __搜索栏__

    点击任意页面右上角的放大镜图标（或按键盘上的 ++slash++）来打开搜索弹窗。

- :material-keyboard: __键盘快捷键__

    - ++slash++ — 聚焦搜索栏。
    - ++esc++ — 关闭搜索弹窗。
    - ++arrow-up++ / ++arrow-down++ — 在结果中移动。
    - ++enter++ — 打开高亮的结果。

- :material-format-letter-case: __提示__

    - 搜索是**基于子串**的。输入 `mkdocs` 会匹配任何包含 "mkdocs" 的页面。
    - 默认情况下搜索是**不区分大小写**的。
    - 引号内的词组匹配精确子串：`"open hands"`。
    - 多个单词会匹配包含所有这些单词的页面。

</div>

## 索引内容

搜索索引覆盖站点上渲染的所有 Markdown 页面：

- `docs/` 下的文章、指南和参考页面。
- `projects/` 下的项目摘要。
- `snippets/` 下的代码片段描述。
- `docs/tools/` 下的工具页面。
- `blog/` 下的博客文章。
- 代码块中的文本（因此你可以搜索函数名或 CLI 标志）。

索引会在每次推送到 `main` 分支时重新生成，因此始终与发布内容保持同步。

## 为什么使用客户端搜索

- **隐私.** 查询不会发送到远程服务。
- **速度.** 结果会随输入即时出现。
- **成本.** 除了静态站点外无需托管其他内容。
- **离线.** 站点加载后，索引会存储在浏览器缓存中，即使没有网络也能继续使用。

## 添加自定义搜索快捷方式

如果你想要一个打开搜索弹窗并预填充搜索词的深度链接，在搜索栏被聚焦一次后，在站点 URL 后添加 `?q=<query>`。具体行为取决于 Material 主题版本；推荐的方法是使用键盘快捷键（++slash++）并输入查询词。