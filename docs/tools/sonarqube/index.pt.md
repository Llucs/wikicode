---
title: SonarQube
description: Uma ferramenta de análise de qualidade e segurança de código que se integra a pipelines CI/CD para automatizar revisões de código e capturar vulnerabilidades.
created: 2026-06-16
tags:
  - code-quality
  - security
  - static-analysis
  - ci-cd
  - sonarqube
status: draft
---

# SonarQube

## O que é o SonarQube?

SonarQube é uma plataforma open-source da SonarSource para inspeção contínua de qualidade e segurança de código. Ela realiza Testes de Segurança Estáticos de Aplicação (SAST) no código-fonte para detectar **Bugs**, **Vulnerabilidades**, **Code Smells** e **Duplicações** em mais de 30 linguagens de programação, incluindo Java, C#, JavaScript, TypeScript, Python, Go, entre outras. SonarQube atua como um hub central de qualidade nos fluxos de trabalho de desenvolvimento, aplicando políticas customizáveis (Quality Gates) para evitar que código problemático seja liberado.

## Por que usar o SonarQube?

- **Capturar Problemas Cedo** – Integre-se em pipelines de CI/CD para revisar automaticamente cada commit e pull request.
- **Aplicar Padrões de Qualidade** – Defina Quality Gates que devem ser atendidos (ex.: nenhum novo bug, limite de cobertura) antes que um build possa ser bem-sucedido.
- **Reduzir Dívida Técnica** – Quantifique o esforço necessário para corrigir problemas existentes e acompanhe melhorias ao longo do tempo.
- **Melhorar a Segurança** – Identifique vulnerabilidades do OWASP Top 10 e CWE e sinalize hotspots de segurança para revisão manual.
- **Automatizar Revisões de Código** – Transfira a detecção de problemas simples (formatação, ponteiros nulos, vazamentos de recursos) dos revisores humanos para que possam se concentrar na arquitetura e lógica.

## Recursos Principais

### Análise Estática de Código
SonarQube escaneia o código-fonte em busca de problemas de confiabilidade, segurança e manutenibilidade. Ele executa análises avançadas de fluxo de dados e fluxo de controle para detectar:
- Possíveis desreferências de ponteiro nulo
- Vazamentos de recursos
- Vulnerabilidades de injeção SQL e cross-site scripting (XSS)
- Credenciais codificadas

### Quality Gates
Um Quality Gate é um conjunto de condições booleanas sobre métricas (ex.: `New Coverage < 80%`, `New Bugs > 0`) que devem ser atendidas para que um projeto seja aprovado. O SonarQube vem com um gate padrão, e você pode criar gates personalizados para atender às políticas da sua equipe.

### Security Hotspots
SonarQube destaca código que requer revisão manual de segurança. Esses hotspots não são automaticamente confirmados como vulnerabilidades, mas são áreas onde um invasor poderia potencialmente injetar entrada maliciosa. Os desenvolvedores podem revisá-los e marcá-los como "Safe" ou "Needs Review".

### Medição de Dívida Técnica
SonarQube traduz problemas em uma métrica de **Dívida Técnica**, expressa em dias ou custo (ex.: USD). Isso ajuda as equipes a orçar e priorizar refatorações.

### Análise de Branch e Pull Request
SonarQube pode analisar branches de funcionalidade e pull requests, permitindo que você aplique Quality Gates apenas em código novo. Isso se encaixa naturalmente em um fluxo de trabalho **Clean as You Code**, onde o foco está no diff em vez de todo o código-base.

### Integrações DevOps
SonarQube integra-se nativamente com:
- **GitHub, GitLab, Bitbucket** – Decoração de pull requests, comentários inline.
- **Jenkins, Azure DevOps, Travis CI, CircleCI** – Integração com pipeline de build.
- **Maven, Gradle, .NET, SonarScanner CLI** – Invocação da varredura.

### Extensão SonarLint para IDE
SonarLint (para VS Code, IntelliJ, Eclipse, Visual Studio) se conecta a um servidor SonarQube e aplica as mesmas regras localmente, fornecendo feedback em tempo real enquanto você digita.

---

## Instalação

SonarQube requer **Java 17+** e um banco de dados dedicado (PostgreSQL recomendado para produção). Ele é executado como uma aplicação web independente.

### Docker (início rápido para avaliação)

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:postgresql://host:port/sonarqube \
  -e SONAR_JDBC_USERNAME=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:community
```

> **Nota:** A edição Community não inclui recursos avançados como análise de branch ou decoração de pull requests. Para isso, considere a edição Developer ou superior.

### Instalação Manual (Linux / macOS)

1. Baixe a versão mais recente em [SonarSource Download](https://www.sonarsource.com/products/sonarqube/downloads/).
2. Extraia o arquivo.
3. Configure a conexão com o banco de dados em `conf/sonar.properties`:
   ```properties
   sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube
   sonar.jdbc.username=sonar
   sonar.jdbc.password=sonar
   ```
4. Inicie o servidor:
   ```bash
   # Linux/macOS
   bin/linux-x86-64/sonar.sh start
   # Windows
   bin/windows-x86-64/StartSonar.bat
   ```
5. Acesse a interface web em `http://localhost:9000`. Credenciais padrão: `admin` / `admin`.

---

## Uso Básico

### 1. Configurar um Projeto

Faça login no SonarQube, clique em **Create new project**, dê uma chave ao projeto e escolha um Quality Profile e um Quality Gate. Em seguida, gere um **Project Token** (ex.: `sqa_xxxx`). Esse token autentica o scanner.

### 2. Executar uma Varredura

#### Usando Maven

```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=my-project \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

#### Usando Gradle

```groovy
// build.gradle
plugins {
    id "org.sonarqube" version "4.4.1.3373"
}

sonar {
    properties {
        property "sonar.projectKey", "my-project"
        property "sonar.host.url", "http://localhost:9000"
        property "sonar.token", "sqa_xxxx"
    }
}
```

```bash
./gradlew sonarqube
```

#### Usando SonarScanner CLI

Instale o SonarScanner (baixe do SonarSource), então:

```bash
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

### 3. Revisar Resultados

Após a conclusão da varredura, o painel do SonarQube mostra:
- **Status do Quality Gate** – Aprovado ou Reprovado.
- **Issues** – Agrupadas por severidade (Blocker, Critical, Major, Minor, Info) e tipo (Bug, Vulnerability, Code Smell).
- **Security Hotspots** – Áreas de código que precisam de revisão manual.
- **Cobertura** – Se você tem uma ferramenta como JaCoCo ou dotCover, importe relatórios de cobertura.
- **Duplicações** – Blocos duplicados destacados.

---

## Integração com CI/CD

### GitHub Actions

```yaml
name: SonarQube Scan
on: [push]
jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@v1.9.0
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    environment {
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_AUTH_TOKEN = credentials('sonarqube-token')
    }
    stages {
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube Server') {
                    sh 'mvn clean verify sonar:sonar'
                }
            }
        }
    }
}
```

### GitLab CI/CD

```yaml
variables:
  SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"
  GIT_DEPTH: "0"

sonarqube-check:
  image: maven:3.8.6-openjdk-17
  script:
    - mvn clean verify sonar:sonar
      -Dsonar.projectKey=$CI_PROJECT_ID
      -Dsonar.host.url=$SONAR_HOST_URL
      -Dsonar.token=$SONAR_TOKEN
      -Dsonar.branch.name=$CI_COMMIT_REF_NAME
```

---

## Metodologia Clean as You Code

SonarQube incentiva uma abordagem **Clean as You Code**: em vez de tentar corrigir todos os problemas existentes, concentre-se em evitar novos no código que você escreve hoje. Isso se reflete em:

- **Foco em Código Novo** – Métricas e Quality Gates têm como alvo o código novo/modificado.
- **Decoração de Pull Request** – As issues são relatadas diretamente nos diffs do PR (GitHub, GitLab, Bitbucket).
- **SonarLint** – Desenvolvedores capturam issues em suas IDEs antes de commitar.

Isso reduz o atrito e torna a melhoria da qualidade sustentável.

---

## Conclusão

SonarQube é uma ferramenta madura e amplamente adotada para análise estática e governança de qualidade. Ao integrá-la em seu pipeline de desenvolvimento, você pode automatizar revisões de código, aplicar padrões de segurança e gerenciar dívida técnica — resultando em software mais confiável e seguro.

Para recursos avançados (análise de branch, gerenciamento de portfólio, cobertura específica de linguagem), considere atualizar para as edições **Developer**, **Enterprise** ou **Data Center** do SonarQube Server, ou use o **SonarQube Cloud** hospedado na nuvem (antigo SonarCloud).