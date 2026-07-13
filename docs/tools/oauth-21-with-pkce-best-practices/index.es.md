---
title: Mejores prácticas para OAuth 2.1 con PKCE
description: Guías detalladas para asegurar implementaciones de OAuth 2.1 utilizando el intercambio de Clave de Código (PKCE) para prevenir ataques de inyección de código de autorización.
created: 2026-07-13
tags:
  - OAuth
  - PKCE
  - Seguridad
  - API
status: borrador
---

# Mejores prácticas para OAuth 2.1 con PKCE

OAuth 2.1 con el intercambio de Clave de Código (PKCE) es una extensión del protocolo que mejora la seguridad del marco de autorización OAuth 2.0. PKCE está diseñado específicamente para mitigar el riesgo de interceptación del código de autorización, lo cual puede ocurrir en clientes públicos (como aplicaciones móviles o aplicaciones de una sola página) que carecen de formas seguras para mantener los secretos del cliente confidenciales.

## Características clave

1. **Verificador de Código/Desafío**: Una cadena aleatoria generada por el cliente para generar el desafío PKCE. El verificador de código se mantiene en secreto y no se envía a través de la red.
2. **Desafío de Código**: Una hash del verificador de código, que se envía al servidor de autorización.
3. **Flujo de Autorización por Código de Autorización**: El flujo permanece en gran medida igual, pero con la adición de PKCE.

## Historia

OAuth 2.1 con PKCE fue introducido como una extensión de OAuth 2.0 para abordar las preocupaciones de seguridad en la autenticación del cliente. Fue propuesto por primera vez en RFC 7636 e integrado más tarde en la especificación de OAuth 2.1.

## Casos de uso

- **Clientes Públicos**: Aplicaciones móviles, aplicaciones de una sola página y cualquier cliente que no pueda almacenar secretos del cliente de forma segura.
- **Seguridad de API**: Mejorar la seguridad del acceso y la autenticación de las API para aplicaciones web y móviles.
- **Aplicaciones Web**: Mejorar la seguridad de las aplicaciones web que utilizan OAuth para autenticación.

## Instalación

Aunque OAuth 2.1 con PKCE es una extensión de protocolo, su implementación generalmente implica los siguientes pasos:

1. **Implementación del Lado del Cliente**:
   - Generar un verificador de código y un desafío de código.
   - Usar el desafío de código en la solicitud de autorización.
   - Administrar la respuesta de autorización y intercambiar el código de autorización por un token de acceso.

2. **Implementación del Lado del Servidor**:
   - Validar el desafío de código contra el verificador de código.
   - Administrar la respuesta de autorización y intercambiar el código de autorización por un token de acceso.

### Uso básico

1. **Autenticación del Cliente**:
   - El cliente genera un verificador de código y un desafío de código.
   - El desafío de código se incluye en la solicitud de autorización.

2. **Respuesta de Autorización**:
   - El usuario aprueba o deniega el acceso.
   - El servidor de autorización responde con un código de autorización.

3. **Solicitud de Token**:
   - El cliente intercambia el código de autorización por un token de acceso utilizando el verificador de código.

4. **Validación**:
   - El servidor de autorización verifica el desafío de código y el verificador de código para asegurar la autenticidad del cliente.

## Mejores prácticas

1. **Usar Verificadores de Código Fuertes**:
   - Generar verificadores de código utilizando un generador de números pseudoaleatorios criptográficamente seguro (CSPRNG).
   - Asegurarse de que el verificador de código tenga al menos 43 caracteres de longitud para mitigar los ataques de tiempo.

2. **Métodos de Desafío de Código**:
   - Usar el método `S256` para hashear el verificador de código. Este método está diseñado para ser seguro contra los ataques de tiempo.

3. **Autenticación del Cliente**:
   - Usar métodos de autenticación del cliente que sean apropiados para el tipo de cliente (por ejemplo, `client_secret_basic` para clientes confidenciales, `none` para clientes públicos).

4. **Seguridad de la Transferencia**:
   - Asegurarse de que toda la comunicación se realice mediante HTTPS para proteger el desafío de código y otras informaciones sensibles.

5. **Gestión de Sesiones**:
   - Implementar la gestión de sesiones adecuada para asegurar que el código de autorización no se reutilice.

6. **Auditorías y Actualizaciones Regulares**:
   - Realizar revisiones y actualizaciones regulares para mantenerse actualizado con las últimas prácticas y estándares de seguridad.

7. **Limitación de Tasa**:
   - Implementar la limitación de tasa para prevenir el abuso y los ataques de fuerza bruta.

8. **Registros y Vigilancia**:
   - Registrar y monitorear las solicitudes y respuestas de autorización para detectar y responder de manera prompt a actividades sospechosas.

Al seguir estas mejores prácticas, puedes mejorar la seguridad de tu implementación de OAuth 2.1 con PKCE, asegurando la protección de la información sensible y manteniendo tu aplicación segura.

## Ejemplo: Implementación en Python

Aquí tienes un ejemplo básico de implementación de PKCE en Python utilizando la biblioteca `requests`:

```python
import requests
import string
import random
import hashlib

# Generar un verificador de código
def generate_code_verifier(length=43):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(length))

# Generar un desafío de código
def generate_code_challenge(verifier):
    sha256 = hashlib.sha256()
    sha256.update(verifier.encode('utf-8'))
    return sha256.hexdigest()[:43]

# Ejemplo de autenticación del cliente
def authenticate_client(authorization_url, client_id, redirect_uri, code_verifier):
    # Generar el desafío de código
    code_challenge = generate_code_challenge(code_verifier)

    # Solicitud de autorización
    auth_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge
    }

    response = requests.get(authorization_url, params=auth_params)
    if response.status_code != 200:
        raise Exception("Falló la autenticación del cliente")

    # Administrar la interacción del usuario y obtener el código de autorización

    # Solicitud de token
    token_params = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier
    }

    token_response = requests.post(token_url, data=token_params, auth=(client_id, 'client_secret'))
    if token_response.status_code != 200:
        raise Exception("Falló el intercambio por el token de acceso")

    return token_response.json()

# Uso
client_id = 'tu_id_de_cliente'
redirect_uri = 'http://tu-redirección-uri'
authorization_url = 'https://tu-servidor-de-autorización'
code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)
access_token = authenticate_client(authorization_url, client_id, redirect_uri, code_verifier)
print("Token de Acceso:", access_token['access_token'])
```

Este ejemplo demuestra cómo generar un verificador y desafío de código, realizar la solicitud de autorización y intercambiar el código de autorización por un token de acceso.

## Conclusión

OAuth 2.1 con PKCE es una mejora crucial de seguridad para las implementaciones de OAuth 2.0. Al seguir las mejores prácticas indicadas en este guía, puedes mejorar significativamente la seguridad de tus aplicaciones basadas en OAuth.