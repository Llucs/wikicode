---
title: DBeaver Community
description: Uma ferramenta gratuita e de código aberto recomendada para projetos pessoais. Gerencie e explore bancos de dados SQL como MySQL, MariaDB, PostgreSQL, SQLite, Família Apache e outros.
created: 2026-07-24
tags:
  - banco de dados
  - sql
  - gerenciamento
  - desenvolvimento
  - ferramenta
status: rascunho
---

# DBeaver Community

DBeaver é uma ferramenta universal de gerenciamento de bancos de dados de código aberto que suporta vários bancos de dados, incluindo SQL Server, MySQL, PostgreSQL, Oracle, SQLite e outros. Foi lançado pela primeira vez em 2013 e desde então se tornou uma escolha popular entre desenvolvedores, DBAs e analistas de dados para gerenciamento, desenvolvimento e administração de bancos de dados.

## Características Principais

1. **Gerenciamento de Banco de Dados**: O DBeaver suporta uma ampla gama de bancos de dados e suas respectivas ferramentas, como editores de consultas SQL, browsers de banco de dados, editores de esquemas e histórico de consultas SQL.
2. **Modelagem e Design de Dados**: O DBeaver permite que os usuários desenhem, gerenciem e modifiquem esquemas de banco de dados através de uma interface gráfica.
3. **Conexão com Banco de Dados**: Pode conectar-se a diversos bancos de dados usando diferentes protocolos e drivers.
4. **Editor de SQL**: O editor de SQL oferece destacamento de sintaxe, compilação de código e um assistente de compilação automática.
5. **Exportação e Importação de Dados**: O DBeaver fornece ferramentas para exportar dados para formatos como CSV, Excel e outros, bem como importar dados desses formatos.
6. **Sincronização de Banco de Dados**: Suporta a sincronização e comparação de esquemas de banco de dados.
7. **Administração de Banco de Dados**: Inclui funcionalidades para gerenciar usuários, papéis, permissões e outras tarefas administrativas.
8. **Interface Gráfica**: A aplicação possui uma interface moderna e intuitiva que suporta temas escuro e claro.
9. **Plugins e Extensões**: Os usuários podem estender a funcionalidade do DBeaver através de plugins, que podem ser instalados da Loja DBeaver.

## Histórico

O DBeaver foi inicialmente desenvolvido por Yvan Volckaert e lançado como um projeto comunitário em 2013. O projeto foi posteriormente adotado e mantido pela Comunidade DBeaver. Em 2017, o projeto foi transformado em uma empresa comercial, a DBeaver GmbH, que continua a apoiar e desenvolver o software.

## Casos de Uso

1. **Desenvolvimento de Banco de Dados**: Desenvolvedores podem usar o DBeaver para escrever, testar e executar consultas SQL, bem como gerenciar esquemas de banco de dados.
2. **Análise de Dados**: Analistas de dados podem usar o DBeaver para consultar e manipular conjuntos de dados grandes, criar e executar consultas SQL complexas e gerar relatórios.
3. **Administração de Banco de Dados**: DBAs podem usar o DBeaver para gerenciar permissões de usuário, papéis e outras tarefas administrativas.
4. ** Migração de Dados**: Os usuários podem usar o DBeaver para migrar dados entre diferentes bancos de dados, especialmente quando o banco de dados de destino tem uma estrutura diferente.

## Instalação

1. **Download**: Visite o site oficial do DBeaver (https://dbeaver.io/) para baixar a última versão do DBeaver.
2. **Instalação**: O processo de instalação é simples. Para Windows, clique duas vezes no instalador e siga as instruções na tela. Para macOS, abra o arquivo `.dmg` e arraste o aplicativo para o folder Aplicativos. Para Linux, execute o arquivo `.deb` ou `.rpm` com o gerenciador de pacotes.
3. **Executar**: Após a instalação, abra o DBeaver do menu de aplicações.

### Exemplo de Comando para Instalador Windows

```sh
sh DBeaver-<version>-win32-installer.exe
```

### Exemplo de Comando para Instalador macOS

```sh
open DBeaver-<version>-macOS.dmg
```

### Exemplo de Comando para Instalador Linux

```sh
sudo dpkg -i DBeaver-<version>.deb
```

ou

```sh
sudo rpm -i DBeaver-<version>.rpm
```

## Uso Básico

1. **Gerenciamento de Conexão**: Abra o DBeaver, clique em "Arquivo" > "Novo" > "Conexão com Banco de Dados", e configure as configurações de conexão do seu banco de dados (servidor, porta, usuário, senha).
2. **Editor de SQL**: Uma vez conectado, use o editor de SQL para escrever, executar e gerenciar consultas SQL.
3. **Navegador de Esquema**: Use o navegador de esquema para explorar a estrutura do banco de dados, navegar pelas tabelas, exibições e outros objetos do banco de dados.
4. **Importação/Exportação de Dados**: Utilize as funcionalidades de importação e exportação para mover dados entre diferentes formatos ou bancos de dados.

## Interface de Linha de Comando (dbvr)

O CLI DBeaver (dbvr) é uma interface de linha de comando para trabalhar com bancos de dados. Pode ser usada como uma aplicação CLI independente ou em conjunto com o DBeaver e o CloudBeaver. Oferece uma maneira scriptável de gerenciar projetos e fontes de dados de banco de dados, inspecionar metadados e executar SQL do terminal.

### Exemplo de Comando para Conectar-se a um Banco de Dados

```sh
dbvr connect --url jdbc:mysql://localhost:3306/mydb --username myuser --password mypassword
```

### Exemplo de Comando para Executar uma Consulta SQL

```sh
dbvr sql -c "SELECT * FROM mytable" -o results.csv
```

## Conclusão

O DBeaver é uma ferramenta poderosa e versátil que oferece uma ampla gama de funcionalidades para gerenciamento e desenvolvimento de bancos de dados. Sua natureza de código aberto e comunidade ativa contribuem para sua robustez e atualizações frequentes, tornando-o uma valiosa ferramenta para profissionais de banco de dados.