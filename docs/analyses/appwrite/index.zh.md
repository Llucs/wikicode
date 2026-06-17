---
title: Appwrite：自托管后端即服务平台
description: 开源BaaS，提供认证、数据库、存储、无服务器函数和消息传递的API——您可掌控的Firebase替代品。
created: 2026-06-15
tags:
  - analysis
  - backend-as-a-service
  - self-hosted
  - firebase-alternative
  - serverless
  - platform-study
status: draft
---

# Appwrite：自托管后端即服务平台

Appwrite 是一个**开源后端即服务（BaaS）**平台，为您提供一套完整的服务器API和工具，以便快速构建 Web、移动和 AI 应用。由 Eldad Fux 于2019年创建，现拥有庞大社区（40k+ GitHub 星标），设计为 Firebase 的自托管替代品，优先考虑数据所有权、隐私和灵活部署。

无需拼接各个微服务，Appwrite 提供统一的 API 用于认证、数据库、存储、无服务器函数、消息传递和实时事件——全部运行在您自己的基础设施上。

---

## 为什么选择 Appwrite？

- **数据所有权** – 您掌控数据的存储位置和方式，这对于 GDPR、HIPAA 或内部合规至关重要。
- **无供应商锁定** – 自托管或使用云服务；您的代码保持可移植。
- **丰富的服务集** – 认证（OAuth2、MFA、JWT、魔法链接）、NoSQL 数据库、文件存储、无服务器函数、推送/电子邮件/短信消息、实时订阅等——全部整合在一个平台中。
- **简单统一的 API** – 跨 Web（JavaScript/TypeScript）、Flutter、Android、iOS 和服务端代码的统一 SDK 模式。
- **活跃的开源生态系统** – 由蓬勃发展的社区支持，提供官方 SDK、CLI 以及不断增长的集成库（Stripe、Twilio、SendGrid、GPT-4o 通过函数）。
- **从快速原型到生产环境** – 使用管理控制台进行无代码设置，然后通过 SDK 实现完全控制。

---

## 关键特性及命令示例

### 认证
支持电子邮件/密码、电话（短信）、OAuth2（Google、GitHub、Discord 等）、魔法链接、JWT、匿名会话和多因素认证（MFA）。

```javascript
import { Client, Account, ID } from 'appwrite';

// 初始化客户端
const client = new Client()
    .setEndpoint('https://<HOST>/v1')
    .setProject('<PROJECT_ID>');

const account = new Account(client);

// 注册用户
await account.create(ID.unique(), 'user@example.com', 'password123', 'Jane Doe');

// 登录
await account.createEmailPasswordSession('user@example.com', 'password123');

// 获取当前用户
const user = await account.get();
```

### 数据库（NoSQL）
基于文档的存储，支持高级查询、全文搜索、实时监听和关联。

```javascript
import { Databases, ID } from 'appwrite';

const databases = new Databases(client);

// 创建文档
await databases.createDocument(
    '<DATABASE_ID>',
    '<COLLECTION_ID>',
    ID.unique(),
    { title: '我的文章', body: '你好，世界！', tags: ['appwrite'] }
);

// 列出文档
const results = await databases.listDocuments(
    '<DATABASE_ID>',
    '<COLLECTION_ID>',
    [Query.equal('tags', ['appwrite'])]
);
```

### 存储
文件上传，内置图片预览、调整大小、裁剪和恶意软件扫描。

```javascript
import { Storage, ID } from 'appwrite';

const storage = new Storage(client);

// 上传文件
const uploaded = await storage.createFile(
    '<BUCKET_ID>',
    ID.unique(),
    myFile
);
```

### 无服务器函数
运行代码以响应事件（数据库、存储、认证、计划任务）。支持的运行时：Node.js、Python、Ruby、PHP、Dart、Deno、Kotlin、Swift、.NET。

```bash
# 通过 CLI 创建函数
appwrite functions create \
  --name='sendWelcomeEmail' \
  --runtime='node-18.0' \
  --execute='any' \
  --entrypoint='index.js'

# 部署代码
appwrite functions deploy \
  --functionId='<FUNCTION_ID>' \
  --path='./my-function'
```

```javascript
// 索引函数代码（Node.js）
export default async ({ req, res, log, error }) => {
    log('函数被触发');
    return res.json({ message: '来自 Appwrite Functions 的问候！' });
};
```

### 消息传递
推送通知（FCM/APNS）、电子邮件（SMTP、SendGrid、Mailgun）和短信（Twilio、Vonage、TextMagic）。通过管理控制台或 API 管理。

```javascript
import { Messaging } from 'appwrite';

const messaging = new Messaging(client);
await messaging.createEmail(
    '<MESSAGE_ID>',
    '<SUBJECT>',
    '<CONTENT>',
    [userEmail]
);
```

### 实时功能
订阅数据库、存储和函数事件（基于 WebSocket）。

```javascript
import { Client } from 'appwrite';

const client = new Client()
    .setEndpoint('https://<HOST>/v1')
    .setProject('<PROJECT_ID>');

client.subscribe('databases.<DB_ID>.collections.<COLL_ID>.documents', response => {
    console.log('文档已更改：', response.payload);
});
```

### GraphQL API
Appwrite 暴露了完整的 GraphQL 端点——适合与 GraphQL 良好配合的前端框架。

```graphql
query {
  usersList(limit: 10) {
    users {
      name
      email
      $id
    }
  }
}
```

### 管理控制台
一个完整的 Web 界面，用于管理所有服务——无需编码即可创建数据库、集合、用户、存储桶或触发器。

---

## 架构

Appwrite 使用**微服务架构**，通过 Docker 编排。每个服务作为独立容器运行：

- **MariaDB** – 元数据存储（项目、用户等）
- **Redis** – 缓存和任务队列
- **InfluxDB** – 使用指标和分析
- **Kafka** – 消息和事件流
- **Workers** – 后台任务（电子邮件、函数、Webhook、迁移）

专用工作器处理异步任务，使主 API 保持响应。整个堆栈通过单个安装命令启动。

---

## 安装

### 自托管（Docker）

在您自己的服务器上运行 Appwrite 的最简单方法：

```bash
docker run -it --rm \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    --volume "$(pwd)"/appwrite:/storage/config:rw \
    --entrypoint="install" \
    appwrite/appwrite:latest
```

这将启动一个交互式安装程序，它会拉取并配置所有必要的容器。默认情况下，Appwrite 运行在 `http://0.0.0.0`。

### 云服务（托管）

在 [cloud.appwrite.io](https://cloud.appwrite.io) 注册——提供具有使用限制的免费套餐，非常适合原型开发。

### 控制台设置

安装后（自托管或云），在控制台中创建一个项目，记下项目 ID 和端点，并生成 API 密钥。

---

## 基本用法（JavaScript SDK）

1. **初始化客户端并认证**

   ```javascript
   import { Client, Account, ID } from 'appwrite';

   const client = new Client()
       .setEndpoint('https://<HOST>/v1')
       .setProject('<PROJECT_ID>');

   const account = new Account(client);

   // 注册 & 登录
   await account.create(ID.unique(), 'user@test.com', 'password123', 'Jane Doe');
   await account.createEmailPasswordSession('user@test.com', 'password123');
   ```

2. **创建和查询文档**

   ```javascript
   import { Databases, Query } from 'appwrite';

   const databases = new Databases(client);

   // 创建
   await databases.createDocument(
       '<DATABASE_ID>',
       '<COLLECTION_ID>',
       ID.unique(),
       { name: '任务', status: '待办' }
   );

   // 查询
   const tasks = await databases.listDocuments(
       '<DATABASE_ID>',
       '<COLLECTION_ID>',
       [Query.equal('status', '待办'), Query.limit(25)]
   );
   ```

3. **通过 CLI 部署函数**

   ```bash
   appwrite functions create --name='processOrder' --runtime='node-18.0' --execute='any'
   appwrite functions deploy --functionId='<ID>' --path='./functions/process-order'
   ```

4. **监听实时事件**

   ```javascript
   client.subscribe('databases.*.collections.*.documents', event => {
       console.log(`${event.events[0]} –`, event.payload);
   });
   ```

---

## 使用场景

- **构建 MVP 和快速原型** – 跳过后端设置；专注于前端逻辑。
- **全栈 Web 应用** – React、Vue、Next.js、Svelte、Nuxt、Angular。
- **跨平台移动应用** – Flutter、Android、iOS（SwiftUI）、React Native。
- **AI 驱动的功能** – 通过无服务器函数集成 GPT-4o 或其他大型语言模型。
- **内部工具** – 使用管理控制台和实时更新构建管理仪表板。
- **符合 GDPR/HIPAA 的应用** – 在您自己的数据中心自托管。

---

## 与类似工具的对比

| 功能          | Appwrite                        | Supabase                          | PocketBase                        |
|---------------|----------------------------------|-----------------------------------|-----------------------------------|
| 数据库模型    | NoSQL（文档）                   | SQL（PostgreSQL）                  | SQLite                            |
| 自托管        | 是（Docker）                     | 是（Docker）                       | 是（单个二进制文件）               |
| 无服务器函数  | 是（Node、Python、Ruby 等）      | 是（PostgreSQL 函数 + 边缘函数）   | 是（JavaScript/Go）               |
| 实时功能      | WebSocket（数据库、存储、事件）  | PostgreSQL 复制                    | WebSocket（数据库）                |
| 认证          | OAuth2、MFA、魔法链接、短信       | OAuth2、MFA、SSO                  | OAuth2、MFA                       |
| 消息传递      | 推送、电子邮件、短信              | 电子邮件（通过 pgmq）               | –                                 |
| 存储          | 图片预览、调整大小、扫描          | 是（兼容 S3）                      | 是                                |
| 管理界面      | 功能完备的 Web 控制台            | Web 控制台                        | 极简 Web UI                      |
| 客户端 SDK    | Web、Flutter、Android、iOS、CLI   | Web、Flutter、Swift、Kotlin 等     | Web、Dart、Android、iOS、Go       |

**选择 Appwrite** 如果您需要一个统一的、有主见的 NoSQL 平台，内置消息传递、GraphQL 和丰富的管理控制台——并且希望将数据保留在您自己的 Docker 堆栈上。

---

## 社区与生态系统

- **GitHub** – [github.com/appwrite/appwrite](https://github.com/appwrite/appwrite)
- **Discord** – 活跃的开发者社区
- **模板与开源项目** – 参见 [builtwith.appwrite.network](https://builtwith.appwrite.network)
- **集成** – Appwrite MCP 用于 AI、传感器、欺诈检测等
- **黑客松** – 经常出现在 Hacktoberfest、Dev.to 挑战赛中

---

## 结论

Appwrite 是一个成熟的开源 BaaS，为您提供 Firebase 的强大功能而无锁定问题。其自托管能力、丰富的功能集和活跃的社区使其成为从黑客松到受监管企业环境等各类场景的绝佳选择。无论您使用云版本还是自行运行，Appwrite 都能抽象后端复杂性，让您专注于构建应用。

**今天就开始：**

```bash
docker run -it --rm --volume /var/run/docker.sock:/var/run/docker.sock --volume $(pwd)/appwrite:/storage/config:rw --entrypoint="install" appwrite/appwrite:latest
```
或直接注册 [cloud.appwrite.io](https://cloud.appwrite.io)。