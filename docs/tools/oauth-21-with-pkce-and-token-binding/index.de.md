---
title: OAuth 2.1 mit PKCE und Token Binding
description: Ein umfassender Leitfaden zur Implementierung von OAuth 2.1 mit PKCE und Token Binding für eine verstärkte Sicherheit in Web- und Mobilanwendungen.
created: 2026-07-19
tags:
  - OAuth
  - PKCE
  - Token Binding
  - Sicherheit
  - Authentifizierung
status: draft
---

# OAuth 2.1 mit PKCE und Token Binding

OAuth 2.1 ist die neueste Version des OAuth 2.0 Protokolls, das für die Authentifizierung und Autorisierung in Web- und Mobilanwendungen weit verbreitet ist. OAuth 2.1 führt mehrere Verbesserungen und neue Funktionen ein, um die Sicherheit und Benutzerfreundlichkeit zu verbessern, insbesondere durch die Integration von PKCE (Proof Key for Code Exchange) und Token Binding.

## Schlüsselereignisse von OAuth 2.1

1. **Sicherheitsverbesserungen**: OAuth 2.1 verbessert die Sicherheit, indem er allgemeine Schwachstellen adressiert und neue Sicherheitsmaßnahmen implementiert.
2. **PKCE (Proof Key for Code Exchange)**: Diese Funktion ist für die Verhinderung des Interceptions des Autorisierungs-Codes entscheidend, insbesondere bei öffentlichen Clients (wie Mobilanwendungen und Single-Page-Anwendungen), die keine sicheren Speicherung von Clientsecrets zulassen.
3. **Token Binding**: Diese Funktion sorgt dafür, dass Tokens sich spezifischen Clients oder Geräten zuordnen, was die Verwendung von Tokens verstärkt sichert.
4. **Dynamische Clientregistrierung**: OAuth 2.1 ermöglicht es Clients, sich während des Autorisierungsprozesses dynamisch zu registrieren, was es flexibler und anpassungsfähiger macht.
5. **Verbesserte Zustimmungsmechanismen**: Verbesserte Zustimmungsflüsse ermöglichen es Nutzern, ihre Autorisierung und Zugriff auf Ressourcen besser zu verwalten.

## Geschichte

- **OAuth 2.0**: Die ursprüngliche Version von OAuth 2.0 wurde 2012 veröffentlicht und ist seitdem der de facto Standard für die Autorisierung im Web geworden.
- **OAuth 2.1**: OAuth 2.1 wurde 2022 offiziell veröffentlicht und integriert neue Sicherheitsmaßnahmen und Verbesserungen, um sich an sich ändernde Sicherheitsbedrohungen und Nutzerverhältnisse anzupassen.

## Nutzungsszenarien

1. **Webanwendungen**: OAuth 2.1 ist ideal für Webanwendungen, die sichere Benutzerauthentifizierung und -autorisierung benötigen.
2. **Mobilanwendungen**: Es unterstützt sowohl öffentliche als auch vertrauliche Clients, sodass es auch für Mobilanwendungen geeignet ist.
3. **API-Integration**: OAuth 2.1 erleichtert die sichere und effiziente Integration von APIs zwischen verschiedenen Systemen.
4. **IoT-Geräte**: Das Token Binding-Feature kann besonders für die Sicherung von Tokens auf IoT-Geräten nützlich sein.

## Installation

OAuth 2.1 wird in der Regel als Teil des OAuth 2.0-Protokolls integriert, sodass keine separate Installation erforderlich ist. Allerdings müssen Sie Änderungen an Ihrem Anwendungscode umsetzen, um OAuth 2.1-Funktionen wie PKCE und Token Binding zu unterstützen.

1. **Registrierung bei einem OAuth-Provider**: Erhalten Sie Berechtigungen (Client-ID und Client-Secret) von Ihrer gewählten OAuth-Provider.
2. **Konfigurieren Ihres Anwendungs-Codes**: Ändern Sie Ihre Anwendung, um OAuth 2.1-Unterstützung hinzuzufügen.
3. **PKCE implementieren**: Stellen Sie sicher, dass Ihr Anwendungscode einen Code-Challenge und einen Code-Verifier für öffentliche Clients generiert und verifiziert.
4. **Token Binding implementieren**: Fügen Sie Tokens spezifischen Geräten oder Clients zu, um Missbrauch zu verhindern.

## Grundlegende Nutzung

1. **Benutzerautorisierung**:
   - Führen Sie den Benutzer zur Autorisierungs-Endpunkt des OAuth-Providers um.
   - Der Provider fordert den Benutzer auf, die Zustimmung zu geben.
   - Nach Zustimmung generiert der Provider einen Autorisierungscode.

2. **Clientauthentifizierung**:
   - Der Client tauscht den Autorisierungscode gegen einen Zugriffstoken aus, indem er einen Token-Anfrage an den Token-Endpunkt sendet.
   - Diese Anfrage enthält den Autorisierungscode, die Client-Berechtigungen (falls erforderlich) und den Code-Verifier (für PKCE).

3. **Token Binding**:
   - Bei Token Binding müssen Sie den Token-Verbindungs-Kontext im Token-Anfrage angeben.
   - Der Provider bindet das Token dann an diesen Kontext, was sicherstellt, dass das Token nur im spezifischen Kontext verwendet werden kann.

4. **Ressourcenabfrage**:
   - Verwenden Sie den Zugriffstoken, um Ressourcen im Namen des Benutzers abzurufen.
   - Das Token muss in den Anfrage-Header oder die URL-Parameter wie von dem Provider vorgegeben enthalten sein.

## Beispiel

Hier ist ein vereinfachtes Beispiel für die Implementierung von PKCE in einer Webanwendung:

1. **Clientanwendung**:
   ```csharp
   string clientID = "deine-client-ID";
   string clientSecret = "dein-client-Secret";
   string redirectURI = "https://deine-anwendung.com/callback";
   string authorizationEndpoint = "https://oauth-provider.com/authorize";
   string tokenEndpoint = "https://oauth-provider.com/token";

   // Generieren Sie einen Code-Verifizierer
   string codeVerifier = GeneriereZufälligenCodeVerifizierer();
   string codeVerifierBase64Url = Base64UrlEncode(codeVerifier);

   // Erstellen Sie einen Code-Challenge mit einem kryptografischen Hash-Funktion
   string codeChallenge = GeneriereCodeChallenge(codeVerifierBase64Url);

   // Führen Sie den Benutzer zur Autorisierungs-URL um, mit dem Code-Challenge
   string authorizationUrl = $"{authorizationEndpoint}?response_type=code&client_id={clientID}&redirect_uri={redirectURI}&scope=profile%20email&code_challenge={codeChallenge}&code_challenge_method=S256";
   Redirect(authorizationUrl);
   ```

2. **Autorisierungs-Server**:
   - Nach Zustimmung des Benutzers generiert der Provider einen Autorisierungscode.
   - Der Benutzer wird mit dem Autorisierungscode und dem Zustand-Parameter zurückgeleitet.

3. **Clientanwendung**:
   ```csharp
   string authorizationCode = AbholenDesAutorisierungsCodesVomAntworten();
   string redirectURI = "https://deine-anwendung.com/callback";
   string codeVerifierBase64Url = Base64UrlEncode(codeVerifier);

   // Tauschen Sie den Autorisierungscode gegen ein Zugriffstoken aus
   string tokenRequestUrl = $"{tokenEndpoint}?grant_type=authorization_code&client_id={clientID}&redirect_uri={redirectURI}&code={authorizationCode}&code_verifier={codeVerifierBase64Url}";

   var httpClient = new HttpClient();
   var response = await httpClient.PostAsync(tokenRequestUrl, null);
   var responseContent = await response.Content.ReadAsStringAsync();

   // Analysieren Sie die Antwort, um das Zugriffstoken abzurufen
   var tokenResponse = JsonConvert.DeserializeObject<TokenResponse>(responseContent);
   string accessToken = tokenResponse.AccessToken;
   ```

Dieses Beispiel verdeutlicht die wesentlichen Schritte zur Nutzung von OAuth 2.1 mit PKCE. Die spezifischen Implementierungsdetails können anhand des OAuth-Providers und der verwendeten Programmiersprache variieren.

## Zusammenfassung

OAuth 2.1 mit PKCE und Token Binding bietet eine verstärkte Sicherheit und Flexibilität bei der Implementierung von Autorisierung und Authentifizierung in verschiedenen Anwendungen. Durch die Einhaltung der Leitlinien und der besten Praktiken können Entwickler sicherstellen, dass ihre Anwendungen sicheren und an den neuesten Standards halten.