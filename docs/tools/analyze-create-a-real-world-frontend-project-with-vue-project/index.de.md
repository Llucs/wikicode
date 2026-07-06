---
title: Erstellen eines realen Frontend-Projekts mit Vue
description: Ein Leitfaden zur Erstellung einer praktischen frontend-basierten Webanwendung mit Vue.js, der grundlegende Funktionen und die besten Praktiken abdeckt.
created: 2026-07-06
tags:
  - Vue.js
  - frontend-Entwicklung
  - Webanwendung
status: Entwurf
---

# Erstellen eines realen Frontend-Projekts mit Vue

## Übersicht

Dieses Projekt führt Lernende Schritt für Schritt bei der Erstellung einer vollständigen frontend-basierten Webanwendung mit Vue.js. Das Ziel ist es, eine dynamische und interaktive Benutzeroberfläche mit Vue zu erstellen, während grundlegende Konzepte und die besten Praktiken der Webentwicklung abgedeckt werden.

## Hauptfunktionen

1. **Vue.js-Framework:** Das Projekt konzentriert sich hauptsächlich auf Vue.js, ein leichtgewichtiges und flexibles Framework.
2. **Real-World-Anwendung:** Das Projekt umfasst die Erstellung einer praktischen Anwendung, wie z.B. eine Todo-Liste, ein E-Commerce-Plattform oder ein soziales Medien-Feed.
3. **Vue CLI:** Die Nutzung von Vue CLI zur Initialisierung und Strukturierung des Projekts.
4. **Vue Router:** Die Implementierung von Routing, um verschiedene Ansichten und Seiten zu verwalten.
5. **Vuex:** Die Verwendung von Vuex für die Zustandsverwaltung.
6. **VueXy (optional):** Die Optionale Integration für reaktive Formulare.
7. **Axios:** Die Nutzung von Axios für HTTP-Anfragen.
8. **CSS-Framework:** Die Integration eines CSS-Frameworks, wie z.B. Bootstrap oder Tailwind CSS.
9. **Tests:** Die Einführung von Einheits- und Integrations-Tests.
10. **Bereitstellung:** Anleitungen zur Bereitstellung der Anwendung auf ein Hostingdienst.

## Voraussetzungen

- Node.js und npm (Node Package Manager)
- Ein Texteditor oder IDE (z.B. VS Code, WebStorm)

## Installation

1. **Vue CLI global aufsetzen:**
   ```bash
   npm install -g @vue/cli
   ```

2. **Ein neues Vue-Projekt erstellen:**
   ```bash
   vue create my-app
   ```

3. **In das Projektverzeichnis wechseln:**
   ```bash
   cd my-app
   ```

4. **Den Entwicklungsserver starten:**
   ```bash
   npm run serve
   ```

## Grundlegende Verwendung

### Komponenten-Erstellung

1. **Eine neue Komponenten-Datei erstellen (z.B. `TodoItem.vue`):**
   ```javascript
   <template>
     <div>
       <p>{{ item.text }}</p>
     </div>
   </template>
   <script>
   export default {
     props: ['item'],
   }
   </script>
   ```

2. **Die Komponente im Elternkomponenten verwenden:**
   ```javascript
   <template>
     <div>
       <TodoItem v-for="item in todoList" :item="item" />
     </div>
   </template>
   <script>
   import TodoItem from './components/TodoItem.vue';
   export default {
     components: { TodoItem },
     data() {
       return {
         todoList: [
           { text: 'Vue lernen', isComplete: false },
           { text: 'ein Projekt bauen', isComplete: true },
         ],
       }
     }
   }
   </script>
   ```

### Routing

1. **Vue Router installieren:**
   ```bash
   npm install vue-router
   ```

2. **Routes in `router/index.js` konfigurieren:**
   ```javascript
   import Vue from 'vue';
   import Router from 'vue-router';
   import Home from './views/Home.vue';
   import About from './views/About.vue';

   Vue.use(Router);

   export default new Router({
     routes: [
       { path: '/', component: Home },
       { path: '/about', component: About },
     ]
   });
   ```

3. **Die Routes im Hauptapp verwenden:**
   ```javascript
   <template>
     <div>
       <router-view></router-view>
     </div>
   </template>
   ```

### Vuex

1. **Vuex installieren:**
   ```bash
   npm install vuex
   ```

2. **Vuex-Store in `store/index.js` initialisieren:**
   ```javascript
   import Vue from 'vue';
   import Vuex from 'vuex';

   Vue.use(Vuex);

   export default new Vuex.Store({
     state: {
       count: 0,
     },
     mutations: {
       increment(state) {
         state.count++;
       },
     },
     actions: {
       increment({ commit }) {
         commit('increment');
       },
     },
     getters: {
       count: state => state.count,
     },
   });
   ```

3. **Die Store in einer Komponente verwenden:**
   ```javascript
   <template>
     <div>{{ count }}</div>
     <button @click="increment">Zähler erhöhen</button>
   </template>
   <script>
   import { mapState, mapActions } from 'vuex';

   export default {
     computed: {
       ...mapState(['count']),
     },
     methods: {
       ...mapActions(['increment']),
     }
   }
   </script>
   ```

### Tests

1. **Jest und Vue Test Utils installieren:**
   ```bash
   npm install --save-dev jest @vue/test-utils
   ```

2. **Eine Test für eine Komponente schreiben:**
   ```javascript
   import { shallowMount } from '@vue/test-utils';
   import TodoItem from '@/components/TodoItem.vue';

   describe('TodoItem.vue', () => {
     it('zeigt den Todo-Text an', () => {
       const wrapper = shallowMount(TodoItem, {
         propsData: {
           item: { text: 'Test Todo' },
         },
       });
       expect(wrapper.text()).toContain('Test Todo');
     });
   });
   ```

### Bereitstellung

1. **Das Projekt erstellen:**
   ```bash
   npm run build
   ```

2. **Die erstellten Dateien bereitstellen:**
   - Für Netlify:
     ```bash
     netlify deploy --dir=dist --prod
     ```

## Zusammenfassung

Das "Erstellen eines realen Frontend-Projekts mit Vue" ist ein umfassender Leitfaden, der Lernende bei der Erstellung praktischer Anwendungen mit Vue.js unterstützt. Indem grundlegende Funktionen und die besten Praktiken abgedeckt werden, ermöglicht das Projekt den Entwicklern, robuste und pflegeleichte Webanwendungen zu erstellen.