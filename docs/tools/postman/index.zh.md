---
title: Postman - API开发和测试平台
description: 一份全面的Postman指南，Postman是用于设计、构建、测试和记录API的行业标准API平台。
created: 2026-06-15
tags:
  - postman
  - api-testing
  - api-development
  - collaboration
  - newman
status: draft
ecosystem: api
---

# Postman - API开发和测试平台

## 什么是Postman？

Postman是一个完整的API平台，简化了API生命周期的每个步骤——从设计和开发到测试、文档记录和监控。最初只是一个简单的HTTP客户端，它已发展成为全球数百万开发者和质量保证工程师使用的协作环境。Postman支持REST、GraphQL和SOAP协议，并提供丰富的工具集，用于高效地构建和使用API。

## 为什么使用Postman？

- **全面的HTTP客户端：** 轻松发送任何方法的请求，自定义请求头、认证和请求体。
- **组织工具：** 将请求分组到集合（Collections），使用环境（Environments）管理变量，并在整个工作区中复用数据。
- **脚本编写与测试：** 编写JavaScript测试脚本以自动化断言，在请求之间提取数据，并处理动态工作流。
- **自动化就绪：** 使用Collection Runner进行手动运行，或使用Newman进行无头执行（CI/CD、流水线）。
- **协作：** 通过带有版本控制和评论功能的云工作区共享集合和环境。
- **文档与模拟：** 自动生成API文档和Mock Servers，在后端准备好之前模拟API响应。
- **监控：** 设置监控器以定期运行集合并验证API健康状态。

## 安装

### 桌面应用（推荐）

Postman提供Windows、macOS和Linux的原生桌面应用。

- 从 [getpostman.com](https://getpostman.com) 下载相应的安装程序
- 或者，使用 [go.postman.co](https://go.postman.co) 的 **Web版本** 并结合Desktop Agent来处理API调用。

### Newman（用于CI/CD的命令行工具）

Newman是Postman的命令行集合运行器。它使您能够直接从命令行运行和测试Postman集合，非常适合将API测试集成到开发流水线中。

通过npm安装：

```bash
npm install -g newman
```

或通过Yarn：

```bash
yarn global add newman
```

## 基本用法

1. **创建请求**  
   点击 **New** 按钮并选择 **HTTP Request**（或使用 `Ctrl+N`）。

2. **指定请求**  
   - 输入URL（例如 `https://jsonplaceholder.typicode.com/posts`）  
   - 选择HTTP方法（`GET`、`POST`、`PUT`等）  
   - 添加所需的请求头、查询参数或请求体。

3. **发送和检查**  
   点击 **Send**。响应面板显示状态码、响应时间、响应头和响应体。

4. **保存到集合**  
   点击 **Save**，然后创建新集合或添加到现有集合。

5. **添加测试**  
   在 **Tests** 标签页下，编写JavaScript脚本来验证响应。示例：

   ```javascript
   pm.test("Response status code is 200", function () {
       pm.response.to.have.status(200);
   });
   ```

   重新发送请求——测试结果会出现在 **Test Results** 标签页中。

## 关键功能示例

### 1. 集合（Collections）

集合帮助您将相关请求分组并与团队共享。集合还可以包含文件夹和元数据。

```javascript
// Example of using collection variables in a pre-request script
pm.collectionVariables.set("baseUrl", "https://api.example.com");
```

使用Newman运行整个集合：

```bash
newman run MyCollection.json
```

### 2. 环境（Environments）

环境包含在不同设置（开发、预发、生产）之间变化的变量的键值对。

```json
{
  "base_url": "https://dev-api.example.com",
  "api_key": "abc123"
}
```

在请求URL中使用 `{{base_url}}`。在环境之间切换即可立即更改上下文。

### 3. 预请求和测试脚本（Pre-request and Test Scripts）

Postman脚本用JavaScript编写，在沙箱中运行，可以访问Postman提供的对象，如`pm`。

**预请求脚本**（在请求发送前执行）：

```javascript
// Dynamically set a timestamp parameter
pm.variables.set("timestamp", Date.now());
```

**测试脚本**（在收到响应后执行）：

```javascript
pm.test("Response time is less than 2000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("Body contains expected user", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData[0].name).to.eql("Leanne Graham");
});
```

### 4. 集合运行器（Collection Runner）

使用数据文件多次运行整个集合或文件夹。

- 从Postman左上方打开 **Runner**。
- 选择一个集合，选择一个环境，设置迭代次数。
- 您可以提供CSV或JSON数据文件，将数据注入到每次迭代中。

### 5. Newman – 命令行集成

Newman使您能够将Postman测试集成到CI/CD流水线（Jenkins、GitLab CI、GitHub Actions等）中。

**使用环境和数据文件运行集合：**

```bash
newman run MyCollection.json \
  --environment staging.json \
  --iteration-data test-data.csv \
  --reporters cli,htmlextra
```

`htmlextra` 报告器会生成测试运行的交互式HTML报告。

**在Node.js脚本中使用：**

```javascript
const newman = require('newman');

newman.run({
    collection: require('./MyCollection.json'),
    environment: require('./staging.json'),
    reporters: 'cli'
}, function (err, summary) {
    if (err) { throw err; }
    console.log('Collection run completed!');
    console.log(summary.run.stats);
});
```

### 6. 文档生成

Postman可以自动为任何集合生成文档。只需打开一个集合，点击 **...** 菜单，然后选择 **View documentation**。文档包括示例请求、请求/响应模式以及多种语言的代码片段。

通过 **Publish Docs** 按钮将文档发布到Web，或将其导出为HTML。

### 7. 模拟服务器（Mock Servers）

通过从集合创建模拟服务器来模拟API。当后端尚未就绪时，这对前端开发非常有用。

- 选择一个集合，点击 **Mock Servers**。
- Postman会创建一个返回已保存示例响应的模拟服务器URL。

### 8. 监控器（Monitors）

监控器允许您在Postman的云基础设施上定期运行集合。如果任何测试失败，您会收到警报。

- 转到 **Monitors** → **Create a monitor**。
- 选择一个集合，设置频率（例如每小时），并可选择定义警报（电子邮件、Slack等）。

## 总结

Postman不仅仅是一个API客户端——它是一个支持整个API生命周期的成熟平台。从最初的模拟和协作设计，到通过Newman进行自动化测试以及生产监控，Postman为团队提供了API的唯一可信源。它的易用性，结合强大的脚本能力和CI/CD集成，使其成为现代开发工作流中不可或缺的工具。