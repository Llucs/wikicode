---
title: npm - Node Package Manager
description: A package manager for Node.js that is a fundamental tool for managing JavaScript dependencies.
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

npm (Node Package Manager) is the default package manager for the Node.js JavaScript runtime. It consists of two main components: a **CLI** (command-line interface) for managing dependencies and the **npm Registry**, a massive public database of JavaScript packages. It has become an essential tool in the JavaScript ecosystem, enabling developers to share, reuse, and manage code efficiently.

## What is npm?

npm provides a way to:

- **Install and manage dependencies** – track packages in `package.json` and lock files.
- **Publish packages** – share your own libraries with the community or your organization.
- **Run scripts** – automate build, test, and deployment workflows.
- **Manage monorepos** – using workspaces to handle multiple packages in a single repository.

## Why use npm?

- **Standardization** – npm is bundled with Node.js, making it the default choice for most JavaScript projects.
- **Huge ecosystem** – over 2 million packages in the registry, covering virtually every need.
- **Reproducibility** – the `package-lock.json` file ensures deterministic installs across environments.
- **Security** – `npm audit` helps you find and fix vulnerabilities in your dependency tree.
- **Convenience** – `npx` lets you run packages without global installation, and scripts simplify common tasks.

## Installation

npm is installed automatically with Node.js. To get the latest LTS version:

1. Download Node.js from [nodejs.org](https://nodejs.org/).
2. Verify the installation:

```bash
node -v
npm -v
```

### Install via version manager (nvm/fnm)

Using a version manager allows you to switch between Node.js versions and install npm for each:

```bash
# Example with nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install --lts
```

After installation, npm is ready to use.

## Basic Usage

### Initialize a project

Create a new project or convert an existing folder:

```bash
npm init -y
```

This generates a `package.json` file with default values. Use `npm init` (without `-y`) for an interactive prompt.

### Install dependencies

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

### Install specific versions

```bash
npm install react@18.2.0
npm install "express@>=4.17.0 <5.0.0"
```

### Run scripts

Scripts are defined under the `"scripts"` key in `package.json`. Common shortcuts:

```bash
npm start        # runs the "start" script
npm test         # runs the "test" script
npm run build    # custom script, e.g., "build"
```

### Uninstall packages

```bash
npm uninstall lodash
```

### Update packages

```bash
npm update                # update all packages within version ranges
npm install lodash@latest # force a specific version update
```

### Check for vulnerabilities

```bash
npm audit
```

To automatically fix (where available):

```bash
npm audit fix
```

### Clean install for CI

```bash
npm ci
```

`npm ci` is faster and removes `node_modules` before installing exactly from `package-lock.json`.

## Key Features

### npx – Run packages without installing

`npx` comes with npm and lets you execute binaries from the registry without global installs:

```bash
npx create-react-app my-app
npx cowsay "Hello, npm!"
```

If the package is already installed locally, `npx` will use that version.

### Workspaces (monorepo support)

npm workspaces allow you to manage multiple packages in a single repository:

```json
{
  "workspaces": [
    "packages/*"
  ]
}
```

Then run commands across all workspaces:

```bash
npm install              # installs dependencies for all workspaces
npm run test --workspaces
```

Linking between workspace packages is handled automatically.

### Scripts lifecycle hooks

npm provides pre/post hooks for common scripts:

- `prepublish` / `postpublish`
- `preinstall` / `postinstall`
- `prebuild` / `postbuild`

Example:

```json
{
  "scripts": {
    "prebuild": "rimraf dist",
    "build": "webpack --config webpack.prod.js"
  }
}
```

### package-lock.json

This file locks the exact version of every dependency and its transitive dependencies. It ensures that everyone running `npm install` gets the same tree, making builds reproducible.

### Overrides and resolutions

You can force specific versions of transitive dependencies in `package.json`:

```json
{
  "overrides": {
    "graceful-fs": "4.2.11"
  }
}
```

This is useful when a sub‑dependency has a vulnerability that you need to patch without waiting for its parent release.

### npm config

Customize npm behavior globally or per project:

```bash
npm config set init-author-name "Your Name"
npm config get registry
npm config delete <key>
```

You can also use an `.npmrc` file in the project root.

### Global packages vs. npx

Global installs should be reserved for tools you use across many projects (e.g., `npm`, `yarn`, `node-gyp`). For one‑off commands, prefer `npx` to avoid polluting the global namespace and to ensure you always use the intended version.

## Conclusion

npm is a powerful and essential tool for any JavaScript developer. From simple dependency installation to complex monorepo management, its rich feature set helps keep projects organized, secure, and reproducible. Whether you are building a small library or a large application, mastering npm will significantly improve your workflow.