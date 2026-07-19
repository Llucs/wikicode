---
title: OAuth 2.1 con PKCE y Enlace de Tokens
description: Un guía completo para implementar OAuth 2.1 con PKCE y Enlace de Tokens para un mayor nivel de seguridad en aplicaciones web y móviles.
created: 2026-07-19
tags:
  - OAuth
  - PKCE
  - Enlace de Tokens
  - Seguridad
  - Autenticación
status: borrador
---

# OAuth 2.1 con PKCE y Enlace de Tokens

OAuth 2.1 es la última versión del protocolo OAuth 2.0, ampliamente utilizado para la autorización y autenticación en aplicaciones web y móviles. OAuth 2.1 introduce varias mejoras y nuevas características para incrementar la seguridad y la usabilidad, particularmente a través de la integración de PKCE (Proof Key for Code Exchange) y Enlace de Tokens.

## Características clave de OAuth 2.1

1. **Mejoras de Seguridad**: OAuth 2.1 enhances security by addressing common vulnerabilities and implementing new security measures.
2. **PKCE (Proof Key for Code Exchange)**: Esta característica es crucial para prevenir la intercepción de códigos de autorización, especialmente en clientes públicos (como aplicaciones móviles y aplicaciones de una sola página) que no pueden almacenar secretos de cliente de forma segura.
3. **Enlace de Tokens**: Esta característica asegura que los tokens estén vinculados a un cliente o dispositivo específico, incrementando la seguridad del uso de tokens.
4. **Registro de Clientes Dinámico**: OAuth 2.1 permite a los clientes registrarse dinámicamente durante el proceso de autorización, haciendo que sea más flexible y adaptable.
5. **Mejores Mecanismos de Consentimiento**: Los flujos de consentimiento mejorados permiten a los usuarios gestionar de forma más sencilla su autorización y acceso a los recursos.

## Historia

- **OAuth 2.0**: La versión inicial de OAuth 2.0 se lanzó en 2012 y se ha convertido en el estándar de hecho para la autorización en la web.
- **OAuth 2.1**: OAuth 2.1 fue oficialmente lanzado en 2022, incorporando nuevas medidas de seguridad y mejoras para abordar amenazas de seguridad y necesidades del usuario que se han ido evolucionando.

## Casos de Uso

1. **Aplicaciones Web**: OAuth 2.1 es ideal para aplicaciones web que requieren una autenticación y autorización seguras.
2. **Aplicaciones Móviles**: Soporta tanto clientes públicos como confidenciales, lo que la hace adecuada para aplicaciones móviles.
3. **Integración de API**: OAuth 2.1 facilita la integración segura y eficiente de API entre diferentes sistemas.
4. **Dispositivos IoT**: La característica de enlace de tokens puede ser especialmente útil para asegurar tokens en dispositivos IoT.

## Instalación

OAuth 2.1 se integra generalmente como parte del protocolo OAuth 2.0, por lo que no se requiere instalación adicional. Sin embargo, necesitarás implementar los cambios necesarios en tu aplicación para soportar las características de OAuth 2.1 como PKCE y Enlace de Tokens.

1. **Regístrate con un Proveedor de OAuth**: Obtiene las credenciales (identificador de cliente y secreto de cliente) de tu proveedor de OAuth elegido.
2. **Configura Tu Aplicación**: Modifica tu aplicación para incluir el soporte de OAuth 2.1.
3. **Implementa PKCE**: Asegúrate de que tu aplicación genere y verifique un desafío de código y un verificador de código para clientes públicos.
4. **Implementa Enlace de Tokens**: Vincula tokens a dispositivos o clientes específicos para prevenir su mal uso.

## Uso Básico

1. **Autorización del Usuario**:
   - Redirige al usuario al punto de autorización del proveedor de OAuth.
   - El proveedor le pide al usuario su consentimiento.
   - Al conceder el consentimiento, el proveedor genera un código de autorización.

2. **Autenticación del Cliente**:
   - El cliente intercambia el código de autorización por un token de acceso enviando una solicitud de token al punto de final de token.
   - Esta solicitud incluye el código de autorización, las credenciales del cliente (si es necesario) y el verificador de código (para PKCE).

3. **Enlace de Tokens**:
   - Para el enlace de tokens, el cliente debe especificar el contexto de enlace de tokens en la solicitud de token.
   - El proveedor entonces enlaza el token a este contexto, asegurándose de que el token solo se pueda usar en este contexto específico.

4. **Acceso a Recursos**:
   - Utiliza el token de acceso para hacer solicitudes de API en nombre del usuario.
   - El token debe incluirse en los encabezados o parámetros de la URL según lo especifique el proveedor.

## Ejemplo

Aquí tienes un ejemplo simplificado de cómo podría implementarse PKCE en una aplicación web:

1. **Aplicación Cliente**:
   ```csharp
   string clientID = "tu-identificador-de-cliente";
   string clientSecret = "tu-secreto-de-cliente";
   string redirectURI = "https://tu-app.com/callback";
   string authorizationEndpoint = "https://proveedor-oauth.com/authorize";
   string tokenEndpoint = "https://proveedor-oauth.com/token";

   // Genera un verificador de código
   string codeVerifier = GenerarVerificadorDeCodigoAleatorio();
   string codeVerifierBase64Url = Base64UrlEncode(codeVerifier);

   // Deriva un desafío de código utilizando una función de hash criptográfica
   string codeChallenge = GenerarDesafioDeCodigo(codeVerifierBase64Url);

   // Redirige al usuario al punto de autorización con el desafío de código
   string authorizationUrl = $"{authorizationEndpoint}?response_type=code&client_id={clientID}&redirect_uri={redirectURI}&scope=profile%20email&code_challenge={codeChallenge}&code_challenge_method=S256";
   Redirigir(authorizationUrl);
   ```

2. **Servidor de Autorización**:
   - Después del consentimiento del usuario, genera un código de autorización.
   - Redirige de vuelta al cliente con el código de autorización y el parámetro de estado.

3. **Aplicación Cliente**:
   ```csharp
   string authorizationCode = ObtenerCódigoDeAutorizaciónDelRespuesta();
   string redirectURI = "https://tu-app.com/callback";
   string codeVerifierBase64Url = Base64UrlEncode(codeVerifier);

   // Intercambia el código de autorización por un token de acceso
   string tokenRequestUrl = $"{tokenEndpoint}?grant_type=authorization_code&client_id={clientID}&redirect_uri={redirectURI}&code={authorizationCode}&code_verifier={codeVerifierBase64Url}";

   var httpClient = new HttpClient();
   var response = await httpClient.PostAsync(tokenRequestUrl, null);
   var responseContent = await response.Content.ReadAsStringAsync();

   // Analiza la respuesta para obtener el token de acceso
   var tokenResponse = JsonConvert.DeserializeObject<TokenResponse>(responseContent);
   string accessToken = tokenResponse.AccessToken;
   ```

Este ejemplo destaca los pasos clave para utilizar OAuth 2.1 con PKCE. Los detalles específicos de la implementación variarán según el proveedor de OAuth y el lenguaje de programación utilizado.