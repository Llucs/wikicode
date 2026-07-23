---
title: gping - Network Monitoring Tool
description: gping is a command-line tool for measuring network latency with real-time graph visualization.
created: 2026-07-23
tags:
  - network
  - monitoring
  - gping
  - ping
status: draft
---

# gping - Network Monitoring Tool

## Overview

**gping** is a command-line tool for measuring the round-trip time (RTT) between two network nodes. It is similar to the `ping` command but uses the `glibc`'s `getaddrinfo` function to resolve hostnames, making it more flexible and capable of handling different types of network addresses. gping is designed for network monitoring, troubleshooting, and performance testing.

## Key Features

- **DNS Resolution**: Uses `getaddrinfo` for hostname resolution, supporting IPv4, IPv6, and other address types.
- **Multiple Host Support**: Can ping multiple hosts simultaneously.
- **Flexible Configuration**: Allows customization of ping parameters such as timeout, packet size, etc.
- **Extended Information**: Provides detailed information about the network path and DNS resolution.

## History

`gping` was developed as part of the GNU C Library (glibc) project. The first implementation was added to glibc in version 2.15. Since then, it has been continuously improved and updated to support newer network protocols and features.

## Use Cases

- **Network Troubleshooting**: Diagnosing network latency and connectivity issues.
- **Performance Testing**: Evaluating the performance of network connections and services.
- **Scripting and Automation**: Incorporating network testing into scripts and automation workflows.

## Installation

`gping` is typically included in the glibc package, which is part of the base system on many Linux distributions. Here’s how you can install it:

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

## Basic Usage

### Basic Ping
To perform a basic ping to a hostname or IP address:
```sh
gping google.com
```

### Specifying Ping Options
You can specify various options to customize the ping behavior:

```sh
gping -c 10 -i 2 google.com
```
- `-c 10`: Send 10 ICMP echo requests.
- `-i 2`: Use a 2-second interval between ping packets.

### Pinging Multiple Hosts
To ping multiple hosts simultaneously:
```sh
gping -c 1 -i 1 google.com example.com
```

### Detailed Output
To get a detailed output:
```sh
gping -v google.com
```

## Example Usage

Here is an example session:

```sh
gping -v google.com
```

Output might look like this:
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

In this example, `gping` successfully pings `google.com` and provides the average round-trip time and other relevant statistics.

## Conclusion

`gping` is a powerful tool for network diagnostics and performance testing, offering a flexible and robust way to measure network latency and address resolution. Its integration with glibc makes it a valuable addition to any network administrator's toolkit.