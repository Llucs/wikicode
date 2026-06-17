---
title: SonarQube
description: 一款可与 CI/CD 流水线集成、自动化代码审查并捕获漏洞的代码质量与安全分析工具。
created: 2026-06-16
tags:
  - code-quality
  - security
  - static-analysis
  - ci-cd
  - sonarqube
status: draft
---

# SonarQube

## 什么是 SonarQube？

SonarQube 是 SonarSource 出品的一个开源平台，用于持续检测代码质量和安全性。它对源代码执行静态应用安全测试（SAST），以检测 30 多种编程语言中的**缺陷**、**漏洞**、**代码异味**和**重复**，包括 Java、C#、JavaScript、TypeScript、Python、Go 等。SonarQube 在开发工作流中充当中央质量枢纽，强制执行可定制的策略（质量门），防止有问题的代码被发布。

## 为什么要使用 SonarQube？

- **尽早发现问题** – 集成到 CI/CD 流水线中，自动审查每一次提交和拉取请求。
- **强制质量标准** – 定义必须通过的质量门（例如没有新增缺陷、覆盖率阈值），否则构建失败。
- **减少技术债务** – 量化修复现有问题所需的工作量，并跟踪随时间改进的情况。
- **提升安全性** – 识别 OWASP Top 10 和 CWE 漏洞，标记安全热点供人工审查。
- **自动化代码审查** – 将简单问题（格式、空指针、资源泄漏）的检测从人工评审中剥离，让审查者专注于架构和逻辑。

## 主要特性

### 静态代码分析
SonarQube 扫描源代码，寻找可靠性、安全性和可维护性问题。它执行高级数据流和控制流分析，检测：
- 潜在的空指针解引用
- 资源泄漏
- SQL 注入和跨站脚本（XSS）缺陷
- 硬编码凭据

### 质量门（Quality Gates）
质量门是针对度量指标（例如 `新代码覆盖率 < 80%`、`新增缺陷 > 0`）设置的一组布尔条件，项目必须满足这些条件才能通过。SonarQube 自带一个默认质量门，你也可以创建自定义质量门来匹配团队策略。

### 安全热点（Security Hotspots）
SonarQube 高亮需要人工安全审查的代码。这些热点不会自动确认为漏洞，而是潜在的攻击者可注入恶意输入的领域。开发人员可以审查并将它们标记为“安全”或“需要审查”。

### 技术债务计量
SonarQube 将问题转化为**技术债务**度量，以天数或成本（例如美元）表示。这有助于团队预算和确定重构优先级。

### 分支和拉取请求分析
SonarQube 可以分析功能分支和拉取请求，允许只对新增代码强制执行质量门。这自然符合**Clean as You Code**工作流，即关注代码差异而非整个代码库。

### DevOps 集成
SonarQube 原生集成：
- **GitHub、GitLab、Bitbucket** – 拉取请求装饰、内联评论。
- **Jenkins、Azure DevOps、Travis CI、CircleCI** – 构建流水线集成。
- **Maven、Gradle、.NET、SonarScanner CLI** – 扫描调用。

### SonarLint IDE 扩展
SonarLint（支持 VS Code、IntelliJ、Eclipse、Visual Studio）连接到 SonarQube 服务器，在本地应用相同的规则，并在你输入时提供实时反馈。

---

## 安装

SonarQube 需要 **Java 17+** 和一个专用数据库（生产环境推荐 PostgreSQL）。它作为一个独立的 Web 应用运行。

### Docker（快速评估）

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:postgresql://host:port/sonarqube \
  -e SONAR_JDBC_USERNAME=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:community
```

> **注意：** 社区版不包含高级功能，如分支分析或拉取请求装饰。如需这些功能，请考虑开发者版或更高版本。

### 手动安装（Linux / macOS）

1. 从 [SonarSource 下载](https://www.sonarsource.com/products/sonarqube/downloads/) 下载最新版本。
2. 解压归档文件。
3. 在 `conf/sonar.properties` 中配置数据库连接：
   ```properties
   sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube
   sonar.jdbc.username=sonar
   sonar.jdbc.password=sonar
   ```
4. 启动服务器：
   ```bash
   # Linux/macOS
   bin/linux-x86-64/sonar.sh start
   # Windows
   bin/windows-x86-64/StartSonar.bat
   ```
5. 在 `http://localhost:9000` 访问 Web UI。默认凭据：`admin` / `admin`。

---

## 基本用法

### 1. 配置项目

登录 SonarQube，点击 **创建新项目**，给项目指定一个标识，然后选择质量配置和质量门。接着生成一个**项目令牌**（例如 `sqa_xxxx`）。该令牌用于验证扫描器。

### 2. 运行扫描

#### 使用 Maven

```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=my-project \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

#### 使用 Gradle

```groovy
// build.gradle
plugins {
    id "org.sonarqube" version "4.4.1.3373"
}

sonar {
    properties {
        property "sonar.projectKey", "my-project"
        property "sonar.host.url", "http://localhost:9000"
        property "sonar.token", "sqa_xxxx"
    }
}
```

```bash
./gradlew sonarqube
```

#### 使用 SonarScanner CLI

安装 SonarScanner（从 SonarSource 下载），然后：

```bash
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

### 3. 审查结果

扫描完成后，SonarQube 仪表板显示：
- **质量门状态** – 通过或失败。
- **问题** – 按严重程度（阻断、严重、主要、次要、信息）和类型（缺陷、漏洞、代码异味）分组。
- **安全热点** – 需要人工审查的代码区域。
- **覆盖率** – 如果你有 JaCoCo 或 dotCover 等工具，可以导入覆盖率报告。
- **重复** – 高亮重复代码块。

---

## 与 CI/CD 集成

### GitHub Actions

```yaml
name: SonarQube Scan
on: [push]
jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@v1.9.0
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    environment {
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_AUTH_TOKEN = credentials('sonarqube-token')
    }
    stages {
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube Server') {
                    sh 'mvn clean verify sonar:sonar'
                }
            }
        }
    }
}
```

### GitLab CI/CD

```yaml
variables:
  SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"
  GIT_DEPTH: "0"

sonarqube-check:
  image: maven:3.8.6-openjdk-17
  script:
    - mvn clean verify sonar:sonar
      -Dsonar.projectKey=$CI_PROJECT_ID
      -Dsonar.host.url=$SONAR_HOST_URL
      -Dsonar.token=$SONAR_TOKEN
      -Dsonar.branch.name=$CI_COMMIT_REF_NAME
```

---

## Clean as You Code 方法论

SonarQube 鼓励 **Clean as You Code** 的方法：不是试图修复所有现有问题，而是专注于在你今天编写的代码中避免新问题。这体现在：
- **关注新代码** – 度量和质量门针对新增/变更的代码。
- **拉取请求装饰** – 问题直接报告在 PR 差异上（GitHub、GitLab、Bitbucket）。
- **SonarLint** – 开发人员在提交前在 IDE 中捕获问题。

这减少了摩擦，并使质量改进可持续。

---

## 结论

SonarQube 是一个成熟、广泛采用的静态分析和质量治理工具。通过将其集成到你的开发流水线中，你可以自动化代码审查、强制执行安全标准并管理技术债务——最终交付更可靠、更安全的软件。

如需高级功能（分支分析、组合管理、特定语言覆盖率），请考虑升级到 SonarQube **开发者版**、**企业版**或**数据中心版**，或者使用云托管的 **SonarQube Cloud**（原 SonarCloud）。