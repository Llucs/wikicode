---
title: Estrategias de Caché para Carga Perezosa y Split de Códigos
description: Una guía completa sobre las estrategias de caché para mejorar el rendimiento de las aplicaciones web mediante la carga perezosa y el split de códigos.
created: 2026-07-03
tags:
  - caché
  - carga perezosa
  - split de códigos
  - rendimiento de la web
status: borrador
---

# Estrategias de Caché para Carga Perezosa y Split de Códigos

## Introducción

En el desarrollo web moderno, la optimización del rendimiento es crucial para brindar una experiencia de usuario suave. La carga perezosa y el split de códigos son dos técnicas que pueden mejorar significativamente el rendimiento de las aplicaciones web. Este guía explorará las estrategias de caché para mejorar tanto la carga perezosa como el split de códigos, proporcionando instrucciones detalladas sobre la implementación y características clave.

## ¿Por qué importa la caché

La caché ayuda a reducir el tiempo de carga de las aplicaciones web al almacenar datos accesados frecuentemente en memoria o en disco. Esto mejora el rendimiento al reducir la necesidad de obtener datos del servidor, especialmente para recursos como imágenes, scripts y estilos.

## Instalación

### Configuración de Webpack para Split de Códigos

Para implementar el split de códigos, podemos usar Webpack. Aquí está cómo configurarlo:

1. **Instalar Webpack y Webpack CLI:**

   ```bash
   npm install --save-dev webpack webpack-cli
   ```

2. **Configurar Webpack:**

   Crea un archivo `webpack.config.js`:

   ```javascript
   const path = require('path');

   module.exports = {
     entry: './src/index.js',
     output: {
       path: path.resolve(__dirname, 'dist'),
       filename: 'bundle.js',
     },
     optimization: {
       splitChunks: {
         chunks: 'all',
       },
     },
   };
   ```

3. **Instalar dependencias adicionales:**

   ```bash
   npm install --save-dev mini-css-extract-plugin html-webpack-plugin
   ```

4. **Actualizar la configuración de Webpack:**

   ```javascript
   const path = require('path');
   const HtmlWebpackPlugin = require('html-webpack-plugin');
   const MiniCssExtractPlugin = require('mini-css-extract-plugin');

   module.exports = {
     entry: './src/index.js',
     output: {
       path: path.resolve(__dirname, 'dist'),
       filename: 'bundle.js',
     },
     module: {
       rules: [
         {
           test: /\.css$/,
           use: [MiniCssExtractPlugin.loader, 'css-loader'],
         },
         {
           test: /\.js$/,
           exclude: /node_modules/,
           use: {
             loader: 'babel-loader',
           },
         },
       ],
     },
     plugins: [
       new HtmlWebpackPlugin({
         template: './public/index.html',
       }),
       new MiniCssExtractPlugin({
         filename: '[name].css',
         chunkFilename: '[id].css',
       }),
     ],
     optimization: {
       splitChunks: {
         cacheGroups: {
           vendor: {
             test: /[\\/]node_modules[\\/]/,
             name: 'vendors',
             chunks: 'all',
           },
         },
       },
     },
   };
   ```

5. **Crear un archivo de plantilla HTML:**

   Crea un archivo `public/index.html`:

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>Ejemplo de Carga Perezosa y Split de Códigos</title>
   </head>
   <body>
     <h1>Ejemplo de Carga Perezosa y Split de Códigos</h1>
     <div id="app"></div>
     <script src="bundle.js"></script>
     <link rel="stylesheet" href="main.css">
   </body>
   </html>
   ```

6. **Crear un archivo de entrada simple:**

   Crea un archivo `src/index.js`:

   ```javascript
   import './styles/main.css';
   import App from './App';

   const appContainer = document.getElementById('app');
   const app = new App();
   appContainer.appendChild(app.el);
   ```

7. **Iniciar el servidor de desarrollo:**

   ```bash
   npx webpack serve --config webpack.config.js
   ```

### Configuración de Caché HTTP

Para habilitar la caché HTTP, puedes usar un middleware como `express-cache` para aplicaciones Node.js.

1. **Instalar `express-cache`:**

   ```bash
   npm install express-cache
   ```

2. **Configurar `express-cache`:**

   Crea un archivo `cache.js`:

   ```javascript
   const express = require('express');
   const cache = require('express-cache');

   const app = express();

   app.use(cache({
     maxAge: 3600, // Caché durante 1 hora
     cacheControl: true,
     cacheRefresh: true,
   }));

   app.get('/api/data', (req, res) => {
     res.send('Datos Cachados');
   });

   app.listen(3000, () => {
     console.log('Servidor en ejecución en el puerto 3000');
   });
   ```

## Uso

### Carga Perezosa con Webpack

La carga perezosa se logra al dividir el código en trozos más pequeños utilizando Webpack. Esto se hace marcando ciertos módulos como perezosos utilizando la función `React.lazy` y el componente `React.Suspense`.

1. **Crear un componente cargado perezosamente:**

   ```javascript
   const MyLazyComponent = React.lazy(() => import('./MyComponent'));
   ```

2. **Envolver el componente cargado perezosamente con `React.Suspense`:**

   ```javascript
   <React.Suspense fallback={<div>Cargando...</div>}>
     <MyLazyComponent />
   </React.Suspense>
   ```

### Caché HTTP

Para habilitar la caché HTTP, se deben establecer los encabezados `Cache-Control` en las respuestas de la API.

1. **Establecer encabezados `Cache-Control` en Express:**

   ```javascript
   app.get('/api/data', (req, res) => {
     res.setHeader('Cache-Control', 'public, max-age=3600');
     res.send('Datos Cachados');
   });
   ```

## Características Clave

### Webpack

- **Split de Códigos:** Divide el código en trozos más pequeños de forma automática.
- **Tree Shaking:** Elimina el código no utilizado del paquete final.
- **SplitChunks:** Optimiza el tamaño y el número de trozos.

### Express Cache

- **Max Age:** Controla la duración de la caché.
- **Cache Control:** Gestionar el comportamiento de la caché.
- **Cache Refresh:** Asegura que los datos cachados sean actualizados después de un período determinado.

### Ejemplos de Comandos

#### Comando Serve de Webpack

```bash
npx webpack serve --config webpack.config.js
```

#### Comando de Express Cache

```javascript
node cache.js
```

## Conclusión

La implementación de estrategias de caché, carga perezosa y split de códigos puede mejorar significativamente el rendimiento de las aplicaciones web. Siguiendo los pasos detallados en esta guía, puedes mejorar la experiencia del usuario y optimizar el rendimiento de tu aplicación.