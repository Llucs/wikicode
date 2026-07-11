---
title: Web 开发中的索引路由
description: 本全面指南介绍了索引路由，包括其主要特性、历史、用例、安装和基本用法。
created: 2026-07-11
tags:
  - web 开发
  - 路由
  - Ruby on Rails
status: 草稿
---

# Web 开发中的索引路由

## 什么是索引路由？

索引路由是一种在 web 框架中处理资源列表或索引的方法。当用户访问类似 `/users` 的 URL 时，框架会自动将请求路由到 `UsersController` 的 `index` 方法。该方法负责检索并显示所有用户的列表。

## 主要特性

1. **简化路由**：索引路由减少了 web 应用中所需的路由数量。通过在单个路由下处理所有列表相关操作（例如 `GET /users`、`POST /users`、`GET /users/:id`），索引路由可以简化路由定义。
2. **一致性**：它提供了一种在应用程序的不同部分处理资源列表的一致方式。
3. **灵活性**：`index` 方法可以根据需要包含不同的查询参数、排序和过滤选项进行自定义。

## 历史

索引路由起源于 web 开发框架，如 Ruby on Rails，该框架最初引入了简化资源列表处理的方法。该概念此后被其他 web 框架和编程语言采用。

## 用例

1. **列出资源**：显示用户、文章或产品的列表。
2. **分页**：处理资源列表中的分页。
3. **筛选和排序**：为列表实现筛选和排序选项。
4. **CRUD 操作**：管理创建、读取、更新和删除操作的索引动作。

## 安装

索引路由通常构建在 web 开发框架中。例如，在 Ruby on Rails 中，它是路由系统的一部分。以下是如何在 Rails 应用程序中设置它的步骤：

1. **创建控制器**：
   ```sh
   rails generate controller Users
   ```

2. **定义索引动作**：
   ```ruby
   # app/controllers/users_controller.rb
   class UsersController < ApplicationController
     def index
       @users = User.all
     end
   end
   ```

3. **配置路由**：
   ```ruby
   # config/routes.rb
   resources :users, only: [:index]
   ```

## 基本用法

1. **路由**：
   - 路由 `resources :users, only: [:index]` 为索引动作设置了一个路由。
   - 当用户访问 `/users` 时，`UsersController` 的 `index` 方法会被调用。

2. **控制器逻辑**：
   - `index` 方法在控制器中使用 `User.all` 获取用户列表。
   - 控制器还可以包含用于筛选、排序和分页的额外逻辑。

3. **视图**：
   - 与 `index` 动作关联的视图可以显示用户列表。
   - 以下是一个使用 ERB（Ruby on Rails 模板引擎）的示例视图：
     ```erb
     <!-- app/views/users/index.html.erb -->
     <h1>Users</h1>
     <ul>
       <% @users.each do |user| %>
         <li><%= user.name %></li>
       <% end %>
     </ul>
     ```

## 示例

以下是在 Rails 应用程序中索引路由的完整示例：

1. **生成控制器**：
   ```sh
   rails generate controller Users
   ```

2. **更新控制器**：
   ```ruby
   # app/controllers/users_controller.rb
   class UsersController < ApplicationController
     def index
       @users = User.all
     end
   end
   ```

3. **配置路由**：
   ```ruby
   # config/routes.rb
   resources :users, only: [:index]
   ```

4. **创建视图**：
   ```erb
   <!-- app/views/users/index.html.erb -->
   <h1>Users</h1>
   <ul>
     <% @users.each do |user| %>
       <li><%= user.name %></li>
     <% end %>
   </ul>
   ```

5. **启动服务器**：
   ```sh
   rails server
   ```

6. **访问页面**：
   在浏览器中访问 `http://localhost:3000/users` 查看用户列表。

## 总结

索引路由是 web 开发框架中的一个强大功能，它简化了资源列表的处理。通过定义一个路由来处理 `index` 动作，开发人员可以以一致且高效的方式管理列表、分页和筛选。此模式在 Ruby on Rails 等框架中得到了充分支持，使其易于实现和维护。