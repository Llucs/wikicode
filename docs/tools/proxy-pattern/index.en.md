---
title: Proxy Pattern
description: A software design pattern that allows for a surrogate or placeholder object to control access to another object, often for the purposes of caching, control, or security.
created: 2026-06-27
tags:
  - design-patterns
  - structural-patterns
  - python
  - java
  - c++
status: draft
---

# Proxy Pattern

## What is the Proxy Pattern?

The Proxy Pattern is a structural design pattern that enables creating a surrogate or placeholder for another object to control access to it. This pattern is particularly useful for managing access to resources, ensuring security, and optimizing performance.

## Key Features

1. **Controlled Access**: Allows controlled access to a real object.
2. **Resource Management**: Can be used to manage resources such as files, databases, or network connections.
3. **Performance Optimization**: Enables lazy loading or caching to improve performance.
4. **Security**: Provides a layer of security by controlling what parts of the real object are accessible.
5. **Logging and Monitoring**: Can log operations or monitor usage patterns.

## History

The Proxy Pattern was first described by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides in their book "Design Patterns: Elements of Reusable Object-Oriented Software." The book, often referred to as the "Gang of Four" (GoF) book, was published in 1994 and introduced the Proxy Pattern along with other design patterns. Since then, the pattern has been widely used in software development to solve various problems related to resource management and control.

## Use Cases

1. **Remote Proxy**: Allows remote access to an object by providing a local representation of a remote object.
2. **Virtual Proxy**: Provides a lightweight and efficient placeholder for an expensive-to-create object.
3. **Protection Proxy**: Controls access to an object by providing a proxy that enforces security policies.
4. **Smart Pointer**: Manages the lifecycle of an object and ensures proper resource management.
5. **Virtual Proxy for Caching**: Caches data to avoid expensive operations and improve performance.

## Installation

The Proxy Pattern can be implemented in various programming languages. Here’s an example in Python:

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
        # Simulate access control logic
        return True  # For simplicity, always allow access

# Client code
real_subject = RealSubject()
proxy = Proxy(real_subject)

proxy.operation()
```

### Detailed Example

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
        # Simulate access control logic
        return self._access_granted

# Client code
real_subject = RealSubject()
proxy = Proxy(real_subject)

# Grant access
proxy._access_granted = True
print(proxy.operation())

# Deny access
proxy._access_granted = False
print(proxy.operation())
```

## Basic Usage

1. **Creating the RealSubject**: This is the real object that performs the actual work.
2. **Creating the Proxy**: The proxy object acts as a facade for the real object.
3. **Checking Access**: The proxy checks if access to the real object is allowed.
4. **Delegating Operations**: If access is allowed, the proxy delegates the operation to the real object; otherwise, it denies access.

## Conclusion

The Proxy Pattern is a versatile design pattern that helps manage access, optimize performance, and enhance security in software systems. By providing a flexible way to control access to an object, the Proxy Pattern can be applied in a variety of scenarios, making it a valuable tool in the software developer’s toolkit.