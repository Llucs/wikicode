---
title: Injeção de Segredos sem Incluir Credenciais nos Imagens do Docker
description: Um método para gerenciar e injetar segredos nos imagens de contêiner sem incorporá-los diretamente, garantindo uma melhor segurança e conformidade nos fluxos de implantação.
created: 2026-07-04
tags:
  - DevOps
  - Docker
  - Kubernetes
  - Segurança
  - Gerenciamento de Segredos
status: rascunho
---

# Injeção de Segredos sem Incluir Credenciais nos Imagens do Docker

Injeção de segredos refere-se ao processo de gerenciar e injetar dados sensíveis em aplicativos contêinerizados em tempo de execução. Isso é alcançado sem incorporar credenciais ou segredos diretamente nas imagens do Docker, mas fornecendo-os em tempo de execução ou durante a fase de implantação.

## Recursos Principais

1. **Segurança em Tempo de Execução**: Credenciais nunca são incorporadas na imagem, reduzindo o risco de exposição durante a análise de imagem ou o vazamento devido a vulnerabilidades.
2. **Flexibilidade**: Permite atualizações fáceis de segredos sem a necessidade de重构后的翻译内容如下：

---
title: Injeção de Segredos sem Incluir Credenciais nos Imagens do Docker
description: Um método para gerenciar e injetar segredos nos imagens de contêiner sem incorporá-los diretamente, garantindo uma melhor segurança e conformidade nos fluxos de implantação.
created: 2026-07-04
tags:
  - DevOps
  - Docker
  - Kubernetes
  - Segurança
  - Gerenciamento de Segredos
status: rascunho
---

# Injeção de Segredos sem Incluir Credenciais nos Imagens do Docker

Injeção de segredos refere-se ao processo de gerenciar e injetar dados sensíveis em aplicativos contêinerizados em tempo de execução. Isso é realizado sem incorporar credenciais ou segredos diretamente nas imagens do Docker, mas fornecendo-os em tempo de execução ou durante a fase de implantação.

## Recursos Principais

1. **Segurança em Tempo de Execução**: Credenciais nunca são incorporadas na imagem, reduzindo o risco de exposição durante a análise de imagem ou o vazamento devido a vulnerabilidades.
2. **Flexibilidade**: Permite atualizações fáceis de segredos sem a necessidade de rebuildar e redeployar a imagem.
3. **Escala**: Facilita o gerenciamento seguro de segredos em ambientes multicontoêiner e microserviços.
4. **Conformidade**: Auxilia as organizações a aderirem a padrões regulatórios e melhores práticas para segurança e conformidade de dados.

## Casos de Uso

1. **Credenciais de Banco de Dados**: Gerenciamento seguro de nomes de usuário e senhas de bancos de dados.
2. **Chaves de API**: Armazenamento seguro e injeção de chaves de API para serviços diversos.
3. **Gerenciamento de Configuração**: Injeção de configurações que não fazem parte do código fonte do aplicativo.
4. **Chaves de Encriptação**: Gerenciamento de chaves de encriptação para proteção de dados em repouso ou em trânsito.

## Instalação

O processo de instalação varia dependendo da ferramenta ou solução específica de gerenciamento de segredos utilizada. Aqui estão passos gerais para algumas soluções comuns:

### Segredos do Kubernetes

1. **Pré-requisitos**: Cluster do Kubernetes.
2. **Instalação**: Não é necessário uma instalação explícita; os segredos são uma funcionalidade embutida do Kubernetes.
3. **Passos**:
   1. Crie um segredo usando `kubectl` ou uma interface do painel do Kubernetes.
   2. Refira o segredo em seu arquivo YAML de implantação ou manifesto do Kubernetes.
   3. Monte o segredo como um volume ou use-o como uma variável de ambiente nos pods.

```yaml
# Exemplo YAML para referenciar um segredo
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app-image
        env:
          - name: MY_SECRET_KEY
            valueFrom:
              secretKeyRef:
                name: my-secret
                key: my-key
```

### Segredos do Docker

1. **Pré-requisitos**: Docker Swarm.
2. **Instalação**: Não é necessário uma instalação explícita; o Docker Swarm suporta segredos de fábrica.
3. **Passos**:
   1. Crie um segredo do Docker usando o comando `docker swarm secret create`.
   2. Refira o segredo em sua definição de serviço.

```bash
# Crie um segredo do Docker
docker swarm secret create my-secret my-value

# Refira o segredo em uma definição de serviço
services:
  my-service:
    secrets:
      - my-secret
    command: ["--my-key=$(MY_SECRET_KEY)"]
```

### HashiCorp Vault

1. **Pré-requisitos**: Servidor HashiCorp Vault.
2. **Instalação**: Baixe e instale o HashiCorp Vault em seu servidor ou use um serviço gerenciado.
3. **Passos**:
   1. Inicialize e descongele o Vault.
   2. Crie e armazene segredos no Vault.
   3. Use a API do Vault para recuperar segredos em tempo de execução.

```bash
# Inicialize e descongele o Vault
vault operator init
vault unseal <chave-descongelamento>

# Crie e armazene um segredo
vault kv put secret/my-secret key=my-value

# Recuperar o segredo usando a API do Vault
vault read secret/my-secret
```

## Uso Básico

### Criação de um Segredo

1. **Kubernetes**: `kubectl create secret generic my-secret --from-literal=my-key=my-value`
2. **Docker Swarm**: `docker swarm secret create my-secret my-value`
3. **HashiCorp Vault**: `vault kv put secret/my-secret key=my-value`

### Referenciando o Segredo

1. **Kubernetes**:
   ```yaml
   spec:
     containers:
     - name: my-app
       image: my-app-image
       env:
         - name: MY_SECRET_KEY
           valueFrom:
             secretKeyRef:
               name: my-secret
               key: my-key
   ```

2. **Docker Swarm**:
   ```yaml
   services:
     my-service:
       secrets:
         - my-secret
       command: ["--my-key=$(MY_SECRET_KEY)"]
   ```

3. **HashiCorp Vault**:
   - Os segredos podem ser recuperados via a API do Vault ou usando o comando `vault read`.

Adotando práticas de injeção de segredos, organizações podem aumentar significativamente a postura de segurança de seus aplicativos contêinerizados, garantindo que dados sensíveis permaneçam protegidos e gerenciáveis ao longo do ciclo de desenvolvimento e implantação.