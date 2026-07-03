---
title: Cachingstrategien für lazes Laden und Code-Splitting
description: Ein umfassender Leitfaden zur Implementierung von Cachingstrategien für die Verbesserung der Leistung von Webanwendungen durch lazes Laden und Code-Splitting.
created: 2026-07-03
tags:
  - Caching
  - lazes Laden
  - Code-Splitting
  - Web-Leistung
status: Entwurf
---

# Cachingstrategien für lazes Laden und Code-Splitting

## Einführung

In moderner Webentwicklung ist die Optimierung der Leistung entscheidend für die Bereitstellung einer glatten Benutzererfahrung. Lazes Laden und Code-Splitting sind zwei Techniken, die die Leistung von Webanwendungen erheblich verbessern können. In diesem Leitfaden werden Cachingstrategien zu deren Verbesserung behandelt, wobei detaillierte Anweisungen zur Implementierung und wichtige Funktionen bereitgestellt werden.

## Warum zählt Caching

Caching hilft, die Ladezeit von Webanwendungen zu senken, indem häufig benutzte Daten in der Arbeitsspeicher oder auf dem Festplatte gespeichert werden. Dies reduziert die Notwendigkeit, Daten von der Serverseite abzurufen, insbesondere für Ressourcen wie Bilder, Skripte und Stylesheets.

## Installation

### Webpack für Code-Splitting einrichten

Um Code-Splitting umzusetzen, können wir Webpack nutzen. Hier ist, wie es so eingerichtet wird:

1. **Webpack und Webpack CLI installieren:**

   ```bash
   npm install --save-dev webpack webpack-cli
   ```

2. **Webpack konfigurieren:**

   Erstelle eine `webpack.config.js`-Datei:

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

3. **Zusätzliche Abhängigkeiten installieren:**

   ```bash
   npm install --save-dev mini-css-extract-plugin html-webpack-plugin
   ```

4. **Webpack-Konfiguration aktualisieren:**

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

5. **Erstellen eines HTML-Vorlagenblatts:**

   Erstelle eine `public/index.html`-Datei:

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>Lazy Loading and Code Splitting</title>
   </head>
   <body>
     <h1>Lazy Loading and Code Splitting Beispiel</h1>
     <div id="app"></div>
     <script src="bundle.js"></script>
     <link rel="stylesheet" href="main.css">
   </body>
   </html>
   ```

6. **Erstellen eines einfachen Eingangsblatts:**

   Erstelle eine `src/index.js`-Datei:

   ```javascript
   import './styles/main.css';
   import App from './App';

   const appContainer = document.getElementById('app');
   const app = new App();
   appContainer.appendChild(app.el);
   ```

7. **Entwicklungsserver starten:**

   ```bash
   npx webpack serve --config webpack.config.js
   ```

### HTTP-Caching einrichten

Um HTTP-Caching zu aktivieren, kannst du einen Middleware wie `express-cache` für Node.js-Anwendungen nutzen.

1. **`express-cache` installieren:**

   ```bash
   npm install express-cache
   ```

2. **`express-cache` konfigurieren:**

   Erstelle eine `cache.js`-Datei:

   ```javascript
   const express = require('express');
   const cache = require('express-cache');

   const app = express();

   app.use(cache({
     maxAge: 3600, // Cache for 1 hour
     cacheControl: true,
     cacheRefresh: true,
   }));

   app.get('/api/data', (req, res) => {
     res.send('Cached Data');
   });

   app.listen(3000, () => {
     console.log('Server is running on port 3000');
   });
   ```

## Verwendung

### Lazes Laden mit Webpack

Das Lazes Laden erreicht sich durch das Aufteilen des Codes in kleinere Teile mit Webpack. Dies wird erreicht, indem bestimmte Module als lazes geladen werden, wodurch die `React.lazy`-Funktion und der `React.Suspense`-Component genutzt werden.

1. **Lazes geladenes Komponenten erstellen:**

   ```javascript
   const MyLazyComponent = React.lazy(() => import('./MyComponent'));
   ```

2. **Lazes geladenes Komponenten mit `React.Suspense` verpacken:**

   ```javascript
   <React.Suspense fallback={<div>Lade...</div>}>
     <MyLazyComponent />
   </React.Suspense>
   ```

### HTTP-Caching

Um HTTP-Caching zu aktivieren, setze die `Cache-Control`-Header in deinen API-Antworten.

1. **`Cache-Control`-Header in Express festlegen:**

   ```javascript
   app.get('/api/data', (req, res) => {
     res.setHeader('Cache-Control', 'public, max-age=3600');
     res.send('Cached Data');
   });
   ```

## Schlüssel-Funktionen

### Webpack

- **Code-Splitting:** Automatisch teilt den Code in kleinere Teile auf.
- **Tree Shaking:** Entfernt nicht benutzten Code aus dem Endpaket.
- **SplitChunks:** Optimiert die Größe und Anzahl der Teile.

### Express Cache

- **Max Age:** Steuert die Cacheadungsdauer.
- **Cache Control:** Steuert das Cachingverhalten.
- **Cache Refresh:** Sorgt dafür, dass gespeicherte Daten nach einer bestimmten Zeitspanne erneuert werden.

### Befehle

#### Webpack Serve Befehl

```bash
npx webpack serve --config webpack.config.js
```

#### Express Cache Befehl

```javascript
node cache.js
```

## Schlussfolgerung

Die Implementierung von Cachingstrategien, lazes Laden und Code-Splitting kann die Leistung von Webanwendungen erheblich verbessern. Folge den Schritten in diesem Leitfaden, um die Benutzererfahrung zu verbessern und die Leistung deiner Anwendung zu optimieren.