---
title: DBeaver - Universal Database Management Tool
description: A free, open-source, cross-platform database management tool and SQL client for developers, DBAs, and data analysts.
created: 2026-06-17
tags:
  - database
  - sql
  - management
  - tools
  - open-source
status: draft
---

# DBeaver - Universal Database Management Tool

## Overview

DBeaver is a **free, open-source, cross-platform** database management tool and SQL client. It provides a rich graphical interface to interact with any database that supports JDBC or ODBC drivers, making it a universal tool for developers, database administrators, and data analysts.

- **License**: Community Edition (CE) is released under **Apache 2.0**; commercial Pro/Enterprise/Team editions are also available.
- **Platform**: Windows, macOS, Linux (also available as a portable application).
- **Architecture**: Built on the Eclipse Rich Client Platform (RCP) using Java.
- **History**: Initiated in 2010 by Serge Rielau, a database expert formerly involved with Apache Derby and Oracle. The project quickly gained widespread adoption, leading to the formation of DBeaver Corp.

DBeaver is ideal for:
- **Application Development** – Write, debug, and optimize SQL queries.
- **Database Administration** – Manage schemas, users, sessions, and indexes.
- **Data Analysis** – Run analytical queries and export results to various formats.
- **Data Engineering** – Transfer data between different databases without heavy scripting.
- **Education** – Learn SQL and relational database concepts through an intuitive GUI.

## Key Features

| Feature | Description |
|---------|-------------|
| **Wide Database Support** | Connects to 100+ databases out of the box, including MySQL/MariaDB, PostgreSQL, Oracle, SQL Server, SQLite, DB2, Snowflake, Redshift, ClickHouse, and many more. |
| **Advanced SQL Editor** | Syntax highlighting, code completion, query execution with multiple result tabs, execution plan visualization (graphical), SQL formatting, and parameterised queries. |
| **Data Browser / Spreadsheet** | Powerful inline editing, advanced filtering, sorting, and handling of BLOB/CLOB data directly in a grid interface. |
| **ER Diagrams** | Automatically generate Entity-Relationship diagrams with reverse engineering (right-click on a schema or table). |
| **Schema Management** | Object browser for browsing, creating, and editing tables, views, indexes, procedures, and functions. |
| **Data Transfer** | Bulk export/import between databases and file formats (CSV, JSON, XML, Excel, SQL, Markdown, HTML). |
| **Administration Tools** | Session manager, task scheduler (Pro), user/role management, and integrated SSH/SSL/Proxy tunneling. |
| **Extensibility** | Plugin architecture; available plugin for additional drivers, version control (Git), and diagram customizations. |
| **Cross‑Platform** | Runs on Windows, macOS, and Linux. |

## Installation

DBeaver is available through multiple channels. Choose the method that suits your environment.

### Official Installer (All Platforms)

Download the installer for your OS from [dbeaver.io](https://dbeaver.io) (Community Edition) or [dbeaver.com](https://dbeaver.com) (Enterprise).

### Package Managers

**macOS (Homebrew)**
```bash
brew install --cask dbeaver-community
```

**Linux (Snap)**
```bash
sudo snap install dbeaver-ce
```

**Linux (APT / YUM – Official Debian/RPM repos)**
```bash
# Debian/Ubuntu
wget -O - https://dbeaver.io/debs/dbeaver.gpg.key | sudo apt-key add -
echo "deb https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list
sudo apt update && sudo apt install dbeaver-ce

# RHEL/CentOS/Fedora
sudo rpm --import https://dbeaver.io/rpms/dbeaver.gpg.key
sudo yum install dbeaver-ce
```

**Windows (winget / Chocolatey)**
```powershell
# winget (Windows 10 / 11)
winget install DBeaver.DBeaverCE

# Chocolatey
choco install dbeaver
```

**Portable Windows Version**

A portable executable is available from the official website, ideal for running from a USB drive without installation.

## Getting Started – Basic Usage

### 1. Create a Database Connection

1. Launch DBeaver.
2. Click the **New Database Connection** button (plug icon) in the toolbar.
3. Select your database type (e.g., **PostgreSQL**).
4. Fill in the connection details:
   - Host, Port, Database name, Username, Password.
5. Click **Test Connection**. DBeaver will automatically prompt to download the required JDBC driver if not already cached.
6. Click **Finish**. The connection appears in the **Database Navigator** panel.

![Connection Wizard Example](https://dbeaver.com/docs/images/connection-wizard.png) <!-- Placeholder URL; actual docs provide screenshots -->

### 2. Browse and Query Data

- In the **Database Navigator**, expand a connection to see schemas, tables, views, etc.
- Right‑click a table and select **View Data** to open a data grid.
- To write custom SQL, press `Ctrl + ]` (Windows/Linux) or `Cmd + ]` (macOS) to open a new **SQL Editor**.

**Example SQL query:**
```sql
-- Select users with their latest order
SELECT u.id, u.name, o.order_date
FROM users u
JOIN (
    SELECT user_id, MAX(order_date) AS order_date
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id
ORDER BY o.order_date DESC;
```

- Execute the query with `Ctrl + Enter` (Win/Lin) or `Cmd + Enter` (macOS).
- Results appear in the result grid below the editor.

### 3. Edit and Export Data

- Click directly on a cell value in the result grid to edit it (requires **Edit** permission on the table).
- Right‑click the result grid and choose **Export Data**.
- Select the desired format (CSV, Excel, JSON, SQL INSERT, XML, Markdown, etc.) and configure options.

## Advanced Usage

### Entity‑Relationship (ER) Diagrams

DBeaver can generate ER diagrams for a schema or specific tables.

1. Right‑click a schema in the Database Navigator.
2. Select **View Diagram** (or open the **ER Diagram** tab).
3. The diagram displays tables, columns, relationships, and indexes.
4. You can rearrange elements, export the diagram as an image, or print it.

### Data Transfer / Migration

Use the **Transfer Data** wizard to copy data between databases or extract data to files.

1. Right‑click a table or schema.
2. Select **Data > Transfer Data**.
3. Choose the source (e.g., a table) and target (another database connection or file).
4. Configure column mappings and transformation rules.
5. Execute the transfer.

### Execution Plan (EXPLAIN)

Visualize the query execution plan for SQL tuning.

1. In the SQL Editor, write a query.
2. Click the **Explain Plan** button (or right‑click → **Explain Plan**).
3. DBeaver shows a graphical plan with cost details and index usage.

### Comparison Tool (Pro/Enterprise)

The **Structure Compare** and **Data Compare** tools allow you to diff schemas or data between two databases or environments.

- Available in commercial editions.

## Configuration & Customization

### Connection Settings

- **Driver Properties**: Modify JDBC driver attributes (e.g., timeouts, SSL mode, chunk sizes) from the connection editor.
- **SSH Tunnel**: Configure SSH tunneling for secure access to remote databases (in the **SSH** tab of the connection settings).
- **SSL**: Enable SSL and import certificates via the **SSL** tab.

### Global Preferences

- `Window → Preferences` (Windows/Linux) or `DBeaver → Preferences` (macOS).
- **Appearance**: Switch between light/dark themes, adjust font sizes.
- **Editors**: Configure SQL formatting style, auto‑completion behavior, and execution options.
- **Connections**: Set default transaction isolation levels, auto‑commit, and idle timeouts.

### Driver Management

- **Driver Manager**: `Database → Driver Manager`. View, edit, or add custom JDBC drivers.
- Download missing drivers directly from DBeaver’s driver repository when first connecting to a database.

## Automation & Scripting

### DBeaver CLI (Pro/Enterprise Only)

DBeaver Pro/Enterprise includes a command‑line tool (`dbeaver-cli`) for executing SQL scripts, exporting data, or running tasks without a GUI.

```bash
# Connect and run a script against a PostgreSQL instance
dbeaver-cli -driver postgresql -url jdbc:postgresql://localhost:5432/mydb \
            -user myuser -password mypass -script query.sql
```

### Task Scheduler (Pro/Enterprise)

Schedule recurring exports, data transfers, or SQL scripts using the built‑in scheduler (cron‑like interface).

## Integrations

- **Version Control**: Git integration plugin (available in Community) – commit SQL scripts or compare with committed versions.
- **Docker**: Running DBeaver directly in a container for CI/CD pipelines is possible with the CLI edition.
- **Cloud Databases**: Pre‑configured drivers for Snowflake, Amazon Redshift, Google BigQuery, Azure SQL, etc.
- **SSH/SSL**: Built‑in support for secure connections and proxy authentication.

## Compatibility & Performance

| Aspect | Details |
|--------|---------|
| **Supported Operating Systems** | Windows 10+, macOS 10.15+, Linux (x64, amd64, aarch64) |
| **Java Requirements** | JDK 11 or later (bundled with installers) |
| **Database Support** | 100+ databases via JDBC/ODBC (including relational, NoSQL‐like, cloud) |
| **Performance Tips** | - Use indexes for large queries.<br>- Close idle connections in preferences.<br>- Enable **“Use batch updates”** for bulk operations.<br>- For extremely large datasets, export in chunks or use dedicated migration tools. |

## Troubleshooting & FAQ

### Common Issues

1. **“Driver not found” / “Cannot connect”**
   - DBeaver will prompt to download the driver. If the automatic download fails, go to `Database → Driver Manager`, select your database, and click **Download/Update**.
   - Ensure you have internet access or manually place the JAR file in the driver library.

2. **Connection hangs or times out**
   - Verify network connectivity and firewall rules.
   - Check the SSH/SSL settings; a misconfigured tunnel can block connections.
   - Increase the connection timeout in the driver properties.

3. **SQL Editor performance is slow**
   - Disable automatic metadata loading: `Preferences → Database → Navigator → Disable lazy metadata reading`.
   - Reduce result set limit in the editor toolbar.

4. **BLOB/CLOB cannot be edited**
   - DBeaver supports inline editing for small objects. For large objects, use the **View / Edit Value** dialog (right‑click cell → **View Value**).

### Frequently Asked Questions

**Q: Is DBeaver fully free?**
A: The Community Edition is free and open‑source (Apache 2.0). The Pro, Enterprise, and Team editions are commercial and add features like NoSQL support, AI assistance, and a CLI.

**Q: Can I use DBeaver for production databases?**
A: Yes, the Community Edition is production‑ready for development and DBA tasks. For mission‑critical environments, consider the Enterprise edition with additional support and auditing.

**Q: Does DBeaver work with MongoDB or other NoSQL databases?**
A: The Community Edition has basic MongoDB support. Full NoSQL and cloud DB support (including MongoDB, Cassandra, and DynamoDB) are available in the Enterprise edition.

**Q: How do I uninstall DBeaver completely?**
A: Use your system’s package manager (e.g., `brew uninstall --cask dbeaver-community`, `snap remove dbeaver-ce`) or the OS uninstaller. User settings are stored in `~/.dbeaver` on macOS/Linux or `%APPDATA%\DBeaver` on Windows; remove those directories to purge all configuration.

## Conclusion

DBeaver is a powerful, flexible, and user‑friendly database tool that fits seamlessly into any developer’s workflow. Its open‑source core, extensive database support, and rich feature set make it an essential utility for anyone working with data.

For more information, visit the official documentation at [dbeaver.com/docs](https://dbeaver.com/docs/) or contribute to the community on [GitHub](https://github.com/dbeaver/dbeaver).