---
title: WikiCode 导航审计
description: 对 WikiCode 站点导航的分析及改进建议。
created: 2026-06-14
tags:
  - meta
  - guide
status: draft
---

# 导航审计

## 当前结构

主导航在 `mkdocs.yml` 中定义，当前包括：

- Home
- Search
- Getting started
- Learning paths
- Guides
- Reference (Glossary, Architecture, Changelog)
- Topics
- Tools
- Tags
- Blog
- Projects
- Snippets
- Reports

## 拟议改进

1. **将元部分分组** 到单个 "About" 或 "WikiCode" 菜单项下（Reports, Changelog, Architecture）
2. **将 Tags 移至 Topics 内部**，因为它们是相关概念
3. **添加视觉指示器** 以标识最近更新的内容
4. **确保面包屑导航** 在所有导航层级上可用

## 实施

所有更改都应应用于 `mkdocs.yml` 中的 `nav:` 块。