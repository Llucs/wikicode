---
title: Postman - Plataforma de Desenvolvimento e Testes de API
description: Um guia abrangente sobre o Postman, a plataforma de API padrão da indústria para projetar, construir, testar e documentar APIs.
created: 2026-06-15
tags:
  - postman
  - api-testing
  - api-development
  - collaboration
  - newman
status: draft
ecosystem: api
---

# Postman - Plataforma de Desenvolvimento e Testes de API

## O que é o Postman?

O Postman é uma plataforma de API completa que simplifica cada etapa do ciclo de vida da API – desde o design e desenvolvimento até testes, documentação e monitoramento. Originalmente iniciado como um simples cliente HTTP, evoluiu para um ambiente colaborativo usado por milhões de desenvolvedores e engenheiros de QA em todo o mundo. O Postman suporta os protocolos REST, GraphQL e SOAP, e fornece um rico conjunto de ferramentas para construir e trabalhar com APIs de forma eficiente.

## Por que usar o Postman?

- **Cliente HTTP Abrangente:** Envie facilmente requisições de qualquer método, personalize cabeçalhos, autenticação e conteúdo do corpo.
- **Ferramentas Organizacionais:** Agrupe requisições em Coleções, gerencie variáveis com Ambientes e reutilize dados em todo um workspace.
- **Scripts e Testes:** Escreva scripts de teste em JavaScript para automatizar asserções, extrair dados entre requisições e lidar com fluxos de trabalho dinâmicos.
- **Pronto para Automação:** Use o Collection Runner para execuções manuais ou Newman para execução headless (CI/CD, pipelines).
- **Colaboração:** Compartilhe coleções e ambientes via workspaces na nuvem com controle de versão e comentários.
- **Documentação e Mocking:** Gere automaticamente documentação de API e servidores mock para simular respostas da API antes do backend estar pronto.
- **Monitoramento:** Configure monitores para agendar execuções de coleções e verificar a saúde da API.

## Instalação

### Aplicativo Desktop (Recomendado)

O Postman oferece aplicativos desktop nativos para Windows, macOS e Linux.

- Baixe o instalador apropriado em [getpostman.com](https://getpostman.com)
- Alternativamente, use a **versão web** em [go.postman.co](https://go.postman.co) com o Desktop Agent para lidar com chamadas de API.

### Newman (CLI para CI/CD)

Newman é o executor de coleções em linha de comando para Postman. Ele permite executar e testar uma coleção do Postman diretamente da linha de comando, tornando-o ideal para integrar testes de API no seu pipeline de desenvolvimento.

Instale via npm:

```bash
npm install -g newman
```

Ou com Yarn:

```bash
yarn global add newman
```

## Uso Básico

1. **Criar uma requisição**  
   Clique no botão **New** e escolha **HTTP Request** (ou use `Ctrl+N`).

2. **Especificar a requisição**  
   - Insira a URL (ex.: `https://jsonplaceholder.typicode.com/posts`)  
   - Selecione o método HTTP (`GET`, `POST`, `PUT`, etc.)  
   - Adicione quaisquer cabeçalhos, parâmetros de consulta ou corpo da requisição necessários.

3. **Enviar e inspecionar**  
   Clique em **Send**. O painel de resposta mostra o código de status, tempo de resposta, cabeçalhos e corpo.

4. **Salvar em uma coleção**  
   Clique em **Save** e crie uma nova coleção ou adicione a uma existente.

5. **Adicionar um teste**  
   Na aba **Tests**, escreva um script JavaScript para validar a resposta. Exemplo:

   ```javascript
   pm.test("Response status code is 200", function () {
       pm.response.to.have.status(200);
   });
   ```

   Execute a requisição novamente – o resultado do teste aparece na aba **Test Results**.

## Principais Recursos com Exemplos

### 1. Coleções

As coleções ajudam você a agrupar requisições relacionadas e compartilhá-las com sua equipe. Uma coleção também pode incluir pastas e metadados.

```javascript
// Example of using collection variables in a pre-request script
pm.collectionVariables.set("baseUrl", "https://api.example.com");
```

Execute uma coleção inteira usando o Newman:

```bash
newman run MyCollection.json
```

### 2. Ambientes

Os ambientes contêm pares chave-valor para variáveis que mudam entre configurações (desenvolvimento, staging, produção).

```json
{
  "base_url": "https://dev-api.example.com",
  "api_key": "abc123"
}
```

Use `{{base_url}}` em suas URLs de requisição. Alterne entre ambientes para mudar de contexto instantaneamente.

### 3. Scripts de Pré-requisição e Teste

Os scripts do Postman são escritos em JavaScript e executados em uma sandbox com acesso a objetos fornecidos pelo Postman, como `pm`.

**Script de pré-requisição** (executado antes do envio da requisição):

```javascript
// Dynamically set a timestamp parameter
pm.variables.set("timestamp", Date.now());
```

**Script de teste** (executado após o recebimento da resposta):

```javascript
pm.test("Response time is less than 2000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("Body contains expected user", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData[0].name).to.eql("Leanne Graham");
});
```

### 4. Collection Runner

Execute uma coleção inteira ou uma pasta várias vezes com arquivos de dados.

- Abra **Runner** no canto superior esquerdo do Postman.
- Selecione uma coleção, escolha um ambiente, defina iterações.
- Você pode fornecer um arquivo de dados CSV ou JSON para injetar dados em cada iteração.

### 5. Newman – Integração com Linha de Comando

O Newman permite integrar seus testes do Postman em pipelines de CI/CD (Jenkins, GitLab CI, GitHub Actions, etc.).

**Execute uma coleção com um ambiente e um arquivo de dados:**

```bash
newman run MyCollection.json \
  --environment staging.json \
  --iteration-data test-data.csv \
  --reporters cli,htmlextra
```

O reporter `htmlextra` gera um relatório HTML interativo da execução do teste.

**Uso em um script Node.js:**

```javascript
const newman = require('newman');

newman.run({
    collection: require('./MyCollection.json'),
    environment: require('./staging.json'),
    reporters: 'cli'
}, function (err, summary) {
    if (err) { throw err; }
    console.log('Collection run completed!');
    console.log(summary.run.stats);
});
```

### 6. Geração de Documentação

O Postman pode gerar automaticamente documentação para qualquer coleção. Basta abrir uma coleção, clicar no menu **...** e escolher **View documentation**. A documentação inclui requisições de exemplo, esquemas de requisição/resposta e trechos de código em várias linguagens.

Publique a documentação na web através do botão **Publish Docs**, ou exporte como HTML.

### 7. Servidores Mock

Simule uma API criando um servidor mock a partir da sua coleção. Isso é extremamente útil para o desenvolvimento frontend quando o backend ainda não está pronto.

- Selecione uma coleção, clique em **Mock Servers**.
- O Postman cria uma URL de servidor mock que retorna as respostas de exemplo salvas.

### 8. Monitores

Os monitores permitem agendar execuções periódicas de uma coleção na infraestrutura em nuvem do Postman. Você recebe alertas se algum teste falhar.

- Vá para **Monitors** → **Create a monitor**.
- Selecione uma coleção, defina uma frequência (ex.: a cada hora) e opcionalmente defina alertas (e-mail, Slack, etc.).

## Resumo

O Postman é muito mais do que um cliente de API – é uma plataforma completa que suporta todo o ciclo de vida da API. Desde a simulação inicial e design colaborativo até testes automatizados via Newman e monitoramento em produção, o Postman equipa as equipes com uma única fonte de verdade para suas APIs. Sua facilidade de uso, combinada com scripts poderosos e integração com CI/CD, o torna uma ferramenta indispensável para fluxos de trabalho modernos de desenvolvimento.