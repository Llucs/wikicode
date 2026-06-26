---
title: Promtail - A Log Shipper for Prometheus
description: Promtail is a lightweight, flexible, and highly configurable log shipper designed to collect logs from various sources and forward them to a Prometheus server or other compatible storage systems.
created: 2026-06-26
tags:
  - logging
  - prometheus
  - grafana
status: draft
---

# Promtail - A Log Shipper for Prometheus

Promtail is a log shipper for Prometheus, developed and maintained by Grafana Labs. It is a lightweight, flexible, and highly configurable tool designed to collect logs from various sources and forward them to a Prometheus server or other compatible storage systems.

## Key Features

1. **High Availability and Fault Tolerance**: Promtail is designed to handle failures gracefully. It can automatically retry failed log entries and supports configuration for log entry reprocessing.
2. **Flexibility**: Promtail supports various log formats (JSON, syslog, plain text) and can be configured to match and extract relevant information from logs using regular expressions.
3. **Scalability**: Promtail is optimized for high-volume log processing and can handle large amounts of data efficiently.
4. **Security**: It supports TLS for secure communication between Promtail and the Prometheus server.
5. **Configuration**: Configurations are stored in a YAML file, which makes it easy to manage and maintain.
6. **Integration**: Promtail can be easily integrated into existing logging infrastructures and is compatible with a variety of logging systems.

## History

Promtail was first introduced in 2018 as part of the Grafana Labs project. It was initially developed to address the need for a lightweight and efficient log shipper that could be integrated with the Prometheus monitoring system. Over the years, Promtail has evolved to become a robust and widely-used tool in the logging and monitoring ecosystem.

## Use Cases

1. **Application Logs**: Promtail can be used to collect application logs from servers, containers, and other sources and forward them to Prometheus for monitoring and alerting.
2. **Security Monitoring**: By collecting and parsing log data, Promtail can be used to detect security breaches, anomalies, and other security-related events.
3. **Diagnostic Support**: Promtail helps in diagnosing issues in production systems by providing detailed logs that can be analyzed for troubleshooting.
4. **Compliance**: Promtail can be used to ensure that log data is collected and stored in compliance with regulatory requirements.
5. **Monitoring**: Promtail integrates seamlessly with Prometheus for real-time monitoring of logs and alerting based on log data.

## Installation

### Prerequisites
- Go (for building from source)
- Docker (for containerized installations)

### Building from Source
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/grafana/promtail.git
   cd promtail
   ```

2. **Build the Binary**:
   ```sh
   make build
   ```

3. **Run Promtail**:
   ```sh
   ./promtail
   ```

### Docker Installation
1. **Pull the Docker Image**:
   ```sh
   docker pull grafana/promtail
   ```

2. **Run Promtail with Docker**:
   ```sh
   docker run -d --name promtail \
     -v /path/to/config.yml:/promtail/promtail.yml \
     grafana/promtail -config.file=/promtail/promtail.yml
   ```

## Basic Usage

### Configuring Promtail
Promtail uses a YAML configuration file to specify the log sources, parsing rules, and output destinations. Here is an example configuration:

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://localhost:9091/log

scrape_configs:
  - job_name: server
    static_configs:
      - targets:
          - localhost
        labels:
          job: server
```

### Running Promtail
Once the configuration file is set up, you can run Promtail to start collecting logs.

```sh
promtail -config.file=/path/to/config.yml
```

### Monitoring Logs
Promtail forwards the collected logs to the specified Prometheus server. You can then use Prometheus to query and visualize the log data.

## Conclusion

Promtail is a powerful tool for collecting and forwarding log data to Prometheus, providing a seamless integration for monitoring and alerting. Its flexibility and ease of use make it a valuable addition to any logging and monitoring infrastructure.

---