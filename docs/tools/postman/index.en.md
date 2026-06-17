---
title: Postman - API Development and Testing Platform
description: A comprehensive guide to Postman, the industry-standard API platform for designing, building, testing, and documenting APIs.
created: 2026-06-15
tags:
  - postman
  - api-testing
  - api-development
  - collaboration
  - newman
status: draft
ecosystem: api
---

# Postman - API Development and Testing Platform

## What is Postman?

Postman is a complete API platform that simplifies each step of the API lifecycle – from design and development to testing, documentation, and monitoring. Originally started as a simple HTTP client, it has evolved into a collaborative environment used by millions of developers and QA engineers worldwide. Postman supports REST, GraphQL, and SOAP protocols, and provides a rich set of tools for building and working with APIs efficiently.

## Why use Postman?

- **Comprehensive HTTP Client:** Easily send requests of any method, customize headers, authentication, and body content.
- **Organisational Tooling:** Group requests into Collections, manage variables with Environments, and reuse data across an entire workspace.
- **Scripting & Testing:** Write JavaScript test scripts to automate assertions, extract data between requests, and handle dynamic workflows.
- **Automation Ready:** Use the Collection Runner for manual runs or Newman for headless execution (CI/CD, pipelines).
- **Collaboration:** Share collections and environments via cloud workspaces with version control and commenting.
- **Documentation & Mocking:** Auto-generate API documentation and mock servers to simulate API responses before the backend is ready.
- **Monitoring:** Set up monitors to schedule collection runs and verify API health.

## Installation

### Desktop App (Recommended)

Postman provides native desktop apps for Windows, macOS, and Linux.

- Download the appropriate installer from [getpostman.com](https://getpostman.com)
- Alternatively, use the **web version** at [go.postman.co](https://go.postman.co) with the Desktop Agent to handle API calls.

### Newman (CLI for CI/CD)

Newman is the command-line collection runner for Postman. It enables you to run and test a Postman collection directly from the command line, making it ideal for integrating API tests into your development pipeline.

Install via npm:

```bash
npm install -g newman
```

Or with Yarn:

```bash
yarn global add newman
```

## Basic Usage

1. **Create a request**  
   Click the **New** button and choose **HTTP Request** (or use `Ctrl+N`).

2. **Specify the request**  
   - Enter the URL (e.g., `https://jsonplaceholder.typicode.com/posts`)  
   - Select the HTTP method (`GET`, `POST`, `PUT`, etc.)  
   - Add any required headers, query parameters, or request body.

3. **Send and inspect**  
   Click **Send**. The response pane shows the status code, response time, headers, and body.

4. **Save to a collection**  
   Click **Save** and either create a new collection or add to an existing one.

5. **Add a test**  
   Under the **Tests** tab, write a JavaScript script to validate the response. Example:

   ```javascript
   pm.test("Response status code is 200", function () {
       pm.response.to.have.status(200);
   });
   ```

   Rerun the request – the test result appears in the **Test Results** tab.

## Key Features with Examples

### 1. Collections

Collections help you group related requests and share them with your team. A collection can also include folders and metadata.

```javascript
// Example of using collection variables in a pre-request script
pm.collectionVariables.set("baseUrl", "https://api.example.com");
```

Run an entire collection using Newman:

```bash
newman run MyCollection.json
```

### 2. Environments

Environments contain key-value pairs for variables that change between setups (development, staging, production).

```json
{
  "base_url": "https://dev-api.example.com",
  "api_key": "abc123"
}
```

Use `{{base_url}}` in your request URLs. Switch between environments to change contexts instantly.

### 3. Pre-request and Test Scripts

Postman scripts are written in JavaScript and run in a sandbox with access to Postman provided objects like `pm`.

**Pre-request script** (executed before the request is sent):

```javascript
// Dynamically set a timestamp parameter
pm.variables.set("timestamp", Date.now());
```

**Test script** (executed after the response is received):

```javascript
pm.test("Response time is less than 2000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("Body contains expected user", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData[0].name).to.eql("Leanne Graham");
});
```

### 4. Collection Runner

Run an entire collection or a folder multiple times with data files.

- Open **Runner** from the top left of Postman.
- Select a collection, choose an environment, set iterations.
- You can provide a CSV or JSON data file to inject data into each iteration.

### 5. Newman – Command Line Integration

Newman enables you to integrate your Postman tests into CI/CD pipelines (Jenkins, GitLab CI, GitHub Actions, etc.).

**Run a collection with an environment and a data file:**

```bash
newman run MyCollection.json \
  --environment staging.json \
  --iteration-data test-data.csv \
  --reporters cli,htmlextra
```

The `htmlextra` reporter generates an interactive HTML report of the test run.

**Use in a Node.js script:**

```javascript
const newman = require('newman');

newman.run({
    collection: require('./MyCollection.json'),
    environment: require('./staging.json'),
    reporters: 'cli'
}, function (err, summary) {
    if (err) { throw err; }
    console.log('Collection run completed!');
    console.log(summary.run.stats);
});
```

### 6. Documentation Generation

Postman can automatically generate documentation for any collection. Simply open a collection, click the **...** menu, and choose **View documentation**. The documentation includes example requests, request/response schemas, and code snippets in various languages.

Publish the documentation to the web via the **Publish Docs** button, or export it as HTML.

### 7. Mock Servers

Mimic an API by creating a mock server from your collection. This is extremely useful for frontend development when the backend is not yet ready.

- Select a collection, click **Mock Servers**.
- Postman creates a mock server URL that returns the saved example responses.

### 8. Monitors

Monitors allow you to schedule periodic runs of a collection on Postman’s cloud infrastructure. You receive alerts if any tests fail.

- Go to **Monitors** → **Create a monitor**.
- Select a collection, set a frequency (e.g., every hour), and optionally define alerts (email, Slack, etc.).

## Summary

Postman is much more than an API client – it’s a full‑fledged platform that supports the entire API lifecycle. From initial mocking and collaborative design to automated testing via Newman and production monitoring, Postman equips teams with a single source of truth for their APIs. Its ease of use, combined with powerful scripting and CI/CD integration, makes it an indispensable tool for modern development workflows.