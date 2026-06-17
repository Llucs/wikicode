---
title: npm - Node.js 包管理器
description: 一个用于 Node.js 的包管理器，是管理 JavaScript 依赖的基础工具。
created: 2026-06-14
tags:
  - package-manager
  - javascript
  - nodejs
  - cli
  - dependency-management
status: draft
ecosystem: javascript
---

# npm – Node Package Manager

npm（Node Package Manager）是 Node.js JavaScript 运行环境的默认包管理器。它由两个主要部分组成：用于管理依赖的**CLI**（命令行界面）以及一个巨大的 JavaScript 包公共数据库——**npm Registry**。它已成为 JavaScript 生态系统中必不可少的工具，使开发者能够高效地共享、重用和管理代码。

## 什么是 npm？

npm 提供了一种方式来：

- **安装和管理依赖** – 在 `package.json` 和锁文件中跟踪包。
- **发布包** – 与社区或组织分享自己的库。
- **运行脚本** – 自动化构建、测试和部署工作流。
- **管理单体仓库** – 使用工作区在单个仓库中处理多个包。

## 为什么使用 npm？

- **标准化** – npm 随 Node.js 一起提供，使其成为大多数 JavaScript 项目的默认选择。
- **庞大的生态系统** – 注册表中拥有超过 200 万个包，几乎涵盖所有需求。
- **可重现性** – `package-lock.json` 文件确保跨环境的确定性安装。
- **安全性** – `npm audit` 帮助您发现并修复依赖树中的漏洞。
- **便利性** – `npx` 允许您在不全局安装的情况下运行包，脚本则简化了常见任务。

## 安装

npm 随 Node.js 自动安装。要获取最新的 LTS 版本：

1. 从 [nodejs.org](https://nodejs.org/) 下载 Node.js。
2. 验证安装：

```bash
node -v
npm -v
```

### 通过版本管理器安装（nvm/fnm）

使用版本管理器可以切换 Node.js 版本并为每个版本安装 npm：

```bash
# 以 nvm 为例
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install --lts
```

安装完成后，npm 即可使用。

## 基本用法

### 初始化项目

创建一个新项目或转换现有文件夹：

```bash
npm init -y
```

这会生成一个带有默认值的 `package.json` 文件。使用 `npm init`（不加 `-y`）进行交互式提示。

### 安装依赖

```bash
# Production dependency
npm install lodash

# Dev-only dependency
npm install --save-dev jest

# Global package (use sparingly; prefer npx)
npm install -g nodemon

# Install all dependencies from package.json
npm install
```

### 安装特定版本

```bash
npm install react@18.2.0
npm install "express@>=4.17.0 <5.0.0"
```

### 运行脚本

脚本定义在 `package.json` 的 `"scripts"` 键下。常用快捷方式：

```bash
npm start        # runs the "start" script
npm test         # runs the "test" script
npm run build    # custom script, e.g., "build"
```

### 卸载包

```bash
npm uninstall lodash
```

### 更新包

```bash
npm update                # update all packages within version ranges
npm install lodash@latest # force a specific version update
```

### 检查漏洞

```bash
npm audit
```

自动修复（如果可用）：

```bash
npm audit fix
```

### 用于 CI 的清洁安装

```bash
npm ci
```

`npm ci` 速度更快，在从 `package-lock.json` 确切安装前会删除 `node_modules`。

## 主要特性

### npx – 无需安装即可运行包

`npx` 随 npm 一起提供，允许您从注册表执行二进制文件而无需全局安装：

```bash
npx create-react-app my-app
npx cowsay "Hello, npm!"
```

如果包已在本地安装，`npx` 将使用该版本。

### 工作区（单体仓库支持）

npm 工作区允许您在单个仓库中管理多个包：

```json
{
  "workspaces": [
    "packages/*"
  ]
}
```

然后跨所有工作区运行命令：

```bash
npm install              # installs dependencies for all workspaces
npm run test --workspaces
```

工作区包之间的链接会自动处理。

### 脚本生命周期钩子

npm 为常用脚本提供前置/后置钩子：

- `prepublish` / `postpublish`
- `preinstall` / `postinstall`
- `prebuild` / `postbuild`

示例：

```json
{
  "scripts": {
    "prebuild": "rimraf dist",
    "build": "webpack --config webpack.prod.js"
  }
}
```

### package-lock.json

此文件锁定每个依赖及其传递依赖的确切版本。它确保每个人运行 `npm install` 时都能得到相同的依赖树，从而使构建具有可重现性。

### 覆盖和解析

您可以在 `package.json` 中强制指定传递依赖的特定版本：

```json
{
  "overrides": {
    "graceful-fs": "4.2.11"
  }
}
```

当子依赖存在漏洞需要修补，而不必等待其父版本发布时，这非常有用。

### npm 配置

全局或按项目自定义 npm 行为：

```bash
npm config set init-author-name "Your Name"
npm config get registry
npm config delete <key>
```

您也可以在项目根目录使用 `.npmrc` 文件。

### 全局包与 npx

全局安装应保留用于跨多个项目使用的工具（例如 `npm`、`yarn`、`node-gyp`）。对于一次性命令，优先使用 `npx`，以避免污染全局命名空间并确保始终使用预期版本。

## 结论

对于任何 JavaScript 开发者来说，npm 都是一个强大且必不可少的工具。从简单的依赖安装到复杂的单体仓库管理，其丰富的功能集有助于保持项目的组织性、安全性和可重现性。无论您是构建一个小型库还是大型应用程序，掌握 npm 都将显著改善您的工作流程。