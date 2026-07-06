---
title: Schéma du commutateur de circuit dans le conception système
description: Un mécanisme utilisé pour empêcher les échecs d'une partie d'un système distribué de se propager à d'autres parties, améliorant ainsi la fiabilité et la stabilité globales du système.
created: 2026-07-06
tags:
  - conception système
  - microservices
  - résilience
  - tolérance aux anomalies
status: brouillon
---

# Schéma du commutateur de circuit dans le conception système

Le Schéma du commutateur de circuit est un modèle de conception utilisé en ingénierie logicielle pour empêcher les échecs en cascade dans les systèmes distribués. Il sert de mécanisme de contrôle qui surveille le succès ou l'échec des opérations externes et change le comportement du système lorsque les échecs dépassent un certain seuil. Lorsque le commutateur de circuit est "ouvert", il arrête les demandes supplémentaires de parvenir au service en aval, en renvoyant une réponse prédéfinie au client au lieu de la suivante. Une fois que le service retourne à un état stable, le commutateur de circuit peut être "fermé" à nouveau, permettant au système de réessayer l'opération.

## Caractéristiques clés

1. **Détecteur d'indisponibilité du service** : Le commutateur de circuit surveille l'état des services dépendants ou des composants. Si un certain nombre d'échecs se produisent dans un intervalle de temps spécifique, le commutateur de circuit tripote.
2. **Mécanisme de retournement** : Lorsque le commutateur de circuit est ouvert, il fournit un mécanisme de retournement qui renvoie une réponse prédéfinie au client, évitant ainsi une échec complète de l'application.
3. **Retrouvailles retardées** : Au lieu de réessayer immédiatement les demandes échouées, le commutateur de circuit permet un délai, qui peut aider le système à se remettre d'issues transitoires.
4. **État du commutateur de circuit** : Le commutateur de circuit maintient un état (ouvert/fermé) et passe d'un état à l'autre en fonction du succès ou de l'échec du service.

## Installation et configuration

La mise en œuvre spécifique du Schéma du commutateur de circuit peut varier en fonction de la langue de programmation et du framework utilisés. Voici un exemple de base d'installation à l'aide d'une bibliothèque Java populaire appelée Hystrix.

### Ajouter une dépendance

Pour Maven, incluez la bibliothèque Hystrix dans votre projet :

```xml
<dependency>
    <groupId>com.netflix.hystrix</groupId>
    <artifactId>hystrix-javanica</artifactId>
    <version>1.5.18</version>
</dependency>
```

### Créer une commande

Définissez une commande Hystrix pour le service que vous voulez protéger.

```java
import com.netflix.hystrix.HystrixCommand;
import com.netflix.hystrix.HystrixCommandGroupKey;

public class MyServiceCommand extends HystrixCommand<String> {
    public MyServiceCommand() {
        super(HystrixCommandGroupKey.Factory.asKey("MyServiceGroup"));
    }

    @Override
    protected String run() throws Exception {
        // Appelez le service ou l'opération ici
        return callService();
    }

    @Override
    protected String getFallback() {
        return "Réponse de retrait";
    }
}
```

### Exécuter la commande

Utilisez la commande pour exécuter l'appel de service.

```java
MyServiceCommand command = new MyServiceCommand();
String result = command.execute();
```

## Utilisation de base

1. **Initialisation** : Créez une instance de la commande Hystrix.
2. **Exécution** : Utilisez la méthode `execute` pour exécuter la commande. Si le service n'est pas disponible, le mécanisme de retrait est invoqué.
3. **Méthode de retrait** : Définissez une méthode de retrait qui renvoie une réponse prédéfinie.

```java
@Override
protected String run() throws Exception {
    // Appelez le service ou l'opération ici
    return callService();
}

@Override
protected String getFallback() {
    return "Réponse de retrait";
}
```

4. **Suivi** : Utilisez Hystrix Dashboard pour suivre les statistiques d'exécution et la santé des commandes.

## Cas d'utilisation

1. **Communication de microservices** : Dans les architectures de microservices, où les services communiquent entre eux, le Schéma du commutateur de circuit empêche une échec dans un service de se propager à d'autres services.
2. **Portail API** : Lorsqu'un portail API gère l'accès à plusieurs services, le Schéma du commutateur peut empêcher les échecs dans un service de perturber l'API entière.
3. **Services tiers** : Lors de l'intégration avec des services tiers ou des API externes, le Schéma du commutateur de circuit aide à gérer les échecs transitoires gracieusement.
4. **Accès à la base de données** : Dans les interactions avec la base de données, le modèle permet d'éviter les échecs dus à des problèmes temporaires de connexion ou à une surcharge de la base de données.

## Conclusion

Le Schéma du commutateur de circuit est un outil puissant pour gérer les échecs dans les systèmes distribués, assurant que les échecs dans une partie du système ne paralysent pas le système entier. En mettant en œuvre ce schéma, les développeurs peuvent construire des applications plus résilientes et échelle.