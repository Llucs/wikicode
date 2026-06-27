---
title: 代理模式
description: 一种软件设计模式，允许通过代理或占位符对象来控制对另一个对象的访问，通常用于缓存、控制或安全目的。
created: 2026-06-27
tags:
  - 设计模式
  - 结构模式
  - Python
  - Java
  - C++
status: 草稿
---

# 代理模式

## 什么是代理模式？

代理模式是一种结构设计模式，它使能够创建另一个对象的代理或占位符对象，以控制对其的访问。此模式特别适用于管理资源访问、确保安全性和优化性能。

## 主要特征

1. **受控访问**：允许对真实对象进行受控访问。
2. **资源管理**：可以用于管理文件、数据库或网络连接等资源。
3. **性能优化**：可以通过延迟加载或缓存来提高性能。
4. **安全性**：通过控制对真实对象的哪些部分是可访问的来提供一层安全。
5. **日志记录和监控**：可以记录操作或监控使用模式。

## 历史

代理模式最早由Erich Gamma、Richard Helm、Ralph Johnson和John Vlissides在其著作《设计模式：面向对象软件重用元素》（通常称为“四人帮”书籍）中描述。该书于1994年出版，并介绍了代理模式以及其他设计模式。自此以后，该模式在软件开发中被广泛用于解决各种与资源管理和控制相关的问题。

## 使用案例

1. **远程代理**：通过提供远程对象的本地表示来允许远程访问一个对象。
2. **虚代理**：提供一个轻量且高效的占位符来替代昂贵的对象创建。
3. **保护代理**：通过提供一个代理来控制对对象的访问，该代理执行安全策略。
4. **智能指针**：管理对象的生命周期并确保正确的资源管理。
5. **用于缓存的虚代理**：缓存数据以避免昂贵的操作并提高性能。

## 安装

代理模式可以在各种编程语言中实现。以下是在Python中的示例：

```python
class RealSubject:
    def operation(self):
        return "RealSubject: Handling request."

class Proxy:
    def __init__(self, real_subject=None):
        self._real_subject = real_subject

    def operation(self):
        if self.check_access():
            print("Proxy: Performing operation.")
            return self._real_subject.operation()
        else:
            return "Proxy: Access denied."

    def check_access(self):
        # 模拟访问控制逻辑
        return True  # 为了简化，总是允许访问

# 客户端代码
real_subject = RealSubject()
proxy = Proxy(real_subject)

proxy.operation()
```

### 详细示例

```python
class RealSubject:
    def operation(self):
        return "RealSubject: Handling request."

class Proxy:
    def __init__(self, real_subject=None):
        self._real_subject = real_subject
        self._access_granted = False

    def operation(self):
        if self.check_access():
            print("Proxy: Performing operation.")
            return self._real_subject.operation()
        else:
            return "Proxy: Access denied."

    def check_access(self):
        # 模拟访问控制逻辑
        return self._access_granted

# 客户端代码
real_subject = RealSubject()
proxy = Proxy(real_subject)

# 授予访问权限
proxy._access_granted = True
print(proxy.operation())

# 拒绝访问
proxy._access_granted = False
print(proxy.operation())
```

## 基本用法

1. **创建RealSubject**：这是执行实际工作的真正对象。
2. **创建Proxy**：代理对象作为真实对象的面纱。
3. **检查访问**：代理检查是否允许访问真实对象。
4. **委托操作**：如果允许访问，则代理将操作委托给真实对象；否则，拒绝访问。

## 结论

代理模式是一种多功能设计模式，有助于在软件系统中管理访问、优化性能和增强安全性。通过提供一种灵活的方式来控制对对象的访问，代理模式可以在各种场景中应用，使其成为软件开发人员工具箱中的宝贵工具。