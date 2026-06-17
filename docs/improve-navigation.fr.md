---
title: Audit de navigation pour WikiCode
description: Analyse et améliorations proposées pour la navigation du site WikiCode.
created: 2026-06-14
tags:
  - meta
  - guide
status: draft
---

# Audit de navigation

## Structure actuelle

La navigation principale est définie dans `mkdocs.yml` et inclut actuellement :

- Accueil
- Recherche
- Pour commencer
- Parcours d'apprentissage
- Guides
- Référence (Glossaire, Architecture, Journal des modifications)
- Sujets
- Outils
- Tags
- Blog
- Projets
- Snippets
- Rapports

## Améliorations proposées

1. **Regrouper les sections méta** sous un seul élément de menu « À propos » ou « WikiCode » (Rapports, Journal des modifications, Architecture)
2. **Déplacer Tags dans Sujets** car ce sont des concepts liés
3. **Ajouter des indicateurs visuels** pour le contenu récemment mis à jour
4. **Assurer que les fils d'Ariane** sont actifs à tous les niveaux de navigation

## Implémentation

Toutes les modifications doivent être apportées au bloc `nav:` dans `mkdocs.yml`.