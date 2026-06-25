---
title: Top 10 OWASP de la sécurité des API
description: Un wiki complet pour développeurs couvrant le Top 10 OWASP de la sécurité des API (2023), incluant des analyses approfondies, des stratégies de test et l'intégration CI/CD.
created: 2026-06-25
tags:
  - owasp
  - api-security
  - top-10
  - bola
  - bopla
  - secure-coding
  - devsecops
  - bug-bounty
status: draft
---

# Top 10 OWASP de la sécurité des API

Le **Top 10 OWASP de la sécurité des API** est un document de sensibilisation de référence publié par l'Open Web Application Security Project (OWASP), mis à jour en 2023 pour refléter les risques de sécurité spécifiques des API REST, GraphQL, gRPC et SOAP modernes. Contrairement au Top 10 Web général d'OWASP (qui couvre XSS, SQLi, CSRF, etc.), cette liste se concentre **exclusivement** sur les failles architecturales et logiques qui affectent les applications pilotées par API.

En 2026, les incidents liés aux API restent le vecteur principal des violations de données, avec des incidents chez des grandes entreprises (Twitter, T-Mobile, Optus) attribuables à quelques erreurs évitables documentées dans ce cadre.

---

## Les 10 principaux risques de sécurité des API (2023)

| Rang | Nom | Acronyme | Problème principal |
|------|-----|----------|--------------------|
| API1 | Autorisation au niveau des objets brisée | BOLA | Accès aux objets d'autres utilisateurs sans vérifications ACL appropriées |
| API2 | Authentification brisée | — | Gestion faible des identifiants, fuite de jetons, fixation de session |
| API3 | Autorisation au niveau des propriétés d'objet brisée | BOPLA | Affectation massive / sur-envoi de champs sensibles |
| API4 | Consommation illimitée des ressources | — | Absence de limite de débit, de plafonnement de pagination ou de taille de charge utile |
| API5 | Autorisation au niveau des fonctions brisée | BFLA | Appel de points d'accès administrateur à haute privilège par un utilisateur standard |
| API6 | Accès illimité aux flux métier sensibles | — | Bots exploitant des workflows API valides (scalping, scraping) |
| API7 | Falsification de requête côté serveur | SSRF | URLs contrôlées par l'utilisateur récupérées par l'API permettant de sonder des services internes |
| API8 | Mauvaise configuration de sécurité | — | Identifiants par défaut, erreurs verbeuses, CORS manquant, systèmes non patchés |
| API9 | Gestion inappropriée de l'inventaire | — | Versions d'API zombies/dépréciées, points d'accès de débogage oubliés, API fantômes |
| API10 | Consommation non sécurisée des API | — | Confiance aveugle dans les réponses d'API tierces (risque sur la chaîne d'approvisionnement) |

### Changements notables par rapport à 2019

L'édition 2023 a supprimé les menaces Web génériques (XSS, SQLi — désormais couvertes par le Top 10 standard) et introduit cinq catégories entièrement nouvelles : **BOPLA**, **Flux métier illimités**, **SSRF**, **Gestion inappropriée de l'inventaire** et **Consommation non sécurisée**.

Elle a également formalisé la méthodologie **« Laver, Rincer, Répéter »** — un cycle continu de Découverte → Validation → Correction.

---

## Méthodologie d'adoption

Puisqu'il s'agit d'un *cadre* (et non d'un logiciel), « l'installation » signifie intégrer l'état d'esprit et les flux de test dans votre cycle de développement.

### Phase 1 : Découverte et inventaire (Aborde API9)

Cartographiez chaque point d'accès, sa sensibilité des données, son mécanisme d'authentification et sa version. C'est l'étape la plus souvent négligée.

```bash
# Un simple scan de découverte pour les chemins d'API courants
for endpoint in /api/v1 /api/v2 /api/v3 /graphql /rest /soap /debug /health /swagger.json /openapi.json; do
  status=$(curl -o /dev/null -s -w "%{http_code}\n" "http://target.com${endpoint}")
  echo "Endpoint ${endpoint} retourné ${status}"
done
```

Outils : Postman, Swagger Inspector, Burp Suite, crawlers personnalisés.

### Phase 2 : Scan automatisé

Exécutez des scanners dynamiques contre votre spécification d'API.

```bash
# Scan d'API OWASP ZAP
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t file:///zap/wrk/openapi.yaml -f openapi -r report.html
```

**Vérifications clés à automatiser :**
- **BOLA :** Échangez les identifiants d'objets dans les requêtes en masse.
- **BFLA :** Tentez des DELETE/PUT sur des points d'accès administrateur avec des jetons à faible privilège.
- **SSRF :** Injectez `http://169.254.169.254/metadata/instance` dans les paramètres d'URL.
- **Mauvaise configuration :** Vérifiez la présence de `Access-Control-Allow-Origin: *` et de réponses d'erreur verbeuses.

### Phase 3 : Analyse manuelle approfondie (Mode test d'intrusion)

Utilisez le Top 10 comme liste de contrôle.

#### API1 : Autorisation au niveau des objets brisée (BOLA)

```bash
# Tentative d'accès aux données d'un autre utilisateur en modifiant l'ID dans l'URL
curl -X GET https://api.example.com/api/v1/users/123 \
  -H "Authorization: Bearer valid_token_for_user_456"
# Si la réponse contient les données de l'utilisateur 123, vous avez une vulnérabilité BOLA.
```

#### API3 : Autorisation au niveau des propriétés d'objet brisée (BOPLA)

```bash
# Affectation massive : essayer d'ajouter "role":"admin" ou "salary":100000 à un PATCH
curl -X PATCH https://api.example.com/api/v1/user/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"test","role":"admin","salary":999999}'
```

#### API6 : Flux métier illimités

```python
import requests
# Simuler un robot abusant d'un flux de vote / coupon / paiement
url = "https://ticketing.example.com/api/v2/checkout"
payload = {"event_id": 1, "quantity": 1}
session = requests.Session()
session.headers.update({"Authorization": "Bearer valid_token"})

for i in range(100):
    r = session.post(url, json=payload)
    print(f"Tentative {i}: {r.status_code} - {r.text[:100]}")
    # Si les 100 réussissent sans limite de débit, API6 est présent.
```

### Phase 4 : Intégration CI/CD

Intégrez les vérifications dans votre pipeline. Une étape de pipeline sécurisée typique ressemble à ceci :

```yaml
# .gitlab-ci.yml (GitLab CI) ou GitHub Actions équivalent
api-security:
  stage: test
  script:
    # Analyse statique pour les motifs BOPLA
    - semgrep --config=auto .
    # Scan dynamique avec ZAP
    - docker run -v $(pwd):/zap/wrk/ zaproxy/zap-stable \
        zap-api-scan.py -t http://staging/api/openapi.json -f openapi
    # Test de limite de débit / abus de flux métier (k6)
    - k6 run tests/abuse.js
  only:
    - branches
```

#### Exemple : Règle Semgrep pour BOPLA (Affectation massive dans Django)

```yaml
rules:
  - id: mass-assignment-django
    patterns:
      - pattern-either:
          - pattern: Model.objects.update(...)  # Non sécurisé si les champs ne sont pas filtrés
          - pattern: serializer.save(...)
    message: >
      Potentielle vulnérabilité d'affectation massive (API3 / BOPLA).
      Définissez explicitement les champs autorisés à l'aide de `fields` ou `read_only_fields` dans le serializer.
    severity: WARNING
    languages:
      - python
```

#### Exemple : Middleware de limite de débit (Go)

```go
import (
    "golang.org/x/time/rate"
    "net/http"
)

var limiter = rate.NewLimiter(rate.Limit(100), 200) // 100 requêtes/s, burst 200

func rateLimitMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if !limiter.Allow() {
            http.Error(w, `{"error":"rate_limit_exceeded"}`, http.StatusTooManyRequests)
            return
        }
        next.ServeHTTP(w, r)
    })
}
```

## La méthodologie « Laver, Rincer, Répéter »

Introduite fortement dans l'édition 2023, ce concept souligne que la sécurité des API **n'est pas un test d'intrusion unique** mais un cycle continu :

1. **Laver :** Découvrez l'ensemble de votre surface API (y compris les API fantômes).
2. **Rincer :** Validez les résultats par des tests automatisés et manuels.
3. **Répéter :** Re-scannée à chaque déploiement d'un nouveau point d'accès ou d'une nouvelle version.

Cela combat directement **API9 (Gestion inappropriée de l'inventaire)** et garantit que la posture de sécurité évolue avec la base de code.

## Relation avec les autres normes

- **PCI DSS 4.0 :** Exige des contrôles de sécurité robustes pour les API (y compris les tests BOLA/BFLA) pour les environnements de données de titulaires de carte.
- **SOC 2 :** Le Top 10 fournit un cadre de contrôle concret pour les critères de disponibilité et de sécurité.
- **ISO 27001 :** Aide à structurer les contrôles de l'Annexe A autour de l'accès logique et de la sécurité opérationnelle.
- **OWASP Web Top 10 :** Complémentaire ; vérifiez toujours les deux listes. Le Top 10 Web couvre l'injection et la cryptographie, tandis que le Top 10 des API couvre les failles logiques et métier.

## Quand NE PAS utiliser le Top 10 de la sécurité des API

- C'est un **document de sensibilisation**, pas une norme de conformité stricte. Considérez-le comme un point de départ, pas une liste de contrôle exhaustive pour un audit.
- Il ne couvre pas en détail la cryptographie, la journalisation ou la sécurité physique (référez-vous à ASVS ou MASVS pour cela).
- Il ne *remplace pas* un modèle de menace adapté à votre architecture spécifique.

## Points clés à retenir

| Risque | Atténuation principale | Exemple de test |
|--------|------------------------|-----------------|
| BOLA | Exiger des vérifications strictes de propriété pour chaque accès à un objet. | Échange d'ID dans les requêtes GET. |
| BOPLA | Utiliser des DTO/ViewModels ; ne jamais passer d'objets utilisateur directement à l'ORM. | Injection de champs `role` ou `admin`. |
| SSRF | Liste de refus des plages IP privées ; liste d'autorisation des destinations sortantes. | Récupération de points d'accès de métadonnées (`169.254.169.254`). |
| Flux métier | Limitation de débit + CAPTCHA pour les actions sensibles. | Automatisation du paiement 100 fois. |
| Inventaire | Maintenir un catalogue d'API vivant dans votre pipeline CI. | Exploration des chemins `v1/`, `swagger.json`, `/debug`. |

## Références

- Projet officiel OWASP API Security : [https://github.com/OWASP/API-Security](https://github.com/OWASP/API-Security)
- OWASP Top 10 Web (2021) : [https://owasp.org/Top10/](https://owasp.org/Top10/)
- Scan d'API OWASP ZAP : [https://www.zaproxy.org/docs/docker/api-scan/](https://www.zaproxy.org/docs/docker/api-scan/)
- Règles Semgrep pour la sécurité des API : [https://semgrep.dev](https://semgrep.dev/)

---

*Statut : brouillon. Dernière mise à jour : 2026-06-25.*