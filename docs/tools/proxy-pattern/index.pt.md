---
title: Pattern Proxy
description: Um padrão de design de software que permite criar um substituto ou objeto de占位符来控制访问另一个对象，通常用于缓存、控制或安全目的。
created: 2026-06-27
tags:
  - padrões-de-diretoria
  - padrões-estruturais
  - python
  - java
  - c++
status: rascunho
---

# Pattern Proxy

## O que é o Pattern Proxy?

O Pattern Proxy é um padrão de direção estrutural que permite criar um substituto ou objeto de占位符来控制访问另一个对象。该模式特别适用于管理访问资源、确保安全性和优化性能。

## Características Principais

1. **Acesso Controlado**: Permite o acesso controlado a um objeto real.
2. **Gerenciamento de Recursos**: Pode ser usado para gerenciar recursos como arquivos, bancos de dados ou conexões de rede.
3. **Optimização de Desempenho**: Permite o carregamento lento ou cacheamento para melhorar o desempenho.
4. **Segurança**: Fornece uma camada de segurança ao controlar quais partes do objeto real são acessíveis.
5. **Log e Monitoramento**: Pode registrar operações ou monitorar padrões de uso.

## História

O Pattern Proxy foi descrito pela primeira vez por Erich Gamma, Richard Helm, Ralph Johnson, e John Vlissides no livro "Design Patterns: Elements of Reusable Object-Oriented Software". O livro, frequentemente referido como o "Gang of Four" (GOF) livro, foi publicado em 1994 e introduziu o Pattern Proxy junto com outros padrões de direção. Desde então, o padrão tem sido amplamente utilizado no desenvolvimento de software para resolver diversos problemas relacionados ao gerenciamento e controle de recursos.

## Casos de Uso

1. **Proxy Remoto**: Permite acesso remoto a um objeto através de uma representação local de um objeto remoto.
2. **Proxy Virtual**: Fornece um substituto leve e eficiente para um objeto caro de criar.
3. **Proxy de Proteção**: Controle o acesso a um objeto fornecendo um proxy que executa políticas de segurança.
4. **Ponteiro Inteligente**: Gerencia a vida útil de um objeto e garante o gerenciamento adequado de recursos.
5. **Proxy Virtual para Cacheamento**: Cachea dados para evitar operações caras e melhorar o desempenho.

## Instalação

O Pattern Proxy pode ser implementado em várias linguagens de programação. Veja um exemplo em Python:

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
        # Simule a lógica de controle de acesso
        return True  # Para simplicidade, permitir acesso sempre

# Código do cliente
real_subject = RealSubject()
proxy = Proxy(real_subject)

proxy.operation()
```

### Exemplo Detalhado

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
        # Simule a lógica de controle de acesso
        return self._access_granted

# Código do cliente
real_subject = RealSubject()
proxy = Proxy(real_subject)

# Permitir acesso
proxy._access_granted = True
print(proxy.operation())

# Negar acesso
proxy._access_granted = False
print(proxy.operation())
```

## Uso Básico

1. **Criando o RealSubject**: Este é o objeto real que executa o trabalho real.
2. **Criando o Proxy**: O objeto proxy atua como uma fachada para o objeto real.
3. **Verificação de Acesso**: O proxy verifica se é permitido o acesso ao objeto real.
4. **Delegação de Operações**: Se o acesso for permitido, o proxy delega a operação para o objeto real; caso contrário, nega o acesso.

## Conclusão

O Pattern Proxy é um padrão versátil que ajuda a gerenciar acesso, otimizar desempenho e melhorar a segurança nos sistemas de software. Ao fornecer uma maneira flexível de controlar o acesso a um objeto, o Pattern Proxy pode ser aplicado em uma variedade de cenários, tornando-se uma ferramenta valiosa no kit de ferramentas do desenvolvedor de software.