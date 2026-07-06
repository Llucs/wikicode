---
title: Proxy Design Pattern
description: A structural design pattern that allows for a proxy, or placeholder, object to control access to another object, often for the purpose of adding functionality.
created: 2026-07-06
tags:
  - design-patterns
  - object-oriented-design
  - structural-patterns
status: draft
---

# Proxy Design Pattern

## What is the Proxy Design Pattern?

The Proxy Design Pattern is a structural design pattern that provides a surrogate or placeholder for another object to control access to it. It allows you to add responsibilities to the original object without modifying its structure. The primary goal of the proxy pattern is to provide a substitute or placeholder for another object. This pattern is widely used in various applications to manage resource access, control access to sensitive data, and optimize performance.

## Key Features

1. **Proxy Objects**: These are objects that act as a stand-in or surrogate for a real object. They can perform tasks before or after the real object.
2. **Controlled Access**: Proxies can control the access to the real object, allowing for additional actions before or after the real object's methods are called.
3. **Decoupling**: Proxies decouple the client from the real object, providing a layer of abstraction.
4. **Flexibility**: Proxies can be used in various scenarios, such as remote objects, resource access control, and caching.

## History

The Proxy Design Pattern was formalized in the book "Design Patterns: Elements of Reusable Object-Oriented Software" by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, commonly known as the Gang of Four (GoF). The pattern was introduced as a way to provide controlled access to objects and manage the lifecycle of objects.

## Use Cases

1. **Remote Proxy**: This allows a local object to act as a proxy for an object that is in a different address space.
2. **Virtual Proxy**: Used to provide a low-cost proxy for an expensive object creation.
3. **Protection Proxy**: Controls access to a sensitive object. For example, a proxy could be used to control access to a file or a database.
4. **Smart Reference**: Provides a way to manage the state of an object. For example, a proxy could be used to ensure that an object is in a valid state before it is accessed.
5. **Virtual Cache**: Uses a proxy to cache the results of an expensive operation.

## Installation

Since the Proxy Design Pattern is a design pattern and not a library or software, it does not require installation. However, to implement the pattern in a specific programming language, you would need to include the necessary classes or modules and follow the pattern's guidelines.

## Basic Usage

Here is a simple example of a proxy pattern implementation in Python:

```python
class RealSubject:
    def operation(self):
        return "RealSubject: Here is the result."

class Proxy:
    def __init__(self):
        self.real_subject = None

    def operation(self):
        if self.real_subject is None:
            self.real_subject = RealSubject()
        return f"Proxy: Processing ({self.real_subject.operation()})"

# Usage
proxy = Proxy()
print(proxy.operation())
```

In this example:
- `RealSubject` is the class that the proxy controls access to.
- `Proxy` is the class that provides controlled access to the `RealSubject`.
- The `Proxy` checks if `real_subject` is `None`. If it is, it creates a `RealSubject` instance. If not, it simply calls the `operation` method of the `RealSubject`.

## Conclusion

The Proxy Design Pattern is a powerful tool in the software developer's toolkit. It provides a way to control access to objects, manage resources, and optimize performance. By understanding its key features and use cases, developers can implement it effectively in various scenarios.