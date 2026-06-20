---
title: DBGate
description: DBGate é uma ferramenta de gerenciamento de banco de dados open-source, multiplataforma e baseada na web para MySQL, PostgreSQL, SQL Server, MongoDB, SQLite e mais, oferecendo uma interface moderna para administração e desenvolvimento de banco de dados.
created: 2026-06-20
tags:
  - database
  - open-source
  - web-based
  - tool
  - management
status: draft
---

# DBGate

DBGate é uma ferramenta de gerenciamento de banco de dados open-source (MIT), baseada na web, projetada como uma alternativa moderna para ferramentas clássicas como phpMyAdmin, Adminer, DBeaver ou DataGrip. Construída com um backend Node.js/Express e um frontend React, ela fornece uma interface de usuário limpa e contemporânea que roda inteiramente em um navegador web, tornando-a multiplataforma e ideal para ambientes cloud, servidor e conteinerizados.

## Por que DBGate?

Os clientes tradicionais de banco de dados geralmente exigem instalação no sistema operacional, levando à fragmentação entre equipes e ambientes. O DBGate resolve isso sendo inteiramente baseado em navegador, permitindo que você:

- **Gerenciar bancos de dados remotamente** sem precisar de túneis SSH ou clientes nativos.
- **Integrar-se a pilhas Docker** para acesso instantâneo a bancos de dados de desenvolvimento.
- **Compartilhar conexões e scripts** por meio de uma instância centralizada (com autenticação).
- **Trabalhar perfeitamente entre Windows, macOS e Linux** usando a mesma interface web.

## Principais Recursos

| Recurso                     | Descrição                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| Suporte a Múltiplos Bancos  | Conecte-se simultaneamente a MySQL, MariaDB, PostgreSQL, SQL Server, MongoDB, SQLite, CockroachDB, Amazon Redshift e Redis. |
| Editor SQL Avançado         | Realce de sintaxe, preenchimento automático inteligente, consultas em várias abas e histórico abrangente de consultas. |
| Navegador de Esquema/Dados  | Navegue, crie, altere e exclua objetos de banco de dados. Edição inline de dados com classificação e filtragem poderosas. |
| Diagramas ER                | Gere automaticamente diagramas Entidade-Relacionamento para visualizar esquemas de banco de dados. |
| Exportar/Importar           | Exporte para CSV, JSON, SQL, Markdown, Excel; importe de arquivos CSV e SQL. |
| Navegação por Chave Estrangeira | Aprofunde-se diretamente em registros relacionados a partir do navegador de dados. |
| Monitoramento do Servidor   | Visualize processos ativos, status do servidor e configurações de variáveis. |
| Otimizado para Docker       | Imagem oficial do Docker para implantação fácil em qualquer servidor. |
| Aplicativo Desktop          | Versão Electron empacotada para uso independente no Windows, macOS e Linux. |

## Instalação

O DBGate pode ser instalado e executado de várias maneiras:

### 1. Docker (Recomendado para Servidor)

```bash
docker run -d -p 3000:3000 --name dbgate dbgate/dbgate
```

Em seguida, acesse `http://localhost:3000`.

Para uma configuração `docker-compose.yml`:

```yaml
version: '3'
services:
  dbgate:
    image: dbgate/dbgate
    ports:
      - "3000:3000"
    restart: unless-stopped
```

### 2. Node Package Manager (NPM)

```bash
npm install -g dbgate
dbgate
```

Acesse via `http://localhost:3000`.

### 3. Instalador Desktop

Baixe os instaladores pré-construídos para Windows, macOS e Linux na [página de releases do GitHub](https://github.com/dbgate/dbgate/releases).

### 4. Implantações em Nuvem

Opções de implantação com um clique estão disponíveis para Heroku, Railway e plataformas similares.

## Início Rápido / Uso

### 1. Iniciar o DBGate

Navegue para `http://localhost:3000` no seu navegador.

### 2. Adicionar uma Conexão

Clique no ícone **+** ao lado de **Conexões**. Escolha seu mecanismo de banco de dados (ex.: PostgreSQL) e insira as credenciais de conexão: Host, Porta, Nome de Usuário, Senha, Banco de Dados.

### 3. Navegar pelos Dados

Clique na conexão salva para ver uma árvore de bancos de dados/tabelas. Clique em uma tabela para visualizar suas linhas.

### 4. Consultar o Banco de Dados

Clique no botão **Consulta** para abrir o editor SQL. Escreva seu SQL e pressione **Executar** (ou `Ctrl+Enter`).

### 5. Visualizar Esquema

Clique com o botão direito em um banco de dados ou tabela e selecione **Diagrama ER** para gerar um esquema visual.

### 6. Exportar Dados

Clique com o botão direito em uma tabela ou conjunto de resultados e selecione **Exportar** para baixar os dados no formato desejado (CSV, JSON, SQL, etc.).

## Exemplos de Comandos

**Iniciar o DBGate com o Docker e persistir dados:**

```bash
docker run -d \
  -p 3000:3000 \
  -v dbgate-data:/home/app/.dbgate \
  --name dbgate \
  dbgate/dbgate
```

**Usar com uma instância local do PostgreSQL em uma pilha de desenvolvimento:**

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: example
  dbgate:
    image: dbgate/dbgate
    ports:
      - "3000:3000"
    depends_on:
      - postgres
```

**Instalar e executar usando npm:**

```bash
npm install -g dbgate
dbgate
```

**Conectar usando variáveis de ambiente (avançado):**

```bash
docker run -d \
  -e DBGATE_SERVER_NAME=myPostgres \
  -e DBGATE_SERVER_TYPE=postgres \
  -e DBGATE_SERVER_HOST=192.168.1.100 \
  -e DBGATE_SERVER_PORT=5432 \
  -e DBGATE_SERVER_USER=admin \
  -e DBGATE_SERVER_PASSWORD=secret \
  -p 3000:3000 \
  dbgate/dbgate
```

## Casos de Uso

1. **Administração Remota de Servidor** – Gerencie bancos de dados em uma VPS ou instância cloud sem túnel SSH ou instalação de clientes nativos.
2. **Ambientes de Desenvolvimento** – Inclua o DBGate em uma pilha `docker-compose.yml` para dar aos desenvolvedores acesso instantâneo via GUI aos seus bancos de dados locais.
3. **Ferramentas de Equipe** – Implante uma instância centralizada do DBGate (com autenticação adequada) para que uma equipe compartilhe acesso a bancos de dados de desenvolvimento ou homologação.
4. **Educação e Treinamento** – Forneça rapidamente aos alunos uma interface SQL sem gerenciar instalações de clientes.
5. **Fluxos de Trabalho Multiplataforma** – Alterne perfeitamente entre sistemas operacionais usando a mesma interface web.

## Arquitetura

O DBGate consiste em:

- **Backend:** Servidor Node.js/Express que gerencia conexões de banco de dados, execução de consultas e endpoints de API.
- **Frontend:** SPA baseada em React que fornece a interface do usuário, incluindo o editor SQL, navegador de dados e visualizador de esquemas.
- **Database Drivers:** Suporta vários mecanismos de banco de dados por meio de drivers nativos do Node.js ou pontes ODBC/JDBC.

A aplicação armazena conexões, scripts SQL e outros objetos no armazenamento local (ou armazenamento em nuvem opcional para a versão hospedada). A imagem Docker agrupa todas as dependências para uma implantação em porta única.

## Limitações

- **Recursos Avançados de IDE:** Pode faltar alguns recursos encontrados no IntelliJ DataGrip (ex.: refatoração distribuída, análise avançada de código).
- **Desempenho:** Renderizar conjuntos de dados muito grandes (>100k linhas) no navegador pode ser mais lento do que aplicativos nativos. As operações de exportação são tratadas no lado do servidor para melhor desempenho.
- **Autenticação:** A versão open-source não inclui autenticação de usuário integrada; você deve colocá-la atrás de um proxy reverso (como nginx + auth_basic) para uso em equipe.

## Resumo

O DBGate é uma ferramenta de gerenciamento de banco de dados poderosa, flexível e open-source que preenche a lacuna entre clientes web leves (como phpMyAdmin) e IDEs nativas pesadas (como DataGrip). Sua natureza multiplataforma, design amigável a contêineres e conjunto de recursos em crescimento o tornam uma excelente escolha para desenvolvedores, DBAs e equipes que buscam um cliente de banco de dados moderno e nativo da web.

---

*Documento gerado em 2026-06-20. Visite o [repositório oficial](https://github.com/dbgate/dbgate) para as atualizações mais recentes.*