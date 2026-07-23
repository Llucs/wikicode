---
title: gping - 网络监控工具
description: gping 是一个用于测量网络延迟的命令行工具，并具有实时图表可视化功能。
created: 2026-07-23
tags:
  - network
  - monitoring
  - gping
  - ping
status: draft
---

# gping - 网络监控工具

## 简介

**gping** 是一个用于测量两个网络节点之间往返时间 (RTT) 的命令行工具。它类似于 `ping` 命令，但使用 `glibc` 的 `getaddrinfo` 函数解析主机名，使其更灵活，能够处理不同的网络地址类型。gping 旨在用于网络监控、故障排除和性能测试。

## 主要功能

- **DNS解析**：使用 `getaddrinfo` 进行主机名解析，支持 IPv4、IPv6 以及其他地址类型。
- **支持多个主机**：可以同时对多个主机进行 ping 操作。
- **灵活配置**：允许自定义 ping 参数，如超时时间、数据包大小等。
- **扩展信息**：提供关于网络路径和 DNS 解析的详细信息。

## 历史

`gping` 是 GNU C 库 (glibc) 项目的一部分。最初实现是在 glibc 2.15 版本中加入的。自那时起，它不断改进和更新，以支持新的网络协议和特性。

## 使用场景

- **网络故障排除**：诊断网络延迟和连接问题。
- **性能测试**：评估网络连接和服务的性能。
- **脚本和自动化**：将网络测试集成到脚本和自动化工作流中。

## 安装

`gping` 通常包含在 glibc 包中，许多 Linux 发行版的基系统中都可以找到。以下是安装它的方法：

### Debian/Ubuntu
```sh
sudo apt-get update
sudo apt-get install glibc-doc
```

### Red Hat/CentOS
```sh
sudo yum install glibc-doc
```

### Arch Linux
```sh
sudo pacman -S glibc
```

## 基本用法

### 基本 Ping
要对主机名或 IP 地址进行基本 ping：
```sh
gping google.com
```

### 指定 Ping 选项
可以指定各种选项来自定义 ping 行为：

```sh
gping -c 10 -i 2 google.com
```
- `-c 10`：发送 10 个 ICMP 回声请求。
- `-i 2`：使用 2 秒的间隔发送 ping 数据包。

### 同时 ping 多个主机
要同时 ping 多个主机：
```sh
gping -c 1 -i 1 google.com example.com
```

### 详细输出
要获取详细输出：
```sh
gping -v google.com
```

## 示例用法

以下是一个示例会话：

```sh
gping -v google.com
```

输出可能如下所示：
```
PING google.com (93.184.216.34): 56 data bytes
64 bytes from 93.184.216.34: icmp_seq=0 ttl=56 time=24.1 ms
64 bytes from 93.184.216.34: icmp_seq=1 ttl=56 time=23.5 ms
64 bytes from 93.184.216.34: icmp_seq=2 ttl=56 time=23.3 ms
64 bytes from 93.184.216.34: icmp_seq=3 ttl=56 time=23.0 ms
64 bytes from 93.184.216.34: icmp_seq=4 ttl=56 time=24.4 ms
--- google.com ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 23.0/23.7/24.4/0.6 ms
```

在该示例中，`gping` 成功 ping 了 `google.com`，并提供了平均往返时间和其他相关统计数据。

## 结论

`gping` 是一个强大的网络诊断和性能测试工具，提供了灵活且可靠的网络延迟和地址解析测量方式。它与 glibc 的集成使其成为任何网络管理员工具箱中的宝贵补充。