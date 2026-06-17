---
title: DBeaver - Ferramenta Universal de Gerenciamento de Banco de Dados
description: Uma ferramenta gratuita, de código aberto e multiplataforma para gerenciamento de banco de dados e cliente SQL para desenvolvedores, DBAs e analistas de dados.
created: 2026-06-17
tags:
  - database
  - sql
  - management
  - tools
  - open-source
status: draft
---

# DBeaver - Ferramenta Universal de Gerenciamento de Banco de Dados

## Visão Geral

DBeaver é uma ferramenta de gerenciamento de banco de dados e cliente SQL **gratuita, de código aberto e multiplataforma**. Ela fornece uma interface gráfica rica para interagir com qualquer banco de dados que suporte drivers JDBC ou ODBC, tornando-se uma ferramenta universal para desenvolvedores, administradores de banco de dados e analistas de dados.

- **Licença**: A Community Edition (CE) é lançada sob **Apache 2.0**; edições comerciais Pro/Enterprise/Team também estão disponíveis.
- **Plataforma**: Windows, macOS, Linux (também disponível como aplicação portátil).
- **Arquitetura**: Construída sobre o Eclipse Rich Client Platform (RCP) usando Java.
- **História**: Iniciado em 2010 por Serge Rielau, um especialista em banco de dados anteriormente envolvido com Apache Derby e Oracle. O projeto rapidamente ganhou ampla adoção, levando à formação da DBeaver Corp.

DBeaver é ideal para:
- **Desenvolvimento de Aplicações** – Escrever, depurar e otimizar consultas SQL.
- **Administração de Banco de Dados** – Gerenciar esquemas, usuários, sessões e índices.
- **Análise de Dados** – Executar consultas analíticas e exportar resultados para vários formatos.
- **Engenharia de Dados** – Transferir dados entre diferentes bancos de dados sem scripts pesados.
- **Educação** – Aprender SQL e conceitos de banco de dados relacionais através de uma GUI intuitiva.

## Principais Recursos

| Recurso | Descrição |
|---------|-------------|
| **Suporte Amplo a Banco de Dados** | Conecta-se a mais de 100 bancos de dados prontos para uso, incluindo MySQL/MariaDB, PostgreSQL, Oracle, SQL Server, SQLite, DB2, Snowflake, Redshift, ClickHouse e muitos outros. |
| **Editor SQL Avançado** | Destaque de sintaxe, conclusão de código, execução de consultas com múltiplas abas de resultados, visualização do plano de execução (gráfico), formatação SQL e consultas parametrizadas. |
| **Navegador de Dados / Planilha** | Edição inline poderosa, filtragem avançada, classificação e manipulação de dados BLOB/CLOB diretamente em uma interface de grade. |
| **Diagramas ER** | Gere automaticamente diagramas Entidade-Relacionamento com engenharia reversa (clique direito em um esquema ou tabela). |
| **Gerenciamento de Esquemas** | Navegador de objetos para navegar, criar e editar tabelas, visões, índices, procedimentos e funções. |
| **Transferência de Dados** | Exportação/importação em massa entre bancos de dados e formatos de arquivo (CSV, JSON, XML, Excel, SQL, Markdown, HTML). |
| **Ferramentas de Administração** | Gerenciador de sessões, agendador de tarefas (Pro), gerenciamento de usuários/papéis e tunelamento SSH/SSL/Proxy integrado. |
| **Extensibilidade** | Arquitetura de plugins; plugin disponível para drivers adicionais, controle de versão (Git) e personalizações de diagramas. |
| **Multiplataforma** | Executa em Windows, macOS e Linux. |

## Instalação

DBeaver está disponível através de vários canais. Escolha o método que se adequa ao seu ambiente.

### Instalador Oficial (Todas as Plataformas)

Baixe o instalador para seu sistema operacional em [dbeaver.io](https://dbeaver.io) (Community Edition) ou [dbeaver.com](https://dbeaver.com) (Enterprise).

### Gerenciadores de Pacotes

**macOS (Homebrew)**
```bash
brew install --cask dbeaver-community
```

**Linux (Snap)**
```bash
sudo snap install dbeaver-ce
```

**Linux (APT / YUM – Repositórios Oficiais Debian/RPM)**
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

**Versão Portátil para Windows**

Um executável portátil está disponível no site oficial, ideal para executar a partir de uma unidade USB sem instalação.

## Primeiros Passos – Uso Básico

### 1. Criar uma Conexão de Banco de Dados

1. Inicie o DBeaver.
2. Clique no botão **Nova Conexão de Banco de Dados** (ícone de plugue) na barra de ferramentas.
3. Selecione o tipo de banco de dados (ex.: **PostgreSQL**).
4. Preencha os detalhes da conexão:
   - Host, Porta, Nome do Banco de Dados, Usuário, Senha.
5. Clique em **Testar Conexão**. O DBeaver solicitará automaticamente o download do driver JDBC necessário, se ainda não estiver em cache.
6. Clique em **Concluir**. A conexão aparecerá no painel **Navegador de Banco de Dados**.

![Exemplo do Assistente de Conexão](https://dbeaver.com/docs/images/connection-wizard.png) <!-- URL de placeholder; a documentação real fornece capturas de tela -->

### 2. Navegar e Consultar Dados

- No **Navegador de Banco de Dados**, expanda uma conexão para ver esquemas, tabelas, visões, etc.
- Clique com o botão direito em uma tabela e selecione **Visualizar Dados** para abrir uma grade de dados.
- Para escrever SQL personalizado, pressione `Ctrl + ]` (Windows/Linux) ou `Cmd + ]` (macOS) para abrir um novo **Editor SQL**.

**Exemplo de consulta SQL:**
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

- Execute a consulta com `Ctrl + Enter` (Win/Lin) ou `Cmd + Enter` (macOS).
- Os resultados aparecem na grade de resultados abaixo do editor.

### 3. Editar e Exportar Dados

- Clique diretamente no valor de uma célula na grade de resultados para editá-lo (requer permissão **Editar** na tabela).
- Clique com o botão direito na grade de resultados e escolha **Exportar Dados**.
- Selecione o formato desejado (CSV, Excel, JSON, SQL INSERT, XML, Markdown, etc.) e configure as opções.

## Uso Avançado

### Diagramas Entidade‑Relacionamento (ER)

DBeaver pode gerar diagramas ER para um esquema ou tabelas específicas.

1. Clique com o botão direito em um esquema no Navegador de Banco de Dados.
2. Selecione **Visualizar Diagrama** (ou abra a guia **Diagrama ER**).
3. O diagrama exibe tabelas, colunas, relacionamentos e índices.
4. Você pode reorganizar elementos, exportar o diagrama como imagem ou imprimi-lo.

### Transferência / Migração de Dados

Use o assistente **Transferir Dados** para copiar dados entre bancos de dados ou extrair dados para arquivos.

1. Clique com o botão direito em uma tabela ou esquema.
2. Selecione **Dados > Transferir Dados**.
3. Escolha a origem (ex.: uma tabela) e o destino (outra conexão de banco de dados ou arquivo).
4. Configure os mapeamentos de colunas e regras de transformação.
5. Execute a transferência.

### Plano de Execução (EXPLAIN)

Visualize o plano de execução da consulta para ajuste de SQL.

1. No Editor SQL, escreva uma consulta.
2. Clique no botão **Explicar Plano** (ou clique com o botão direito → **Explicar Plano**).
3. O DBeaver mostra um plano gráfico com detalhes de custo e uso de índice.

### Ferramenta de Comparação (Pro/Enterprise)

As ferramentas **Comparar Estrutura** e **Comparar Dados** permitem comparar esquemas ou dados entre dois bancos de dados ou ambientes.

- Disponível nas edições comerciais.

## Configuração e Personalização

### Configurações de Conexão

- **Propriedades do Driver**: Modifique atributos do driver JDBC (ex.: timeouts, modo SSL, tamanhos de bloco) no editor de conexão.
- **Túnel SSH**: Configure o tunelamento SSH para acesso seguro a bancos de dados remotos (na guia **SSH** das configurações de conexão).
- **SSL**: Habilite SSL e importe certificados através da guia **SSL**.

### Preferências Globais

- `Janela → Preferências` (Windows/Linux) ou `DBeaver → Preferências` (macOS).
- **Aparência**: Alterne entre temas claro/escuro, ajuste tamanhos de fonte.
- **Editores**: Configure o estilo de formatação SQL, comportamento de auto‑completar e opções de execução.
- **Conexões**: Defina níveis de isolamento de transação padrão, auto‑commit e timeouts de inatividade.

### Gerenciamento de Drivers

- **Gerenciador de Drivers**: `Banco de Dados → Gerenciador de Drivers`. Visualize, edite ou adicione drivers JDBC personalizados.
- Baixe drivers ausentes diretamente do repositório de drivers do DBeaver ao conectar-se a um banco de dados pela primeira vez.

## Automação e Scripts

### DBeaver CLI (Apenas Pro/Enterprise)

O DBeaver Pro/Enterprise inclui uma ferramenta de linha de comando (`dbeaver-cli`) para executar scripts SQL, exportar dados ou executar tarefas sem GUI.

```bash
# Connect and run a script against a PostgreSQL instance
dbeaver-cli -driver postgresql -url jdbc:postgresql://localhost:5432/mydb \
            -user myuser -password mypass -script query.sql
```

### Agendador de Tarefas (Pro/Enterprise)

Agende exportações recorrentes, transferências de dados ou scripts SQL usando o agendador integrado (interface semelhante ao cron).

## Integrações

- **Controle de Versão**: Plugin de integração com Git (disponível na Community) – commit de scripts SQL ou comparação com versões comitadas.
- **Docker**: Executar o DBeaver diretamente em um contêiner para pipelines CI/CD é possível com a edição CLI.
- **Bancos de Dados na Nuvem**: Drivers pré‑configurados para Snowflake, Amazon Redshift, Google BigQuery, Azure SQL, etc.
- **SSH/SSL**: Suporte integrado para conexões seguras e autenticação por proxy.

## Compatibilidade e Desempenho

| Aspecto | Detalhes |
|--------|---------|
| **Sistemas Operacionais Suportados** | Windows 10+, macOS 10.15+, Linux (x64, amd64, aarch64) |
| **Requisitos Java** | JDK 11 ou posterior (incluído nos instaladores) |
| **Suporte a Banco de Dados** | Mais de 100 bancos de dados via JDBC/ODBC (incluindo relacionais, NoSQL-like, na nuvem) |
| **Dicas de Desempenho** | - Use índices para consultas grandes.<br>- Feche conexões ociosas nas preferências.<br>- Ative **“Usar atualizações em lote”** para operações em massa.<br>- Para conjuntos de dados extremamente grandes, exporte em partes ou use ferramentas de migração dedicadas. |

## Solução de Problemas e FAQ

### Problemas Comuns

1. **“Driver não encontrado” / “Não é possível conectar”**
   - O DBeaver solicitará o download do driver. Se o download automático falhar, vá em `Banco de Dados → Gerenciador de Drivers`, selecione seu banco de dados e clique em **Baixar/Atualizar**.
   - Certifique-se de ter acesso à internet ou coloque manualmente o arquivo JAR na biblioteca de drivers.

2. **Conexão trava ou excede o tempo limite**
   - Verifique a conectividade de rede e as regras de firewall.
   - Verifique as configurações SSH/SSL; um túnel mal configurado pode bloquear conexões.
   - Aumente o tempo limite de conexão nas propriedades do driver.

3. **O desempenho do Editor SQL está lento**
   - Desative o carregamento automático de metadados: `Preferências → Banco de Dados → Navegador → Desativar leitura preguiçosa de metadados`.
   - Reduza o limite do conjunto de resultados na barra de ferramentas do editor.

4. **BLOB/CLOB não pode ser editado**
   - O DBeaver suporta edição inline para objetos pequenos. Para objetos grandes, use a caixa de diálogo **Visualizar / Editar Valor** (clique com o botão direito na célula → **Visualizar Valor**).

### Perguntas Frequentes

**P: O DBeaver é totalmente gratuito?**
R: A Community Edition é gratuita e de código aberto (Apache 2.0). As edições Pro, Enterprise e Team são comerciais e adicionam recursos como suporte a NoSQL, assistência de IA e uma CLI.

**P: Posso usar o DBeaver para bancos de dados de produção?**
R: Sim, a Community Edition é pronta para produção para tarefas de desenvolvimento e DBA. Para ambientes de missão crítica, considere a edição Enterprise com suporte e auditoria adicionais.

**P: O DBeaver funciona com MongoDB ou outros bancos de dados NoSQL?**
R: A Community Edition tem suporte básico ao MongoDB. Suporte completo a NoSQL e bancos de dados em nuvem (incluindo MongoDB, Cassandra e DynamoDB) está disponível na edição Enterprise.

**P: Como desinstalo completamente o DBeaver?**
R: Use o gerenciador de pacotes do seu sistema (ex.: `brew uninstall --cask dbeaver-community`, `snap remove dbeaver-ce`) ou o desinstalador do SO. As configurações do usuário são armazenadas em `~/.dbeaver` no macOS/Linux ou `%APPDATA%\DBeaver` no Windows; remova esses diretórios para limpar toda a configuração.

## Conclusão

DBeaver é uma ferramenta de banco de dados poderosa, flexível e fácil de usar que se encaixa perfeitamente no fluxo de trabalho de qualquer desenvolvedor. Seu núcleo de código aberto, suporte extensivo a bancos de dados e rico conjunto de recursos fazem dela um utilitário essencial para qualquer pessoa que trabalhe com dados.

Para mais informações, visite a documentação oficial em [dbeaver.com/docs](https://dbeaver.com/docs/) ou contribua com a comunidade no [GitHub](https://github.com/dbeaver/dbeaver).