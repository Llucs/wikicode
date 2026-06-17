---
title: 入门
description: 仓库布局、本地构建和贡献规范。
created: 2026-06-03
---

# 入门

您阅读、构建和贡献 WikiCode 所需的一切。

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">创建日期：2026-06-03</span>
<span class="wikicode-meta-updated">最后更新：自动（git）</span>
</div>

## 1. 仓库布局

```
.
├── README.md            # 项目概览
├── LICENSE              # MIT 许可证
├── AGENT.md             # 代理的操作契约
├── mkdocs.yml           # 静态站点配置
├── .gitignore
├── .github/
│   └── workflows/
│       ├── pages.yml    # 推送至 main 分支时构建并部署站点
│       └── wikicode-agent.yml# 自主代理工作流
├── docs/                # 站点内容（文章、指南）
│   ├── assets/css/      # 自定义样式
│   ├── index.md
│   └── getting-started.md
├── projects/            # 独立的开发者项目
├── snippets/            # 可复用的代码片段
├── memory/              # 代理长期记忆
│   ├── mission.md
│   ├── rules.md
│   ├── knowledge.md
│   └── decisions.md
├── tasks/               # 工作流水线
│   ├── queue.md
│   └── completed.md
└── reports/             # 带时间戳的执行报告
```

## 2. “wiki 从仓库生长”循环

WikiCode 是一个**仓库优先**的站点。`site/`（发布输出）中的任何内容都不会手动编辑。

1. 对仓库进行更改（新文章、项目、片段、报告、决策等）。
2. 提交更改并推送到 `main` 分支。
3. `.github/workflows/pages.yml` 在推送时自动运行。
4. MkDocs 读取 `docs/`、`projects/`、`snippets/` 并重建整个站点。
5. GitHub Pages 提供新构建的内容。

本地 AI 代理（或任何贡献者）通过向仓库写入内容来接入此循环。站点随后会自动获取更改，无需人工干预。

## 3. 本地运行站点

你需要 Python 3.10+。

```bash
pip install mkdocs mkdocs-material \
            mkdocs-awesome-pages-plugin \
            mkdocs-git-revision-date-localized-plugin
mkdocs serve
```

站点将在 `http://127.0.0.1:8000` 可用。对 `docs/`、`projects/` 或 `snippets/` 下任何 Markdown 文件的编辑都会触发即时重载。

## 4. 构建静态站点

```bash
mkdocs build --clean
```

输出写入 `site/`。CI 使用相同的命令。

## 5. 添加内容

| 你想添加… | 放在…                              | 需要的文件                      |
| ---------------- | ---------------------------------------- | ----------------------------------- |
| 一篇文章       | `docs/<topic>/<slug>.md` 或 `docs/`      | `.md` 文件本身               |
| 一个项目        | `projects/<slug>/`                       | `README.md` + `index.md` + 源码   |
| 一个片段        | `snippets/<slug>/`                       | 代码文件 + `index.md`          |
| 一个决策       | `memory/decisions.md`                    | 追加一个新条目                  |
| 一个任务           | `tasks/queue.md`                         | 追加一个新复选框条目         |
| 一份报告         | `reports/YYYY-MM-DD-<slug>.md`           | 文件 + 索引更新             |

不属于 `docs/` 的章节（projects、snippets）通过其 `index.md` 文件被 `awesome-pages` MkDocs 插件自动拾取。

## 6. 元数据头

站点上的每个页面至少包含：

```yaml
---
title: 页面标题
description: 简短描述。
created: YYYY-MM-DD
---
```

`created` 日期在页面首次添加时设置。**最后更新**日期自动从文件的 git 历史获取，因此无需手动编辑即可保持准确。

## 7. 自主工作

代理必须遵循 `AGENT.md`。简要版本：

1. 读取 `memory/mission.md` 和 `memory/rules.md`。
2. 从 `tasks/queue.md` 选取下一个任务。
3. 对仓库进行一次有意义的更改。
4. 在 `reports/` 中编写报告。
5. 将任务移至 `tasks/completed.md`。
6. 提交并推送。站点将自动重建。

## 8. 搜索

WikiCode 完全可搜索。搜索索引在部署时构建，完全在浏览器中运行。

- 在任何页面上按 ++slash++ 键聚焦搜索栏。
- 索引覆盖站点上的每个页面，包括代码块和博客文章。
- 查看 [搜索](search.md) 了解更多详情和提示。

## 9. 代理如何被触发

wikicode-agent 工作流支持**自动和手动**两种触发方式：

| 触发方式              | 时机                                                  | 使用场景                                  |
| -------------------- | ----------------------------------------------------- | ----------------------------------------- |
| `schedule`           | 每天 UTC 时间 12:00。                                   | 默认的“每天成长一点”运行。    |
| `workflow_dispatch`  | 从 Actions 标签页手动触发。                        | 按需运行，适用于解除阻塞。     |
| `issue_comment`      | 当有人在 issue 中写入 `@agent` 时。             | 将 issue 转化为贡献。        |
| `issues` 带标签      | 当 issue 被标记为 `agent` 时。                     | 操作员策划的批量运行。              |

每次运行只执行**一个**任务。AI 使用 OpenCode API 进行内容生成——无需外部 API 密钥。

## 10. 规范

- Markdown 文件名：小写，用连字符连接。
- 每个项目、片段和工具文件夹都公开一个 `index.md` 用于导航。
- 关于架构、工具或工作流的决策记录在 `memory/decisions.md` 中。
- 绝不提交任何凭证、令牌或私有数据。
- 本地 AI 代理使用内置的 `secrets.GITHUB_TOKEN` 进行提交和推送。无需外部 API 密钥。