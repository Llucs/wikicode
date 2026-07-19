---
title: Crear un Proyecto de API REST Real en TypeScript
description: Una guía completa para construir una API REST sólida utilizando TypeScript, Express.js y MongoDB.
created: 2026-07-19
tags:
  - TypeScript
  - Express.js
  - MongoDB
  - API REST
  - Autenticación
  - Docker
status: borrador
---

# Crear un Proyecto de API REST Real en TypeScript

Esta guía te guía a través del proceso de construir una API REST sólida utilizando TypeScript, Express.js y MongoDB. Incluye documentación detallada, mejores prácticas y ejemplos del mundo real para ayudarte a entender e implementar una solución de API lista para producción.

## Características Principales

1. **TypeScript**: Tipado estático para una mejor detección de errores y calidad del código.
2. **Express.js**: Un framework de aplicaciones web popular de Node.js.
3. **MongoDB**: Una base de datos NoSQL de documentos para almacencamiento de datos.
4. **Autenticación con JWT**: Rutas seguras utilizando Tokens de Web JSON (JWT).
5. **Mongoose**: Una biblioteca de modelo de objeto (ODM) para MongoDB.
6. **Pruebas**: Pruebas de unidad e integración con Jest y Supertest.
7. **Documentación con Swagger**: Documentación de la API generada automáticamente para fácil referencia.

## Instalación

1. **Clona el Repositorio**:
   ```sh
   git clone https://github.com/username/repo.git
   cd repo
   ```

2. **Instala Dependencias**:
   ```sh
   npm install
   ```

3. **Configura MongoDB**:
   - Instala MongoDB si no está instalado.
   - Inicia el servidor de MongoDB.
   - Configura la cadena de conexión en el archivo `.env`.

4. **Configura Variables de Entorno**:
   - Actualiza el archivo `.env` con las variables de entorno necesarias, como la cadena de conexión de la base de datos, la secret de JWT, etc.

5. **Ejecuta el Servidor**:
   ```sh
   npm start
   ```

## Uso Básico

### Rutas de API

1. **Administración de Usuarios**:
   - **Crear Usuario**: POST `/api/users`
   - **Obtener Usuario**: GET `/api/users/:id`
   - **Actualizar Usuario**: PATCH `/api/users/:id`
   - **Eliminar Usuario**: DELETE `/api/users/:id`

2. **Administración de Productos**:
   - **Crear Producto**: POST `/api/products`
   - **Obtener Producto**: GET `/api/products/:id`
   - **Actualizar Producto**: PATCH `/api/products/:id`
   - **Eliminar Producto**: DELETE `/api/products/:id`

3. **Administración de Pedidos**:
   - **Crear Pedido**: POST `/api/orders`
   - **Obtener Pedido**: GET `/api/orders/:id`
   - **Actualizar Pedido**: PATCH `/api/orders/:id`
   - **Eliminar Pedido**: DELETE `/api/orders/:id`

4. **Autenticación**:
   - **Generar Token JWT**: POST `/api/auth/login`
   - **Proteger Rutas**: Utilizar el token JWT en la cabecera `Authorization`

### Pruebas

1. **Pruebas de Unidad**:
   - Utiliza Jest para pruebas de unidad.
   - Ejecuta las pruebas con:
     ```sh
     npm test
     ```

2. **Pruebas de Integración**:
   - Utiliza Supertest para pruebas de integración.
   - Ejecuta las pruebas con:
     ```sh
     npm test
     ```

### Documentación con Swagger

1. **Acceder a Swagger UI**:
   - Navega a `http://localhost:3000/docs` en tu navegador.
   - Usa la documentación generada para entender e interactuar con la API.

### Autenticación

1. **Generar Token JWT**:
   - Realiza una solicitud POST a `/api/auth/login` con las credenciales del usuario.
   - Ejemplo usando `curl`:
     ```sh
     curl -X POST http://localhost:3000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password"}'
     ```

2. **Incluir JWT en Solicitudes**:
   - Utiliza el token JWT en la cabecera `Authorization` para rutas protegidas.
   - Ejemplo usando `curl`:
     ```sh
     curl -X GET http://localhost:3000/api/users/1 \
     -H "Authorization: Bearer <JWT_TOKEN>"
     ```

### Gestión de Datos

1. **Definir Esquemas Mongoose**:
   - Usa Mongoose para definir los esquemas para los modelos.
   - Ejemplo de esquema para un Usuario:
     ```typescript
     import { Schema, model } from 'mongoose';

     const UserSchema = new Schema({
       name: String,
       email: { type: String, unique: true },
       password: String
     });

     export const User = model('User', UserSchema);
     ```

2. **Realizar Operaciones CRUD**:
   - Usa los métodos de Mongoose para realizar operaciones CRUD.
   - Ejemplo para crear un usuario:
     ```typescript
     import { Request, Response } from 'express';
     import User from '../models/User';

     const createUser = async (req: Request, res: Response) => {
       const { name, email, password } = req.body;
       const user = new User({ name, email, password });
       await user.save();
       res.status(201).json(user);
     };
     ```

## Conclusión

Siguiendo la guía detallada y utilizando la base de código proporcionada como punto de partida, puedes extender y personalizar la API para cumplir con los requisitos del proyecto específicos. Este proyecto completo no solo proporciona un ejemplo práctico, sino que también sirve como una excelente herramienta de aprendizaje para comprender las mejores prácticas modernas de desarrollo web con TypeScript, Express.js y MongoDB.

¡Feliz codificación!