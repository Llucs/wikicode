---
title: Pulumi – Infrastructure en tant que code avec des langages généralistes
description: Pulumi est une plateforme open-source d'Infrastructure en tant que code qui permet aux utilisateurs de définir et de gérer des ressources cloud en utilisant des langages de programmation familiers tels que TypeScript, Python, Go et C#.
created: 2026-06-18
tags:
  - infrastructure-as-code
  - cloud
  - devops
  - iac
  - kubernetes
status: draft
---

# Pulumi

Pulumi est une plateforme open-source d'Infrastructure en tant que code (IaC) qui utilise des langages de programmation généralistes pour définir, déployer et gérer des ressources cloud. Au lieu d'apprendre un langage spécifique au domaine (DSL) propriétaire, vous utilisez des langages standard comme TypeScript, Python, Go, C#, Java et YAML. Cette approche apporte des pratiques familières du génie logiciel — boucles, fonctions, classes, tests et gestion de paquets — directement dans le provisionnement de l'infrastructure.

## Pourquoi Pulumi ?

- **Multi-Language & Multi-Cloud** – Gérez les ressources sur AWS, Azure, GCP, Kubernetes et plus de 100 fournisseurs avec le même outil.
- **Expérience développeur** – Utilisez votre langage, IDE, débogueur et frameworks de test préférés.
- **Automation API** – Intégrez les opérations d'infrastructure directement dans le code de l'application ou les pipelines CI/CD sans nécessiter la CLI.
- **Policy as Code** – Appliquez des règles de sécurité, de conformité et de coûts en utilisant TypeScript ou OPA/Rego.
- **Gestion d'état** – Gérez l'état de manière sécurisée via Pulumi Cloud ou des backends autogérés (S3, GCS, Azure Blob). Les secrets sont chiffrés par défaut.
- **Open Source** – Le moteur principal et de nombreux fournisseurs sont sous licence Apache 2.0.

## Installation

### macOS / Linux
```bash
curl -fsSL https://get.pulumi.com | sh
```

### macOS (Homebrew)
```bash
brew install pulumi
```

### Windows (Chocolatey)
```powershell
choco install pulumi
```

Après l'installation, vérifiez la version :
```bash
pulumi version
```

> **Remarque** : Vous devez configurer les identifiants de votre fournisseur cloud (par exemple, `aws configure`) avant de déployer des ressources.

## Démarrage rapide

Créez un nouveau projet en utilisant un modèle (ici AWS avec TypeScript) :

```bash
pulumi new aws-typescript
```

Cela génère un fichier de projet `Pulumi.yaml` et un fichier `index.ts` où vous définissez votre infrastructure. Par exemple, pour créer un bucket S3 :

```typescript
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("my-website-bucket", {
    website: {
        indexDocument: "index.html",
    },
});

export const bucketName = bucket.bucket;
```

Déployez la stack :

```bash
pulumi up
```

Prévisualisez les modifications, puis confirmez. Après le déploiement, visualisez les sorties :

```bash
pulumi stack output bucketName
```

Nettoyez les ressources une fois terminé :

```bash
pulumi destroy
```

## Fonctionnalités clés

### 1. Automation API

L'Automation API encapsule le moteur Pulumi sous forme de bibliothèque, vous permettant de provisionner l'infrastructure par programmation depuis n'importe quelle application sans passer par la CLI.

```typescript
import { LocalWorkspace } from "@pulumi/pulumi/automation";
import * as aws from "@pulumi/aws";

const stack = await LocalWorkspace.createOrSelectStack({
    stackName: "dev",
    projectName: "my-project",
    program: async () => {
        const bucket = new aws.s3.Bucket("automated-bucket");
        return { bucketName: bucket.bucket };
    },
});

await stack.up();
```

### 2. Policy as Code (CrossGuard)

Définissez des politiques qui s'exécutent pendant `pulumi up` pour appliquer la gouvernance. Les politiques sont écrites en TypeScript ou Rego/OPA.

```typescript
import { PolicyPack } from "@pulumi/policy";

const policies = new PolicyPack("aws-policies", {
    policies: [
        {
            name: "s3-no-public-read",
            description: "Interdit l'accès en lecture publique sur les buckets S3.",
            enforcementLevel: "mandatory",
            validateResource: (args, reportViolation) => {
                if (args.type === "aws:s3/bucket:Bucket") {
                    // vérifier acl ou policy
                }
            },
        },
    ],
});
```

Exécutez avec :

```bash
pulumi up --policy-pack ./policy
```

### 3. Gestion d'état

Par défaut, l'état est stocké dans Pulumi Cloud (offre gratuite disponible), ce qui fournit versionnage, collaboration et chiffrement des secrets. Vous pouvez aussi utiliser un backend autogéré :

```bash
pulumi login s3://my-state-bucket
```

Les secrets (par exemple, les mots de passe de base de données) sont automatiquement chiffrés et peuvent être définis avec :

```bash
pulumi config set --secret dbPassword mySecret123
```

### 4. Tests

Pulumi s'intègre avec les frameworks de test standard (Jest, Pytest, etc.). Vous pouvez écrire des tests unitaires avec des ressources simulées, des tests d'intégration sur des stacks éphémères et des tests basés sur les propriétés.

**Exemple : Test unitaire avec Jest**

```typescript
import { describe, it, expect } from "@jest/globals";
import * as pulumi from "@pulumi/pulumi";
import { Mocks, ResourceArgs } from "@pulumi/pulumi/runtime";

pulumi.runtime.setMocks({
    newResource: (type: string, name: string, inputs: any): ResourceArgs => {
        return { id: `${name}`, ...inputs };
    },
    call: (token: string, args: any) => args,
});

it("should create an S3 bucket", async () => {
    const { bucketName } = await import("./index");
    const value = await bucketName.get();
    expect(value).toEqual("my-unique-bucket");
});
```

### 5. Opérateur Kubernetes

L'opérateur Kubernetes Pulumi vous permet de gérer les ressources cloud et Kubernetes nativement depuis votre cluster en utilisant des définitions de ressources personnalisées (CRD).

```yaml
apiVersion: pulumi.com/v1
kind: Stack
metadata:
  name: my-k8s-stack
spec:
  stack: dev
  projectRepo: https://github.com/org/repo
  branch: main
  destroyOnFinalize: true
```

## Exemple : Déploiement d'un bucket S3 (multi-langage)

| Langage      | Extrait clé                                                        |
|---------------|--------------------------------------------------------------------|
| Python        | `bucket = aws.s3.Bucket("my-bucket")`                              |
| Go            | `bucket, err := s3.NewBucket(ctx, "my-bucket", nil)`              |
| C#            | `var bucket = new Aws.S3.Bucket("my-bucket");`                    |
| Java          | `var bucket = new Bucket("my-bucket");`                           |
| YAML          | Utilise le langage de modèle YAML Pulumi.                                |

## Pour en savoir plus

- [Documentation officielle](https://www.pulumi.com/docs/)
- [Dépôt GitHub](https://github.com/pulumi/pulumi)
- [Registre Pulumi](https://www.pulumi.com/registry/)
- [Exemples d'Automation API](https://github.com/pulumi/automation-api-examples)
- [Guide Policy as Code](https://www.pulumi.com/crossguard/)