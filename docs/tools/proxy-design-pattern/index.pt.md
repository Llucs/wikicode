---
title: Pattern Proxy
description: Uma padrão estrutural que permite que um proxy, ou substituto, controle o acesso a outro objeto, frequentemente com o propósito de adicionar funcionalidade.
created: 2026-07-06
tags:
  - padrões-de-diregin
  - diregin-orientado-a-objetos
  - padrões-estruturais
status: rascunho
---

# Pattern Proxy

## O Que é o Pattern Proxy?

O Pattern Proxy é um padrão estrutural que fornece um substituto ou substituto para outro objeto para controlar o acesso a ele. Permite adicionar responsabilidades ao objeto original sem modificar sua estrutura. O principal objetivo do padrão Proxy é fornecer um substituto ou substituto para outro objeto. Esse padrão é amplamente utilizado em várias aplicações para gerenciar o acesso a recursos, controlar o acesso a dados sensíveis e otimizar o desempenho.

## Características Principais

1. **Objetos Proxy**: São objetos que atuam como um substituto ou substituto para um objeto real. Eles podem realizar tarefas antes ou depois do objeto real.
2. **Acesso Controlado**: Proxies podem controlar o acesso ao objeto real, permitindo ações adicionais antes ou depois dos métodos do objeto real serem chamados.
3. **Decupagem**: Proxies decupam o cliente do objeto real, fornecendo uma camada de abstração.
4. **Flexibilidade**: Proxies podem ser utilizados em diversas situações, como objetos remotos, controle de acesso a recursos e cache.

## História

O Pattern Proxy foi formalizado no livro "Design Patterns: Elements of Reusable Object-Oriented Software", de Erich Gamma, Richard Helm, Ralph Johnson e John Vlissides, comumente conhecido como o Grupo das Quatro (GoF). O padrão foi introduzido como uma maneira de fornecer acesso controlado a objetos e gerenciar a vida útil de objetos.

## Casos de Uso

1. **Proxy Remoto**: Permite que um objeto local aguente como proxy para um objeto em um espaço de endereçamento diferente.
2. **Proxy Virtual**: Utilizado para fornecer um proxy de baixo custo para a criação de um objeto caro.
3. **Proxy de Proteção**: Controla o acesso a um objeto sensível. Por exemplo, um proxy poderia ser usado para controlar o acesso a um arquivo ou banco de dados.
4. **Proxy Inteligente**: Fornece uma maneira de gerenciar o estado de um objeto. Por exemplo, um proxy poderia ser usado para garantir que um objeto esteja em um estado válido antes de ser acessado.
5. **Cache Virtual**: Usa um proxy para armazenar os resultados de uma operação caro.

## Instalação

Como o Pattern Proxy é um padrão e não uma biblioteca ou software, não é necessário instalá-lo. No entanto, para implementar o padrão em uma linguagem de programação específica, você precisaria incluir as classes ou módulos necessárias e seguir as diretrizes do padrão.

## Uso Básico

Aqui está um exemplo simples de implementação do pattern proxy em Python:

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

# Uso
proxy = Proxy()
print(proxy.operation())
```

Em esse exemplo:
- `RealSubject` é a classe que o proxy controla o acesso.
- `Proxy` é a classe que fornece o acesso controlado ao `RealSubject`.
- O `Proxy` verifica se `real_subject` é `None`. Se for, ele cria uma instância de `RealSubject`. Se não for, ele simplesmente chama o método `operation` do `RealSubject`.

## Conclusão

O Pattern Proxy é uma ferramenta poderosa no conjunto de ferramentas do desenvolvedor de software. Fornece um modo de controlar o acesso a objetos, gerenciar recursos e otimizar o desempenho. Com o entendimento de suas características principais e casos de uso, os desenvolvedores podem implementá-lo efetivamente em diversas situações.