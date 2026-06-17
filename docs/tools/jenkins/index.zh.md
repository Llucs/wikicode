---
title: Jenkins CI/CD 自动化服务器
description: 用于软件项目持续集成和持续交付的自动化服务器。
created: 2026-06-15
tags:
  - jenkins
  - ci
  - cd
  - devops
  - automation
  - java
status: draft
ecosystem: ci-cd
---

# Jenkins CI/CD 自动化服务器

## 它是什么

Jenkins 是一个用 Java 编写的开源自动化服务器。它用于自动化软件的构建、测试和部署，实现持续集成（CI）和持续交付（CD）。Jenkins 最初源自 Hudson 项目，现在已成为流水线编排的行业标准。

## 为什么选择 Jenkins？

- **可扩展性：** 超过 1800 个插件允许与几乎所有的 DevOps 工具集成（Git、Docker、Kubernetes、AWS、Azure、Slack 等）。
- **灵活性：** 支持从简单的自由风格任务到作为代码定义的复杂多阶段流水线。
- **分布式构建：** 主/代理架构允许将工作负载分布到多台机器上。
- **开源且成熟：** 免费（MIT 许可证），拥有庞大社区和丰富文档。
- **丰富的生态系统：** 提供用于源代码管理、构建工具、测试报告、制品管理、部署和通知的插件。

## 安装

Jenkins 需要 Java 8、11 或 17（推荐 LTS）。存在多种安装方法：

### WAR 文件

```bash
java -jar jenkins.war
```
在 8080 端口上独立运行 Jenkins，适合快速测试。

### 原生包

**Debian/Ubuntu:**

```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```

**Red Hat/CentOS:**

```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo yum install jenkins
```

### Docker

```bash
docker run -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### Kubernetes（Helm Chart）

```bash
helm repo add jenkins https://charts.jenkins.io
helm repo update
helm install jenkins jenkins/jenkins --namespace jenkins --create-namespace
```

安装后，访问 `http://localhost:8080` 进入 Jenkins，并从日志或文件（`/var/lib/jenkins/secrets/initialAdminPassword`）中获取初始管理员密码。

## 基本使用

### 1. 创建任务

- **自由风格任务：** 包含少量步骤的简单任务。
- **流水线：** 在 `Jenkinsfile` 中定义构建生命周期。

### 2. 配置源代码

- 使用凭据（用户名/密码或 SSH 密钥）连接到 Git 仓库。

### 3. 设置触发器

- **轮询 SCM：** `* * * * *`（每分钟）
- **Webhook：** 推送时从 GitHub/GitLab 触发。
- **Cron：** 例如 `H 2 * * 1-5`（工作日凌晨 2 点）

### 4. 添加构建步骤

- 执行 shell/batch 命令。
- 运行 Maven/Gradle 目标。
- 构建 Docker 镜像。
- 调用其他构建工具。

### 5. 构建后操作

- 归档制品（如 JAR、报告）。
- 发布测试结果（JUnit、HTML 报告）。
- 部署到服务器。
- 发送通知（Slack、邮件）。

## 主要功能及示例

### 流水线即代码

源代码仓库中的声明式 `Jenkinsfile`：

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh 'mvn clean compile'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'mvn deploy'
            }
        }
    }
    post {
        failure {
            slackSend channel: '#ops', message: "Build failed."
        }
    }
}
```

该流水线在每次提交时自动运行：编译代码、运行测试、归档测试结果，并从 `main` 分支进行部署。

### 多分支流水线

自动为仓库中的每个分支和拉取请求创建流水线。

```groovy
// In Jenkins UI: New Item → Multibranch Pipeline → add Git source
// The Jenkinsfile from the branch controls execution.
```

### 使用代理进行分布式构建

Jenkins 可以标记代理（如 "linux"、"docker"、"high-mem"）并将任务分配给它们：

```groovy
pipeline {
    agent { label 'linux && docker' }
    stages {
        stage('Test') {
            steps {
                sh 'docker build -t myapp .'
            }
        }
    }
}
```

### 共享库

跨仓库的可复用流水线代码。在共享库 Git 仓库中定义：

**vars/buildApp.groovy:**

```groovy
def call(String project) {
    sh "mvn -f ${project}/pom.xml clean package"
}
```

然后在任何 `Jenkinsfile` 中：

```groovy
library identifier: 'my-lib@master', retriever: modernSCM(...)
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                buildApp('my-service')
            }
        }
    }
}
```

### 与 Kubernetes 集成

使用 Kubernetes 插件动态启动构建代理：

```groovy
pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: maven
    image: maven:3.8.4-openjdk-11
    command: ['cat']
    tty: true
"""
        }
    }
    stages {
        stage('Build') {
            steps {
                container('maven') {
                    sh 'mvn clean install'
                }
            }
        }
    }
}
```

### REST API

Jenkins 提供了全面的 REST API 用于自动化。触发构建的 curl 示例：

```bash
curl -X POST http://jenkins-url/job/my-job/build \
  --user username:api-token
```

列出任务：

```bash
curl http://jenkins-url/api/json
```

### Blue Ocean UI

现代化的流水线可视化界面（需要 Blue Ocean 插件）。提供构建、日志和流水线阶段的图形化视图。

## 配置即代码（JCasC）

使用 `configuration-as-code` 插件以 YAML 声明式管理 Jenkins 配置。

**jenkins.yaml:**

```yaml
jenkins:
  systemMessage: "Managed by JCasC"
  numExecutors: 2
  globalNodeProperties:
  - envVars:
      env:
      - key: VARIABLE1
        value: "value1"
security:
  globalMatrixAuthorizationStrategy:
    grantedPermissions:
      - "Overall/Administer:admin"
      - "Job/Build:developer"
jobs:
  - script: >
      multibranchPipelineJob('my-pipeline') {
        branchSources {
          git {
            remote('https://github.com/org/repo.git')
            credentialsId('github-creds')
          }
        }
      }
```

在启动时应用，或通过 `reload-configuration-as-code` 端点重新加载。

## 插件

关键插件类别：

- **源代码管理：** Git、GitHub、GitLab、Bitbucket、Subversion。
- **构建：** Maven、Gradle、Ant、NodeJS、Docker Pipeline。
- **测试：** JUnit、HTML Publisher、Allure、Cucumber Reports。
- **部署：** Kubernetes、AWS CodeDeploy、Ansible、SSH。
- **通知：** Slack、Email Extension、PagerDuty。
- **工具：** Credentials Binding、Pipeline Utility Steps、Job DSL。

## 最佳实践

- **使用流水线即代码** – 将 `Jenkinsfile` 与项目一同存储在 SCM 中。
- **使用共享库** – 避免重复流水线逻辑。
- **保持代理无状态** – 使用 Docker 或 Kubernetes 代理。
- **保护凭据安全** – 使用凭据插件，而非明文。
- **备份 JENKINS_HOME** – 定期备份任务配置和插件数据。
- **限制并发** – 使用 `properties([disableConcurrentBuilds()])` 处理资源敏感型任务。
- **使用 Blue Ocean** 获得更好的流水线可视化。
- **通过 Prometheus Metrics 插件** 使用 Prometheus 进行监控。

## 故障排除

- **查看日志：** `tail -f /var/log/jenkins/jenkins.log`
- **重新加载配置：** `Manage Jenkins → Reload Configuration from Disk`
- **清除构建队列：** 点击构建队列项 → "Cancel"
- **运行 Groovy 脚本：** `Manage Jenkins → Script Console` 进行诊断。
- **增加堆大小：** 在启动时设置 `JAVA_OPTS="-Xmx2048m -Xms1024m"`。

## 相关链接

- [官方 Jenkins 文档](https://www.jenkins.io/doc/)
- [插件索引](https://plugins.jenkins.io/)
- [流水线语法生成器](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [JCasC 文档](https://www.jenkins.io/projects/jcasc/)

---

*此页面作为 WikiCode 开发团队文档的一部分创建。*