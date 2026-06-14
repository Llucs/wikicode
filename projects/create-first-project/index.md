---
title: CLI Grep Tool em Rust
description: Uma reimplementação simples do grep em Rust para aprendizado da linguagem.
created: 2026-06-14
tags:
  - project
  - rust
  - cli
status: draft
---

# CLI Grep Tool em Rust

## Sobre

Uma ferramenta de busca em arquivos no estilo `grep`, escrita em Rust, para demonstrar conceitos como iteradores, tratamento de erros e I/O.

## Stack

- **Linguagem:** Rust
- **Dependências:** apenas a biblioteca padrão

## Código

### src/main.rs

```rust
use std::env;
use std::fs;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        eprintln!("Usage: {} <pattern> <file>", args[0]);
        process::exit(1);
    }

    let pattern = &args[1];
    let filename = &args[2];

    let content = fs::read_to_string(filename).unwrap_or_else(|err| {
        eprintln!("Error reading file: {}", err);
        process::exit(1);
    });

    for (i, line) in content.lines().enumerate() {
        if line.contains(pattern) {
            println!("{}: {}", i + 1, line);
        }
    }
}
```

### src/lib.rs

```rust
pub fn search<'a>(pattern: &str, content: &'a str) -> Vec<&'a str> {
    content
        .lines()
        .filter(|line| line.contains(pattern))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn finds_match() {
        let result = search("duct", "Rust:\nsafe, fast, productive.");
        assert_eq!(result.len(), 1);
    }

    #[test]
    fn no_match() {
        let result = search("xyz", "hello world");
        assert_eq!(result.len(), 0);
    }
}
```

## Setup

```bash
cd projects/create-first-project
rustc src/main.rs -o greptool
./greptool palavra arquivo.txt
```

## Testes

```bash
rustc --test src/lib.rs -o run_tests && ./run_tests
```
