---
title: Deploys Sem-Downtime
description: Um guia completo sobre a implementação de deploys sem-downtime com estratégias blue/green, canary e rolling.
created: 2026-07-24
tags:
  - DevOps
  - Deploy
  - Sem-Downtime
status: draft
---

# Deploys Sem-Downtime

O deploy sem-downtime é uma prática de engenharia de software que garante que um serviço ou aplicativo permaneça disponível para os usuários durante o processo de implantação. Esta técnica envolve estratégias para minimizar ou eliminar qualquer interrupção na disponibilidade do serviço quando novos códigos ou configurações são lançados. O objetivo é manter a disponibilidade do serviço, mesmo durante atualizações de software ou atividades de manutenção.

## Funcionalidades Principais

1. **Descoberta de Serviços e Balanceamento de Carga:** Utiliza mecanismos como DNS, service mesh ou balanceadores de carga para rotear o tráfego para diferentes instâncias.
2. **Deploy Blue/Green:** Implanta dois ambientes idênticos (blue e green), permitindo que o tráfego seja roteado entre eles sem interrupção.
3. **Lançamento Canary:** Gradualmente libera novas versões para um subset pequeno de usuários para testar problemas antes de liberar para toda a base de usuários.
4. **Atualizações Gradualmente:** Gradualmente atualiza instâncias individuais ou grupos de instâncias para garantir que não haja um único ponto de falha.
5. **Arquitetura de Microserviços:** Descompõe o aplicativo em serviços menores e independentemente implantáveis para garantir que falhas em um serviço não afetem os outros.

## Instalação

A instalação de ferramentas e estratégias de deploy sem-downtime depende do ambiente específico e das tecnologias em uso. Aqui estão alguns passos gerais:

1. **Configuração do Ambiente:**
   - Configure um balanceador de carga ou service mesh para gerenciar o roteamento do tráfego.
   - Configure DNS para descoberta de serviço e failover.

2. **Deploy Blue/Green:**
   - Implante uma nova versão do aplicativo em um novo ambiente.
   - Use o balanceador de carga para rotear o tráfego entre o ambiente antigo e novo.
   - Após a verificação do novo ambiente, troque completamente o tráfego.

3. **Lançamento Canary:**
   - Implante uma nova versão para um subset pequeno de usuários ou uma região específica.
   - Monitore o desempenho e feedback dos usuários.
   - Gradualmente aumente a porcentagem de usuários ou regiões recebendo a nova versão.

4. **Atualizações Gradualmente:**
   - Atualize uma instância por vez ou em lotes.
   - Monitore por problemas e reverta se necessário.
   - Gradualmente escala as instâncias atualizadas.

5. **Microserviços:**
   - Use um service mesh ou ferramenta de orquestração (como o Kubernetes) para gerenciar o deploy de serviços individuais.
   - Garanta que cada serviço possa ser escalado e atualizado independentemente.

## Uso Básico

1. **Planeje o Deploy:**
   - Defina a estratégia (blue/green, canary, rolling).
   - Planeje para problemas potenciais e tenha estratégias de reverter.

2. **Prepare a Nova Implantação:**
   - Construa e teste a nova versão com rigor.
   - Garanta que todas as dependências estejam corretamente configuradas.

3. **Implante a Nova Versão:**
   - Use a estratégia escolhida para implantar a nova versão.
   - Monitore o processo de implantação para problemas.

4. **Verifique e Escalão:**
   - Monitore a nova versão para estabilidade e desempenho.
   - Gradualmente escalone a nova versão e retire a versão antiga.

5. **Documente e Aprenda:**
   - Documente o processo de implantação e lições aprendidas.
   - Continuamente melhore a estratégia de implantação com base na experiência.

### Exemplo: Deploy Blue/Green com Kubernetes

#### Pré-requisitos
- Clúster do Kubernetes com `kubectl` instalado e configurado.
- Dois ambientes identicos: `blue` e `green`.

#### Passo 1: Defina os Arquivos de Manifesto do Deployment

Crie dois arquivos de manifesto de deployment, um para cada ambiente.

**Deploy Blue:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: blue
  template:
    metadata:
      labels:
        app: my-app
        version: blue
    spec:
      containers:
      - name: my-app
        image: my-app:blue
        ports:
        - containerPort: 80
```

**Deploy Green:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: green
  template:
    metadata:
      labels:
        app: my-app
        version: green
    spec:
      containers:
      - name: my-app
        image: my-app:green
        ports:
        - containerPort: 80
```

#### Passo 2: Implante o Ambiente Blue

```bash
kubectl apply -f blue-deployment.yaml
```

#### Passo 3: Crie um Serviço para Balanceamento de Carga

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
```

Aplicar o arquivo de manifesto do serviço:

```bash
kubectl apply -f service.yaml
```

#### Passo 4: Troque o Tráfego para o Ambiente Green

Atualize o serviço para rotear o tráfego para o ambiente green:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
    version: green
```

Aplicar o arquivo de manifesto atualizado:

```bash
kubectl apply -f service.yaml
```

#### Passo 5: Verifique a Implantação

Verifique os pods e o serviço:

```bash
kubectl get pods
kubectl get services
```

Após a verificação, você pode trocar o tráfego de volta para o ambiente blue se necessário.

### Exemplo: Lançamento Canary

#### Pré-requisitos
- Clúster do Kubernetes com `kubectl` instalado e configurado.
- Dois ambientes de deploy: `stable` e `canary`.

#### Passo 1: Defina os Arquivos de Manifesto do Deployment

Crie dois arquivos de manifesto de deployment, um para cada ambiente.

**Deploy Stable:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-stable
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: stable
  template:
    metadata:
      labels:
        app: my-app
        version: stable
    spec:
      containers:
      - name: my-app
        image: my-app:stable
        ports:
        - containerPort: 80
```

**Deploy Canary:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-canary
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: canary
  template:
    metadata:
      labels:
        app: my-app
        version: canary
    spec:
      containers:
      - name: my-app
        image: my-app:canary
        ports:
        - containerPort: 80
```

#### Passo 2: Implante o Ambiente Stable

```bash
kubectl apply -f stable-deployment.yaml
```

#### Passo 3: Crie um Serviço para Balanceamento de Carga

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
```

Aplicar o arquivo de manifesto do serviço:

```bash
kubectl apply -f service.yaml
```

#### Passo 4: Implante o Ambiente Canary

```bash
kubectl apply -f canary-deployment.yaml
```

#### Passo 5: Roteie o Tráfego para o Ambiente Canary

Atualize o serviço para rotear o tráfego para o ambiente canary:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
    version: canary
```

Aplicar o arquivo de manifesto atualizado:

```bash
kubectl apply -f service.yaml
```

#### Passo 6: Verifique a Implantação

Verifique os pods e o serviço:

```bash
kubectl get pods
kubectl get services
```

Após a verificação, você pode gradualmente aumentar o tráfego canary:

```bash
kubectl patch service my-app-service -p '{"spec":{"selector":{"app":"my-app","version":"canary"}}}'
```

Monitore o ambiente canary para problemas e aumente gradualmente o tráfego canary até 100%.

### Conclusão

Deploy sem-downtime é essencial para manter a confiabilidade e disponibilidade de sistemas distribuídos. Ao empregar estratégias eficazes, técnicas de implementação e ferramentas adequadas, organizações podem alcançar atualizações sem interrupções sem prejudicar a experiência do usuário. Este guia fornece uma visão abrangente sobre as estratégias de deploy blue/green, canary e rolling, juntamente com exemplos práticos usando o Kubernetes.

---