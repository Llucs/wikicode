---
title: Stratégies de versionnement d'API
description: Techniques essentielles et meilleures pratiques pour gérer les modifications apportées à une API au fil du temps sans casser les clients existants, y compris les approches basées sur l'URI, l'en-tête, le paramètre de requête et le schéma.
created: 2026-06-24
tags:
  - api-design
  - rest
  - versioning
  - architecture
  - backend
status: draft
---

# Stratégies de versionnement d'API

Le versionnement d'API est la pratique qui consiste à gérer les modifications apportées à un contrat d'API public ou interne afin que les fournisseurs puissent faire évoluer l'interface sans perturber les consommateurs existants. Il permet à plusieurs représentations d'une même ressource de fonctionner en parallèle, en équilibrant innovation et stabilité. Choisir la bonne stratégie—et l'implémenter de manière cohérente—est l'une des décisions les plus importantes dans la conception d'API.

Ce guide couvre les techniques de versionnement les plus courantes, leurs compromis, des cas d'utilisation réels et des exemples d'implémentation pratiques pour les principaux frameworks. Vous apprendrez également à gérer la dépréciation et la suppression avec des en-têtes de cycle de vie appropriés.

---

## Pourquoi le versionnement est important

Sans versionnement, chaque modification d'une API est risquée :

- L'ajout d'un champ obligatoire peut casser les clients qui envoient d'anciennes charges utiles.
- La suppression d'un point de terminaison peut entraîner des interruptions de production.
- La modification du format d'un champ de réponse (par exemple, de chaîne à entier) force tous les consommateurs à se mettre à jour simultanément.

Une stratégie de versionnement fournit un **contrat** : les clients sur la version `v1` bénéficient d'une interface stable, tandis que le fournisseur peut introduire des changements cassants dans `v2`. Cela permet aux équipes de livrer rapidement tout en maintenant la confiance des consommateurs.

### Contexte historique

- **Premières API REST (milieu des années 2000) :** Flickr, Twitter et d'autres ont commencé à préfixer les URI par `/v1/` pour plus de clarté. SOAP s'appuyait sur des schémas WSDL stricts.
- **La thèse de Roy Fielding** prônait l'hypermedia (HATEOAS) comme mécanisme de versionnement « naturel »—où les liens guident les clients à travers les états. Cependant, la complexité a fait du versionnement par URI le standard de facto.
- **GraphQL (2015)** a promu une approche « sans version » en utilisant la dépréciation de champs plutôt que des changements cassants.
- **gRPC** utilise les packages Protobuf et les registres de schémas pour l'évolution des contrats.
- **La spécification OpenAPI** documente désormais plusieurs versions dans un seul fichier de spécification, ce qui facilite la rédaction et la comparaison des versions.

---

## Stratégies principales

Toutes les stratégies se situent sur un spectre allant des **identifiants de version explicites** (faciles pour les consommateurs) aux **contrats implicites** (propres pour les fournisseurs). Choisissez en fonction de la maturité de votre écosystème et de sa tolérance aux changements cassants.

### 1. Versionnement par URI / chemin

La version est intégrée directement dans le chemin de l'URL, ce qui en fait l'approche la plus courante et la plus simple.

```
GET /v1/utilisateurs
GET /v2/utilisateurs
```

**Avantages**
- Simple à implémenter et à router.
- Très découvrable—les consommateurs voient la version immédiatement.
- Excellent cache : différentes versions peuvent être mises en cache indépendamment.
- Facile à déployer sur les passerelles API et les CDN.

**Inconvénients**
- Enfreint la sémantique REST : une URI doit identifier une ressource, pas une version (selon Fielding).
- Encourage le fork du code serveur s'il n'est pas conçu avec des couches.
- Impossible de versionner par représentation (par exemple, une version différente pour la même ressource basée sur l'en-tête `Accept`).

**Exemple d'implémentation (Express.js)**

```javascript
// routeur v1
const v1Router = require('./routes/v1');
app.use('/v1', v1Router);

// routeur v2
const v2Router = require('./routes/v2');
app.use('/v2', v2Router);
```

**Exemple d'implémentation (ASP.NET Core)**

```csharp
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/[controller]")]
public class UsersController : ControllerBase
{
    [HttpGet]
    public IActionResult Get() => Ok("Users from v1");
}
```

### 2. Versionnement par paramètre de requête

Un paramètre de requête spécifie la version.

```
GET /utilisateurs?version=1
GET /utilisateurs?version=2
```

**Avantages**
- Simple à ajouter sans modifier les routes.
- Le modèle d'URL reste cohérent entre les versions.

**Inconvénients**
- Pollue la sémantique de la requête—`version` n'est pas un filtre ou un terme de requête.
- Complique la mise en cache car le paramètre modifie la clé de cache.
- Facile pour les clients d'oublier de l'inclure, ce qui entraîne un repli de version involontaire.

**Exemple d'implémentation (Express.js)**

```javascript
app.get('/users', (req, res) => {
  const version = req.query.version || 1;
  switch(version) {
    case '1': return handleV1(req, res);
    case '2': return handleV2(req, res);
    default:  return res.status(400).json({ error: 'Invalid version' });
  }
});
```

### 3. Versionnement par en-tête

Les informations de version sont transportées dans les en-têtes HTTP. Deux approches courantes :

| Approche               | Exemple d'en-tête                               |
|------------------------|--------------------------------------------------|
| En-tête personnalisé   | `X-API-Version: 1`                               |
| En-tête Accept (type MIME vendor) | `Accept: application/vnd.myapi.v1+json` |

**Avantages**
- Le plus RESTful—l'URL identifie la ressource, l'en-tête identifie la représentation.
- URI propres qui ne changent jamais.
- Contrôle fin : vous pouvez versionner par type de média (par exemple, JSON `v1`, XML `v2`).

**Inconvénients**
- Faible découvrabilité—difficile à tester dans un navigateur ou curl sans modification d'en-tête.
- Simule la complexité côté serveur pour le routage basé sur les en-têtes.
- La mise en cache peut être délicate à moins que les en-têtes `Vary` ne soient correctement définis.

**Exemple d'implémentation (ASP.NET Core avec en-tête Accept)**

```csharp
// Dans Startup.cs
services.AddApiVersioning(options =>
{
    options.ApiVersionReader = new MediaTypeApiVersionReader();
    options.AssumeDefaultVersionWhenUnspecified = true;
});

// Contrôleur
[ApiVersion("1.0")]
[Route("api/users")]
public class UsersV1Controller : ControllerBase {}
```

**Exemple d'implémentation (Spring Boot)**

```java
@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v1+json")
public class UserControllerV1 { ... }

@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v2+json")
public class UserControllerV2 { ... }
```

### 4. Versionnement par code / schéma (sans version explicite)

Souvent appelé « sans version » ou « contrat d'abord ». Au lieu d'exposer un identifiant de version, le fournisseur d'API maintient la rétrocompatibilité en ajoutant uniquement des champs ou des points de terminaison. Les changements cassants sont communiqués via des registres de schémas (par exemple, Protobuf, Avro) ou en introduisant un nouveau point de terminaison/opération.

```
// Versionnement par package Protobuf
package myapi.v1;
message User {
  string name = 1;
}

// Plus tard, dans v2 :
message User {
  string name = 1;
  string email = 2;
}
```

**Avantages**
- Pas besoin de maintenir plusieurs chemins de routage.
- Incite à la rétrocompatibilité continue.
- Bon pour les microservices internes et les systèmes pilotés par les événements.

**Inconvénients**
- Impossible de communiquer des changements cassants intentionnels sans indicateur de version.
- Devient un fardeau de maintenance si la rétrocompatibilité est involontairement rompue.

**Idéal pour :**
- Les microservices internes où consommateurs et fournisseurs sont dans la même organisation.
- Les schémas GraphQL utilisant la directive `@deprecated`.
- Les systèmes pilotés par les événements avec des registres de schémas (Confluent Schema Registry, AWS Glue).

---

## Cas d'utilisation par secteur

| Cas d'utilisation | Stratégie préférée | Justification |
|----------|-------------------|-----------|
| **API publiques (Stripe, Twilio)** | Versionnement par URI | Les clients ont besoin de contrats explicites et stables ; la mise en cache est simple. |
| **Backends mobiles (Facebook, Twitter)** | Versionnement par en-tête (personnalisé) | L'application envoie la version avec laquelle elle a été compilée ; l'URL ne change jamais, évitant la pression de mise à jour de l'app store. |
| **Microservices internes** | Sans version / Protobuf | Les registres de schémas imposent la compatibilité ; pas besoin de maintenir plusieurs versions de point de terminaison. |
| **Systèmes pilotés par les événements** | Schema Registry (Avro/Protobuf) | Les contrats de données évoluent indépendamment ; les consommateurs valident par rapport à l'ID du schéma. |

---

## Installation et configuration

Le versionnement est un **modèle de conception**, mais il nécessite des outils pour appliquer le routage, la validation et la documentation. Vous trouverez ci-dessous les étapes d'installation pour les environnements courants.

### ASP.NET Core

Ajoutez le package NuGet `Microsoft.AspNetCore.Mvc.Versioning` et configurez :

```csharp
// Installation : dotnet add package Microsoft.AspNetCore.Mvc.Versioning
// Dans Startup.cs :
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers();
    services.AddApiVersioning(options =>
    {
        options.DefaultApiVersion = new ApiVersion(1, 0);
        options.AssumeDefaultVersionWhenUnspecified = true;
        options.ReportApiVersions = true;
    });
}
```

### Express.js

Aucune bibliothèque requise. Créez des routeurs par version et montez-les :

```javascript
// Installation : npm i express (aucune bibliothèque supplémentaire nécessaire)
const express = require('express');
const app = express();

const v1Router = require('./routes/v1');
const v2Router = require('./routes/v2');

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

app.listen(3000);
```

### Spring Boot

Spring Boot prend en charge nativement le versionnement par en-tête et par URI via `@RequestMapping`. Pour le versionnement par en-tête Accept, vous pouvez définir des contrôleurs séparés avec différents attributs `produces`.

```java
// Dépendance POM : spring-boot-starter-web (inclut Spring MVC)
// Pour le versionnement par type de média, les contrôleurs produisent différents types MIME vendor :
@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v1+json")
public class UserControllerV1 { ... }
```

### Passerelles API (Kong, AWS API Gateway)

Configurez les règles de routage en amont de votre code d'application :

- **Kong :** Définissez des services et des routes avec des chemins spécifiques (`/v1/`, `/v2/`). Vous pouvez également supprimer le préfixe du chemin avant de transmettre au backend.
- **AWS API Gateway :** Créez des stages ou des ressources avec des paramètres de chemin comme `{proxy+}` et le versionnement dans le chemin. Ou utilisez un en-tête `version` et routez avec un modèle de mapping.

```yaml
# Configuration déclarative Kong (YAML)
services:
  - name: users-api
    routes:
      - name: users-v1
        paths:
          - /v1/users
        strip_path: true
        service: users-api-v1-upstream
      - name: users-v2
        paths:
          - /v2/users
        strip_path: true
        service: users-api-v2-upstream
```

---

## Meilleures pratiques

### 1. Soyez cohérent
Choisissez une seule stratégie par surface d'API. Mélanger le versionnement par URI et par en-tête entre les points de terminaison prête à confusion.

### 2. Versionnez le contrat, pas l'implémentation
Votre spécification OpenAPI (ou équivalent) doit être la source de vérité. Les modifications du contrat nécessitent une nouvelle version, pas des changements dans le code interne.

### 3. Préférez la rétrocompatibilité (mais n'ayez pas peur des changements cassants)
Lorsque c'est possible, ajoutez de nouveaux champs plutôt que de supprimer ou renommer des champs existants. Utilisez les marqueurs `@deprecated` dans votre spécification. Cependant, les changements cassants sont parfois nécessaires—le versionnement est le filet de sécurité.

### 4. Utilisez des en-têtes de cycle de vie explicites
Lorsqu'une version est dépréciée, renvoyez ces en-têtes inspirés des RFC :

- `Deprecation: Sat, 01 Jan 2025 00:00:00 GMT` – indique que la version est dépréciée.
- `Sunset: Wed, 01 Jul 2026 00:00:00 GMT` – indique quand la version sera supprimée.
- `Link: </v2/users>; rel="successor-version"` – pointe vers le remplacement.

**Exemple d'ensemble d'en-têtes de réponse :**

```http
HTTP/1.1 200 OK
Content-Type: application/json
Deprecation: true
Sunset: Wed, 01 Jul 2026 00:00:00 GMT
Link: </v2/users>; rel="successor-version"
```

### 5. Traitez votre contrat d'API avec le versionnement sémantique
Utilisez la sémantique `MAJEUR.MINEUR.CORRECTIF` :

- **Majeur :** changements cassants → nouvelle version (par exemple, `/v2/`).
- **Mineur :** modifications additives et rétrocompatibles (par exemple, nouveaux champs dans le corps, nouveaux points de terminaison).
- **Correctif :** corrections ou améliorations non fonctionnelles.

### 6. Documentez tout
Incluez la stratégie de versionnement dans le champ `info.version` de votre spécification OpenAPI et fournissez des guides de migration entre les versions.

```yaml
openapi: 3.0.0
info:
  title: My API
  version: 2.0.0
  description: |
    ## Versionnement
    Cette API utilise le versionnement par chemin URI. Toutes les requêtes doivent inclure la version dans le chemin de l'URL, par exemple `/v2/users`.
    Consultez le [guide de migration](/docs/migration) pour les changements de v1 à v2.
```

### 7. Automatisez l'application de la suppression
Utilisez des passerelles API ou un middleware pour rejeter les appels vers les versions dépréciées après une date limite. Renvoyez `410 Gone` avec un lien vers la dernière version.

---

## Cycle de vie de la dépréciation

Une API versionnée entièrement gérée passe par ces étapes :

1. **Active** – la version est par défaut ou appelable explicitement.
2. **Dépréciée** – la version fonctionne toujours mais renvoie l'en-tête `Deprecation`. Les consommateurs devraient voir une bannière dans la documentation.
3. **Suppression programmée** – la version sera supprimée à une date spécifique. Renvoie les en-têtes `Deprecation` et `Sunset`.
4. **Supprimée** – le point de terminaison renvoie `410 Gone` (pas `404`). La date `Sunset` est dépassée.

**Exemple de middleware (Express.js) pour les en-têtes de dépréciation automatiques :**

```javascript
const deprecatedVersions = {
  v1: { deprecatedAt: new Date('2025-01-01'), sunsetAt: new Date('2026-07-01'), successor: '/v2/users' }
};

app.use((req, res, next) => {
  const match = req.path.match(/^\/v(\d+)/);
  if (match && deprecatedVersions[`v${match[1]}`]) {
    const info = deprecatedVersions[`v${match[1]}`];
    res.set('Deprecation', info.deprecatedAt.toUTCString());
    res.set('Sunset', info.sunsetAt.toUTCString());
    if (info.successor) {
      res.set('Link', `<${info.successor}>; rel="successor-version"`);
    }
  }
  next();
});
```

---

## Conclusion

Le versionnement d'API est une décision stratégique qui affecte chaque consommateur de votre API. Il n'existe pas de stratégie universelle ; le choix correct dépend de votre base de consommateurs, de votre écosystème et de votre tolérance au risque.

| Stratégie | Quand choisir |
|----------|----------------|
| **URI / Chemin** | API publiques, où la découvrabilité et la mise en cache sont primordiales. |
| **Paramètre de requête** | Cas d'utilisation simples avec des consommateurs internes où la flexibilité est nécessaire. |
| **En-tête (Accept / Personnalisé)** | Applications mobiles, clients de longue durée, ou lorsque vous souhaitez des URI propres. |
| **Sans version / Schéma** | Services internes, architectures pilotées par les événements, ou GraphQL. |

Quelle que soit la stratégie, investissez dans une documentation claire, des en-têtes de cycle de vie et une dépréciation progressive. Une API bien versionnée établit la confiance et permet à votre plateforme d'évoluer sans casser l'écosystème qui en dépend.

> **Lectures complémentaires**
> - [Versionnement d'API REST par Microsoft](https://learn.microsoft.com/fr-fr/azure/architecture/best-practices/api-design#versioning)
> - [Spécification OpenAPI](https://spec.openapis.org/oas/latest.html)
> - [RFC 8594 : En-tête Sunset](https://tools.ietf.org/html/rfc8594)
> - [API Design Patterns – Chapitre sur le versionnement](https://www.manning.com/books/api-design-patterns)