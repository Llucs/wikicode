---
title: 不可变基础设施：完全指南
description: 一种部署理念，服务器在部署后永不修改，以减少配置漂移并确保环境一致性。
created: 2026-06-23
tags:
  - infrastructure
  - devops
  - deployment
  - cloud-computing
  - configuration-management
status: draft
---

# 不可变基础设施：完全指南

## 什么是不可变基础设施？

不可变基础设施是一种部署模型，其中服务器或容器在配置完成后**永不修改**。当需要更新（补丁、配置更改或代码发布）时，运行中的实例会被销毁，并从标准化的、版本化的工件（称为“黄金镜像”或容器镜像）中创建一个全新的实例。

这种方法与**可变基础设施**形成鲜明对比，后者是传统方法，操作员通过SSH登录到运行中的服务器来应用补丁或运行配置管理工具（如Ansible、Chef、Puppet）。可变基础设施通常会导致“配置漂移”和“雪花服务器”——环境逐渐变得独特且无法重现。

不可变基础设施将服务器视为**牲畜，而非宠物**：它们是可丢弃的、有编号的且易于替换。对系统的任何更改都会触发完整的重新部署，而不是就地修改。

## 为什么使用不可变基础设施？

采用不可变基础设施的主要动机是消除配置漂移及其在不同环境中引起的可变性。好处包括：

- **可重现性：** 每次部署都从完全相同的工件开始，确保开发、预发和生产环境相同。
- **简单性：** 回滚变得简单——只需重新部署上一个镜像版本。
- **安全性：** 生产实例无需SSH访问，减少了攻击面。审计线索清晰：确切知道哪个镜像在何时运行。
- **扩展性：** 自动缩放组或编排器（例如Kubernetes）可以从已知的良好镜像启动新实例，确保所有节点一致。
- **可丢弃性：** 实例可以被终止并替换而不影响可用性，实现无缝的蓝绿部署和金丝雀部署。

## 关键原则与特性

| 原则 | 描述 |
|-----------|-------------|
| **可重现性** | 每个环境源自相同的版本化工件。 |
| **可丢弃性** | 实例是牲畜——可以随意销毁和重建。 |
| **原子化部署** | 更新通过替换整个堆栈进行，永远不会就地修补。 |
| **简化回滚** | 恢复到以前的状态意味着重新部署旧工件。 |
| **幂等性** | 相同的工件多次部署会产生相同的结果。 |
| **无实时修补** | 配置管理仅在镜像构建期间应用，而不是在运行时。 |

## 历史与起源

- **2012年——“宠物与牲畜”：** 这个类比由CloudScaling的Randy Bias和Microsoft的Bill Baker推广。宠物是独特的且需要手动照料；牲畜是编号的、标准化的且易于替换。
- **2013年——Chad Fowler的博文“不可变基础设施”** 正式定义了该术语。
- **2013年——Docker发布：** 容器成为不可变性的完美载体——短暂的、标准化的、从镜像构建。
- **2014年——HashiCorp Packer：** 使得从单个模板为多个云提供商（AWS AMI、Azure VHD、VMware）创建相同的机器镜像变得实用。
- **2015年至今——Kubernetes、Terraform、CI/CD流水线：** 这些工具使不可变部署成为云原生应用的行业标准。

## 工具生态系统

不可变基础设施是一种**范式**，而不是一个单一的软件包。下表概述了关键工具及其安装方法。

| 层面 | 工具 | 安装 | 用途 |
|-------|------|--------------|---------|
| **镜像构建器** | HashiCorp Packer | `brew install packer` / 下载二进制文件 | 创建黄金虚拟机/AMI |
| **容器镜像** | Docker / Podman | `brew install docker` / `apt install docker.io` | 构建容器镜像 |
| **镜像仓库** | Docker Hub / ECR / GCR | 云提供商控制台 / CLI设置 | 存储和版本化不可变工件 |
| **IaC / 编排** | Terraform / Pulumi / Kubernetes | `brew install terraform` / `kubectl` | 部署不可变资源 |
| **CI/CD** | GitLab CI / GitHub Actions | 配置运行器 | 自动化构建和部署 |
| **密钥注入** | HashiCorp Vault / AWS Secrets Manager | 安装Vault代理或CSI驱动 | 在启动时注入密钥，而非烘焙到镜像中 |

> **注意：** 传统的配置管理工具（Ansible、Chef、Puppet）仍然发挥作用，但仅限于**镜像构建阶段**——在Packer provisioner或Dockerfile中，绝不会针对运行中的生产实例。

## 基本用法示例

让我们通过一个典型的工作流：使用不可变原则在AWS上部署Nginx Web服务器。

### 步骤1：使用Packer构建黄金镜像

创建一个Packer模板，例如`web.pkr.hcl`：

```hcl
# web.pkr.hcl
source "amazon-ebs" "web" {
  ami_name      = "nginx-web-{{timestamp}}"
  source_ami    = "ami-0c02fb55956c7d316"   # Ubuntu 22.04 LTS
  instance_type = "t2.micro"
  region        = "us-east-1"
  ssh_username  = "ubuntu"
}

build {
  sources = ["source.amazon-ebs.web"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update -y",
      "sudo apt-get install nginx -y",
      "sudo systemctl enable nginx"
    ]
  }
}
```

构建镜像：

```bash
packer build web.pkr.hcl
```

输出是一个唯一的AMI ID，例如`ami-0abc123def456`。这成为不可变的工件。

### 步骤2：从不可变镜像部署实例

使用Terraform（`main.tf`）：

```hcl
# main.tf
resource "aws_instance" "web" {
  ami           = "ami-0abc123def456"
  instance_type = "t2.micro"

  tags = {
    Name = "immutable-web-v1"
  }
}
```

应用配置：

```bash
terraform apply
```

从黄金AMI启动一个EC2实例。如果它崩溃了，会从同一个镜像重新启动一个——没有漂移。

### 步骤3：推出新版本

1. 更新Packer模板（例如，安装更新的Nginx版本，复制更新的静态文件）。
2. 运行`packer build`生成一个**新的**AMI：`ami-0new123ghi789`。
3. 将`main.tf`中的`ami`字段修改为`ami-0new123ghi789`。
4. 执行`terraform apply`。Terraform将销毁旧实例并从新镜像创建一个全新的实例。

**没有实例会被就地修补。** 每次更改都是完全的替换。

### 步骤4：蓝绿部署（生产模式）

对于零停机更新，在Terraform中定义两个独立的自动缩放组（ASG）或启动模板：

- **蓝色** = 当前版本（v1）
- **绿色** = 新版本（v2）

部署绿色ASG后，运行健康检查，然后将应用程序负载均衡器（ALB）的目标组从蓝色切换到绿色。一旦流量稳定，终止蓝色ASG。

## 挑战与反模式

- **可变状态：** 数据库和其他有状态系统不能完全被视为不可变。状态必须隔离在计算层之外（例如，RDS、带快照的EBS卷，或带持久卷声明的Kubernetes StatefulSets）。
- **启动时间：** 构建完整的操作系统镜像比热补丁花费的时间更长。容器大大减少了这一点，但大型虚拟机镜像仍然可能很麻烦。
- **镜像大小：** 如果没有规范（多阶段Docker构建、清理脚本），镜像会变得臃肿并导致部署缓慢。
- **调试：** 没有SSH访问，调试完全依赖于结构化日志（ELK、CloudWatch、Loki）和分布式追踪（OpenTelemetry）。
- **密钥管理：** 密钥绝不能烘焙到镜像中。必须在启动时通过Vault、AWS Secrets Manager或CSI驱动注入。

## 结论

不可变基础设施将运维复杂性**左移**——转移到构建流水线中，而不是在生产中被动管理。虽然它需要在CI/CD和工具（Packer、Terraform、Kubernetes）上进行前期投资，但它消除了由配置漂移和环境不一致引起的整个类别的故障。它是现代云原生运维的基石，也是可靠、安全和可扩展的微服务架构的先决条件。