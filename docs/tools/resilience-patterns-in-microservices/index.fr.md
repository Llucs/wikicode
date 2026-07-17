---
title: Modèles de résilience dans les microservices
description: Stratégies pratiques et modèles pour construire des architectures de microservices résilientes, notamment les interrupteurs de circuit, les réessayages, les compartiments de charge et les délais de réponse.
created: 2026-07-17
tags:
  - microservices
  - résilience
  - architecture
status: brouillon
---

# Modèles de résilience dans les microservices

Les modèles de résilience sont des stratégies de conception et des pratiques qui permettent aux architectures de microservices de gérer les échecs et de maintenir une haute disponibilité. Ils sont cruciaux pour s'assurer que le système peut se remettre des pannes, se dégrader de manière gracieuse et continuer à fournir de la valeur aux utilisateurs même lorsque des parties du système sont hors service.

## Caractéristiques clés des modèles de résilience

1. **Tolérance aux pannes** : La capacité à continuer d'opérer même lorsque des parties du système échouent.
2. **Balancement de charge** : Distribuer les requêtes parmi plusieurs instances pour éviter de surcharger un seul service.
3. **Interrupteur de circuit** : Un mécanisme qui détecte les échecs et arrête de faire des requêtes vers un service échoué pour prévenir les échecs cascades.
4. **Retours d'urgence** : Renvoyer une réponse préétablie lorsque le service principal échoue.
5. **Délais de réponse** : Fixer des limites sur le temps nécessaire pour que la requête soit terminée.
6. **Mécanismes de réessayage** : Réessayer automatiquement les requêtes échouées après une courte période.
7. **Dégagement** : Fournir une version simplifiée ou limitée d'un service lorsque la pleine fonctionnalité n'est pas disponible.
8. **Vérifications de santé** : Surveiller la santé des services pour détecter et atténuer les problèmes de manière proactive.

## Histoire

Le concept de modèles de résilience dans les architectures de microservices a pris de l'ampleur avec l'adoption généralisée des microservices. La nécessité de ces modèles est devenue apparente lorsque les microservices ont commencé à introduire des systèmes plus complexes et distribués. Les travaux précurseurs en tolérance aux pannes et en balancement de charge peuvent être tracés à des recherches sur les systèmes distribués, mais le contexte moderne des microservices et de l'informatique en nuage a considérablement étendu leur importance.

## Cas d'utilisation

1. **Services financiers** : La haute disponibilité et la tolérance aux pannes sont critiques pour éviter les pertes financières.
2. **Commerce électronique** : Assurer que les systèmes de traitement des paiements et de gestion des stocks peuvent gérer les pics de charge et les échecs.
3. **Santé** : Maintenir l'accessibilité des services est crucial pour éviter la perte de données patient et des erreurs de traitement.
4. **Traitement en temps réel des données** : Les systèmes nécessitant un traitement en temps réel et une analyse des données en flux continu.
5. **Services en nuage** : Gérer la nature dynamique et imprévisible des ressources en nuage.

## Installation et configuration

La mise en place des modèles de résilience implique à la fois des composants logiciels et des solutions d'infrastructure.

1. **Bibliothèques de logiciel et outils** :
   - **Netflix Hystrix** : Une bibliothèque pour gérer les interrupteurs de circuit, les retours d'urgence, les délais de réponse et les réessayages.
   - **Resilience4j** : Une bibliothèque Java pour la résilience qui fournit une API simple pour implémenter les modèles de résilience.
   - **Spring Cloud Circuit Breaker** : Une implémentation d'Hystrix au sein de l'écosystème Spring.

2. **Solutions d'infrastructure** :
   - **Balanciers de charge** : Des services comme NGINX, AWS Elastic Load Balancer, ou HAProxy peuvent être configurés pour distribuer le trafic.
   - **Réseaux de services** : Des outils comme Istio ou Linkerd peuvent fournir des injections de fautes, des interrupteurs de circuit et des réessayages à un niveau d'abstraction plus élevé.

### Exemple de configuration

Voici un exemple de la mise en place d'un interrupteur de circuit avec Resilience4j dans une application Java :

```java
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;

public class Example {

    private final CircuitBreakerRegistry circuitBreakerRegistry;

    public Example(CircuitBreakerRegistry circuitBreakerRegistry) {
        this.circuitBreakerRegistry = circuitBreakerRegistry;
    }

    @CircuitBreaker(name = "exampleService", fallbackMethod = "fallbackMethod")
    public String callExampleService() {
        // Appel au service exampleService
        return "Résultat du service exampleService";
    }

    public String fallbackMethod() {
        return "Réponse d'urgence";
    }
}
```

## Utilisation de base

### Interrupteur de circuit

1. **Implémentation** : Utiliser Hystrix ou Resilience4j pour créer un interrupteur de circuit.
2. **Configuration** : Définir le seuil pour débrancher le circuit (par exemple, 50 requêtes échouées par minute) et le temps de remise à zéro (par exemple, 30 secondes).
3. **Utilisation** : Envelopper les appels de service dans un interrupteur de circuit pour détecter les échecs et arrêter les appels supplémentaires vers le service échoué.

### Exemple avec Resilience4j

```java
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;

public class Example {

    private final CircuitBreakerRegistry circuitBreakerRegistry;

    public Example(CircuitBreakerRegistry circuitBreakerRegistry) {
        this.circuitBreakerRegistry = circuitBreakerRegistry;
    }

    @CircuitBreaker(name = "exampleService", fallbackMethod = "fallbackMethod")
    public String callExampleService() {
        // Appel au service exampleService
        return "Résultat du service exampleService";
    }

    public String fallbackMethod() {
        return "Réponse d'urgence";
    }
}
```

### Délais de réponse

1. **Configuration** : Fixer un délai de réponse pour les appels de service (par exemple, 500 ms pour une requête à une base de données).
2. **Utilisation** : Assurer que tous les appels de service sont enveloppés par un délai de réponse pour éviter des attentes indéfinies.

### Exemple avec Resilience4j

```java
import io.github.resilience4j.ratelimiter.RateLimiter;
import io.github.resilience4j.ratelimiter.RateLimiterRegistry;
import io.github.resilience4j.ratelimiter.annotation.RateLimiter;

public class Example {

    private final RateLimiterRegistry rateLimiterRegistry;

    public Example(RateLimiterRegistry rateLimiterRegistry) {
        this.rateLimiterRegistry = rateLimiterRegistry;
    }

    @RateLimiter(name = "exampleService", fallbackMethod = "fallbackMethod")
    public String callExampleService() {
        // Appel au service exampleService
        return "Résultat du service exampleService";
    }

    public String fallbackMethod() {
        return "Réponse d'urgence";
    }
}
```

### Mécanismes de retour d'urgence

1. **Implémentation** : Définir une réponse d'urgence lorsque le service principal échoue.
2. **Utilisation** : Utiliser les retours d'urgence pour fournir une réponse par défaut ou limitée lorsque le service principal est indisponible.

### Exemple avec Resilience4j

```java
import io.github.resilience4j.ratelimiter.RateLimiter;
import io.github.resilience4j.ratelimiter.RateLimiterRegistry;
import io.github.resilience4j.ratelimiter.annotation.RateLimiter;

public class Example {

    private final RateLimiterRegistry rateLimiterRegistry;

    public Example(RateLimiterRegistry rateLimiterRegistry) {
        this.rateLimiterRegistry = rateLimiterRegistry;
    }

    @RateLimiter(name = "exampleService", fallbackMethod = "fallbackMethod")
    public String callExampleService() {
        // Appel au service exampleService
        return "Résultat du service exampleService";
    }

    public String fallbackMethod() {
        return "Réponse d'urgence";
    }
}
```

### Mécanismes de réessayage

1. **Configuration** : Définir le nombre de réessayages et la stratégie d'écartement (par exemple, écartement exponentiel).
2. **Utilisation** : Envelopper les appels de service dans un mécanisme de réessayage pour réessayer automatiquement les requêtes échouées.

### Exemple avec Resilience4j

```java
import io.github.resilience4j.retry.Retry;
import io.github.resilience4j.retry.RetryRegistry;
import io.github.resilience4j.retry.annotation.Retry;

public class Example {

    private final RetryRegistry retryRegistry;

    public Example(RetryRegistry retryRegistry) {
        this.retryRegistry = retryRegistry;
    }

    @Retry(name = "exampleService", fallbackMethod = "fallbackMethod")
    public String callExampleService() {
        // Appel au service exampleService
        return "Résultat du service exampleService";
    }

    public String fallbackMethod() {
        return "Réponse d'urgence";
    }
}
```

### Vérifications de santé

1. **Implémentation** : Utiliser des outils comme Prometheus ou les sondes de santé Kubernetes pour surveiller la santé des services.
2. **Utilisation** : Configurer les vérifications de santé pour détecter les problèmes et prendre les mesures appropriées (par exemple, redémarrer le service).

### Exemple avec Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: example-service
  template:
    metadata:
      labels:
        app: example-service
    spec:
      containers:
      - name: example-service
        image: example-service:latest
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
```

## Conclusion

Les modèles de résilience sont essentiels pour construire des architectures de microservices robustes. En mettant en place ces modèles, les développeurs peuvent s'assurer que leurs systèmes sont résilients face aux échecs, peuvent gérer des charges de travail élevées et continuer à fournir de la valeur aux utilisateurs même sous des conditions difficiles.