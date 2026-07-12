---
title: Recomendaciones de longitud del Verificador de Código para PKCE de OAuth 2.1
description: Guía para implementar PKCE de OAuth 2.1 con recomendaciones sobre la longitud del verificador de código para mejorar la seguridad.
created: 2026-07-12
tags:
  - OAuth
  - PKCE
  - Seguridad
status: borrador
---

# Recomendaciones de longitud del Verificador de Código para PKCE de OAuth 2.1

## ¿Qué es PKCE?

PKCE (Proof Key for Code Exchange) es una mécanica de seguridad utilizada en OAuth 2.0 para prevenir que los atacantes obtengan el código de autorización. Añade una capa adicional de seguridad al requerir un clave única y no reutilizable (el verificador de código) que se intercambia entre el cliente y el servidor de autorización.

## Características clave de PKCE de OAuth 2.1

- **Verificador de Código**: Una cadena aleatoria usada como secreto entre el cliente y el servidor de autorización.
- **Desafío de Código**: Un hash del verificador de código, usado para prevenir la captura de paquetes en la red.
- **Nonce**: Un valor único incluido en la solicitud de autorización para asegurar que el código se utilice solo una vez.

## Historia de PKCE

PKCE se introdujo como una mécanica opcional en OAuth 2.0 para mejorar la seguridad. Sin embargo, se convirtió en una parte obligatoria de la especificación de OAuth 2.1 para garantizar un nivel más alto de seguridad, especialmente para clientes públicos.

## Casos de uso de PKCE

- **Clientes Públicos**: Clientes que no pueden almacenar secretos de manera segura, como aplicaciones web y aplicaciones móviles.
- **Flujo Híbrido**: Adecuado para escenarios donde el cliente necesita intercambiar el código de autorización por un token de acceso.
- **Flujo de Código de Autorización**: Mejora la seguridad en escenarios donde el cliente redirige al usuario a un servidor de autorización.

## Longitud recomendada del Verificador de Código

La longitud del verificador de código es un aspecto crítico de la seguridad de PKCE. El verificador de código debe ser lo suficientemente largo como para resistir ataques de fuerza bruta, pero lo suficientemente corto como para ser manejable en implementaciones del cliente.

### Longitudes recomendadas

- **Longitud mínima**: 43 caracteres
- **Longitud recomendada**: 128 caracteres o más

La longitud más larga del verificador de código proporciona una resistencia mayor a los ataques de fuerza bruta. La longitud mínima de 43 caracteres se recomienda según la especificación de OAuth 2.1 para proporcionar un nivel razonable de seguridad. Sin embargo, el uso de un verificador de código más largo, como 128 caracteres, proporciona una margen de seguridad significativamente mayor.

## Instalación y Uso Básico

### Paso 1: Generar el Verificador de Código

```python
import random
import string

def generar_verificador_de_código(longitud=128):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=longitud))
```

### Paso 2: Generar el Desafío de Código

```python
import hashlib
import base64

def generar_desafío_de_código(verificador_de_código):
    desafío_de_código = hashlib.sha256(verificador_de_código.encode()).digest()
    return base64.urlsafe_b64encode(desafío_de_código).rstrip(b'=').decode()
```

### Paso 3: Incluir PKCE en el Flujo de OAuth 2.0

1. **Solicitud de Autorización**:
   - Incluir el `desafío_de_código` y `code_challenge_method` en la solicitud de autorización.
   - Ejemplo:
     ```http
     GET /authorize?response_type=code&client_id=your_client_id&redirect_uri=https%3A%2F%2Fyourapp.com%2Fcallback&code_challenge=your_code_challenge&code_challenge_method=S256&state=some_state_value&nonce=some_nonce_value
     ```

2. **Solicitud de Token**:
   - Incluir el `verificador_de_código` en la solicitud de token.
   - Ejemplo:
     ```http
     POST /token HTTP/1.1
     Host: your_authorization_server.com
     Content-Type: application/x-www-form-urlencoded

     grant_type=authorization_code&code=your_authorization_code&redirect_uri=https%3A%2F%2Fyourapp.com%2Fcallback&code_verifier=your_code_verifier
     ```

## Conclusión

Usar PKCE con un verificador de código lo suficientemente largo (al menos 128 caracteres) es crucial para mejorar la seguridad de los flujos de OAuth 2.0, especialmente en escenarios de clientes públicos. Siguiendo las recomendaciones, los desarrolladores pueden asegurar un nivel más alto de seguridad para sus aplicaciones.