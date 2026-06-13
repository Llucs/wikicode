---
title: Mission
description: WikiCode mission statement.
created: 2026-06-03
tags:
  - wiki-code
status: draft
---

# Mission

Create the best developer knowledge platform possible.

## Scope

WikiCode is a long-lived, documentation-first repository that combines:

- technical articles,
- real, runnable projects,
- focused code snippets,
- and an operational memory for the agents that maintain it.

## Success criteria

- Every published page is real, accurate and useful.
- The site is easy to navigate and search.
- Autonomous agents can evolve the wiki safely, without losing context.
- New contributors — human or AI — can onboard in minutes.

## Non-goals

- Mirroring third-party tutorials.
- Hosting interactive services or APIs.
- Acting as a personal blog or marketing site.
- Collecting user data.

---

# Rules

Permanent operational rules. These are normative and override any ad-hoc instructions that conflict with them.

## Content

1. Build real content only. No placeholders, no fake integrations, no simulated data, no demo-only branches.
2. Never invent completed work. If something is not done, it is not in `tasks/completed.md`.
3. Never fabricate results. No fake benchmarks, screenshots or metrics.
4. Prefer improving existing content over expanding scope.

## Safety

5. Never expose secrets, tokens, keys or personal data.
6. Use GitHub Secrets for credentials. Never commit `.env` files.
7. Never delete content. Archive it first (move to an `archive/` folder inside the relevant section) and reference the move in a report.

## Process

8. One meaningful task per execution. Do not bundle unrelated changes.
9. Generate a report in `reports/` after every execution, even if the task was small.
10. Keep documentation synchronized with the code or content it describes.
11. Preserve structure consistency. New sections follow the same layout as existing ones.
12. Record architectural decisions in `memory/decisions.md`.

## Quality

13. Code snippets must be runnable or at least syntactically valid.
14. Projects must include a `README.md` and an `index.md` for the site.
15. Markdown must render cleanly. The CI runs `mkdocs build --clean` on every push; a broken build blocks deployment.

---

# WikiCode Project

## Overview

This project is a complete REST API service written in Go, serving as a real-world example of how to build and maintain such an application using the best practices outlined in our rules. The goal is to demonstrate the creation of a robust, secure, and functional API that can be integrated into various applications.

### Technology Stack

- **Programming Language:** Go
- **Web Framework:** Gin (for simplicity and performance)
- **Database:** SQLite for development, PostgreSQL for production
- **Authentication:** JWT (JSON Web Tokens) for user authentication
- **API Endpoints:** RESTful endpoints using HTTP methods like GET, POST, PUT, DELETE

### Architecture

The project will be organized into the following directories:

- `api`: Contains all API-related files.
- `models`: Models and data structures used by the API.
- `services`: Business logic for handling requests and responses.
- `utils`: Utility functions that can be reused across different parts of the application.

### Features

1. **User Authentication**: Users can register, log in, and logout securely using JWT tokens.
2. **Resource Management**: CRUD (Create, Read, Update, Delete) operations on user profiles.
3. **Error Handling**: Proper error handling to ensure robustness and user-friendly responses.
4. **Security Measures**: Implementing best practices for security such as input validation, rate limiting, and secure session management.

### Project Structure

```plaintext
api/
├── auth/           # Authentication logic
│   └── handlers.go  # JWT token handling
│   └── middleware.go # Middleware to handle authentication
└── controllers/     # Controller files for API endpoints
    ├── user.go       # User controller
    └── index.go      # Index file for all API endpoints
├── models/          # Models and data structures
│   └── user_model.go # User model definition
└── services/        # Business logic for handling requests and responses
    └── auth_service.go  # Authentication service implementation
    └── user_service.go  # User service implementation
├── utils/           # Utility functions
│   ├── jwt_utils.go  # JWT utility functions
│   └── error_handler.go # Error handling utilities
└── README.md        # Project documentation and setup instructions
```

### API Endpoints

Here are the initial RESTful endpoints for user management:

- **POST /api/v1/auth/register**: Register a new user.
- **POST /api/v1/auth/login**: Log in an existing user with credentials.
- **GET /api/v1/user/profile**: Retrieve user profile information.

### Setup Instructions

To set up and run this project locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/wikicode.git
   cd wikicode/api
   ```

2. Install required dependencies:
   ```sh
   go get -u github.com/gin-gonic/gin
   go get -u golang.org/x/crypto/ssh
   go get -u github.com/dgrijalva/jwt-go
   ```

3. Create a `.env` file with your database credentials and API keys:
   ```plaintext
   DB_USER=your_db_user
   DB_PASS=your_db_pass
   JWT_SECRET=my_jwt_secret_key
   ```

4. Run the development server:
   ```sh
   go run main.go
   ```

5. Test the endpoints using a tool like `curl` or Postman.

### Running Tests

To ensure your application is working as expected, you can run tests:

1. Install Go modules if not already installed:
   ```sh
   go mod tidy
   ```

2. Run unit tests:
   ```sh
   go test ./...
   ```

This project serves as a foundation for building more complex APIs and showcases the importance of following best practices in software development, particularly when it comes to security and maintainability.