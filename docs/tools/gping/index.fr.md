---
title: gping - Outil de Supervision de Réseau
description: gping est un outil de ligne de commande pour mesurer le temps de latence aller-retour (RTT) entre deux nœuds de réseau. Il est similaire à la commande `ping` mais utilise la fonction `getaddrinfo` de `glibc` pour la résolution des noms d'hôte, ce qui en fait un outil plus flexible et capable de gérer différents types d'adresses de réseau. gping est conçu pour la supervision de réseau, le dépannage et le test de performances.
created: 2026-07-23
tags:
  - réseau
  - supervision
  - gping
  - ping
status: brouillon
---

# gping - Outil de Supervision de Réseau

## Aperçu

**gping** est un outil de ligne de commande pour mesurer le temps de latence aller-retour (RTT) entre deux nœuds de réseau. Il est similaire à la commande `ping` mais utilise la fonction `getaddrinfo` de `glibc` pour la résolution des noms d'hôte, ce qui en fait un outil plus flexible et capable de gérer différents types d'adresses de réseau. gping est conçu pour la supervision de réseau, le dépannage et le test de performances.

## Fonctionnalités Clés

- **Résolution DNS**: Utilise `getaddrinfo` pour la résolution des noms d'hôte, en prenant en charge les IPv4, les IPv6 et d'autres types d'adresses.
- **Soutien à Plusieurs Hôtes**: Peut pinger plusieurs hôtes simultanément.
- **Configuration Flexible**: Permet la personnalisation des paramètres de ping tels que le délai d'échec, la taille du paquet, etc.
- **Informations Étendues**: Fournit des informations détaillées sur le chemin réseau et la résolution DNS.

## Histoire

`gping` a été développé comme partie du projet GNU C Library (glibc). La première implémentation a été ajoutée à glibc dans la version 2.15. Depuis lors, elle a été continuellement améliorée et mise à jour pour prendre en charge de nouveaux protocoles réseau et fonctionnalités.

## Cas d'Utilisation

- **Dépannage du Réseau**: Diagnostic de la latence de réseau et des problèmes de connectivité.
- **Test de Performance**: Évaluation de la performance des connexions de réseau et des services.
- **Scripting et Automatisation**: Intégration du test de réseau dans les scripts et les flux de travail d'automatisation.

## Installation

`gping` est généralement inclus dans le package glibc, qui fait partie du système d'exploitation de base sur de nombreuses distributions Linux. Voici comment l'installer :

### Debian/Ubuntu
```sh
sudo apt-get update
sudo apt-get install glibc-doc
```

### Red Hat/CentOS
```sh
sudo yum install glibc-doc
```

### Arch Linux
```sh
sudo pacman -S glibc
```

## Utilisation de Base

### PING Basique
Pour exécuter un ping basique vers un nom d'hôte ou une adresse IP :
```sh
gping google.com
```

### Spécification des Options de PING
Vous pouvez spécifier diverses options pour personnaliser le comportement du ping :

```sh
gping -c 10 -i 2 google.com
```
- `-c 10` : Envoyer 10 requêtes ICMP d'écho.
- `-i 2` : Utiliser un intervalle de 2 secondes entre les paquets de ping.

### PING de Plusieurs Hôtes
Pour pinger simultanément plusieurs hôtes :
```sh
gping -c 1 -i 1 google.com example.com
```

### Affichage Détaillé
Pour obtenir un affichage détaillé :
```sh
gping -v google.com
```

## Exemple d'Utilisation

Voici une session d'exemple :

```sh
gping -v google.com
```

La sortie pourrait ressembler à ceci :
```
PING google.com (93.184.216.34): 56 octets
64 octets de 93.184.216.34 : icmp_seq=0 ttl=56 temps=24.1 ms
64 octets de 93.184.216.34 : icmp_seq=1 ttl=56 temps=23.5 ms
64 octets de 93.184.216.34 : icmp_seq=2 ttl=56 temps=23.3 ms
64 octets de 93.184.216.34 : icmp_seq=3 ttl=56 temps=23.0 ms
64 octets de 93.184.216.34 : icmp_seq=4 ttl=56 temps=24.4 ms
--- google.com ping statistiques ---
5 paquets transmis, 5 paquets reçus, 0.0% de perte de paquets
temps aller-retour minimum/maximum/moyen/écart-type = 23.0/23.7/24.4/0.6 ms
```

Dans cet exemple, `gping` pingue avec succès `google.com` et fournit la durée moyenne aller-retour et d'autres statistiques pertinentes.

## Conclusion

`gping` est un outil puissant pour le diagnostic réseau et le test de performance, offrant une flexibilité et une robustesse pour mesurer la latence de réseau et la résolution DNS. Sa intégration avec glibc en fait un ajout précieux à l'outillage d'administrateur réseau.