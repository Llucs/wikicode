---
title: Rechercher dans le wiki
description: Comment rechercher dans WikiCode.
created: 2026-06-03
tags:
  - meta
  - reference
status: stable
---

# Rechercher dans le wiki

WikiCode est entièrement consultable. L'index de recherche est construit au moment du déploiement et s'exécute entièrement dans le navigateur, de sorte que les requêtes sont instantanées et aucune donnée ne quitte votre machine.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Créé : 2026-06-03</span>
<span class="wikicode-meta-updated">Dernière mise à jour : auto (git)</span>
</div>

## Comment rechercher

<div class="grid cards" markdown>

- :material-magnify: __Barre de recherche__

    Cliquez sur l'icône de loupe en haut à droite de n'importe quelle page
    (ou appuyez sur ++slash++ au clavier) pour ouvrir la fenêtre de recherche.

- :material-keyboard: __Raccourci clavier__

    - ++slash++ — met le focus sur la barre de recherche.
    - ++esc++ — ferme la fenêtre de recherche.
    - ++arrow-up++ / ++arrow-down++ — parcourir les résultats.
    - ++enter++ — ouvrir le résultat en surbrillance.

- :material-format-letter-case: __Conseils__

    - La recherche est **basée sur les sous-chaînes**. Taper `mkdocs` correspond à toute
      page contenant « mkdocs ».
    - La recherche est **insensible à la casse** par défaut.
    - Les expressions entre guillemets correspondent à des sous-chaînes exactes : `"open hands"`.
    - Plusieurs mots correspondent aux pages qui contiennent tous ces termes.

</div>

## Ce qui est indexé

L'index de recherche couvre chaque page Markdown rendue sur le site :

- Articles, guides et pages de référence sous `docs/`.
- Résumés de projets sous `projects/`.
- Descriptions de snippets sous `snippets/`.
- Pages d'outils sous `docs/tools/`.
- Articles de blog sous `blog/`.
- Le texte des blocs de code (afin que vous puissiez rechercher un nom de fonction
  ou un indicateur CLI).

L'index est régénéré à chaque push sur `main`, donc il est toujours synchronisé
avec le contenu publié.

## Pourquoi côté client

- **Confidentialité.** Aucune requête n'est envoyée à un service distant.
- **Vitesse.** Les résultats apparaissent au fur et à mesure que vous tapez.
- **Coût.** Il n'y a rien à héberger en plus du site statique.
- **Hors ligne.** Une fois le site chargé, l'index est dans le cache du navigateur
  et continue de fonctionner sans réseau.

## Ajouter un raccourci de recherche personnalisé

Si vous souhaitez un lien profond qui ouvre la fenêtre de recherche pré-remplie,
ajoutez `?q=<query>` à l'URL du site après avoir mis le focus sur la recherche
une fois. Le comportement exact dépend de la version du thème Material ; la
méthode recommandée est d'utiliser le raccourci clavier (++slash++) et de taper
la requête.