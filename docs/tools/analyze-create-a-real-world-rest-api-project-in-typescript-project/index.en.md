---
title: Create a Real-World REST API Project in TypeScript
description: A comprehensive guide to building a robust REST API using TypeScript, Express.js, and MongoDB.
created: 2026-07-19
tags:
  - TypeScript
  - Express.js
  - MongoDB
  - REST API
  - Authentication
  - Docker
status: draft
---

# Create a Real-World REST API Project in TypeScript

This guide walks you through the process of building a robust REST API using TypeScript, Express.js, and MongoDB. It includes detailed documentation, best practices, and real-world examples to help you understand and implement a production-ready API solution.

## Key Features

1. **TypeScript**: Static typing for better error detection and code quality.
2. **Express.js**: A popular Node.js web application framework.
3. **MongoDB**: A NoSQL document database for data storage.
4. **JWT Authentication**: Secure routes using JSON Web Tokens (JWT).
5. **Mongoose**: An Object Data Modeling (ODM) library for MongoDB.
6. **Testing**: Unit and integration tests with Jest and Supertest.
7. **Swagger Documentation**: Auto-generated API documentation for easy reference.

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/username/repo.git
   cd repo
   ```

2. **Install Dependencies**:
   ```sh
   npm install
   ```

3. **Set Up MongoDB**:
   - Install MongoDB if not already installed.
   - Start the MongoDB server.
   - Configure the connection string in the `.env` file.

4. **Configure Environment Variables**:
   - Update the `.env` file with necessary environment variables, such as database connection string, JWT secret, etc.

5. **Run the Server**:
   ```sh
   npm start
   ```

## Basic Usage

### API Endpoints

1. **User Management**:
   - **Create User**: POST `/api/users`
   - **Get User**: GET `/api/users/:id`
   - **Update User**: PATCH `/api/users/:id`
   - **Delete User**: DELETE `/api/users/:id`

2. **Product Management**:
   - **Create Product**: POST `/api/products`
   - **Get Product**: GET `/api/products/:id`
   - **Update Product**: PATCH `/api/products/:id`
   - **Delete Product**: DELETE `/api/products/:id`

3. **Order Management**:
   - **Create Order**: POST `/api/orders`
   - **Get Order**: GET `/api/orders/:id`
   - **Update Order**: PATCH `/api/orders/:id`
   - **Delete Order**: DELETE `/api/orders/:id`

4. **Authentication**:
   - **Generate JWT Token**: POST `/api/auth/login`
   - **Protect Routes**: Use JWT token in the `Authorization` header

### Testing

1. **Unit Testing**:
   - Use Jest for unit testing.
   - Run tests with:
     ```sh
     npm test
     ```

2. **Integration Testing**:
   - Use Supertest for integration testing.
   - Run tests with:
     ```sh
     npm test
     ```

### Swagger Documentation

1. **Access Swagger UI**:
   - Navigate to `http://localhost:3000/docs` in your browser.
   - Use the generated documentation to understand and interact with the API.

### Authentication

1. **Generate JWT Token**:
   - Make a POST request to `/api/auth/login` with user credentials.
   - Example using `curl`:
     ```sh
     curl -X POST http://localhost:3000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password"}'
     ```

2. **Include JWT in Requests**:
   - Use the JWT token in the `Authorization` header for protected routes.
   - Example using `curl`:
     ```sh
     curl -X GET http://localhost:3000/api/users/1 \
     -H "Authorization: Bearer <JWT_TOKEN>"
     ```

### Data Management

1. **Define Mongoose Schemas**:
   - Use Mongoose to define schemas for models.
   - Example schema for a User:
     ```typescript
     import { Schema, model } from 'mongoose';

     const UserSchema = new Schema({
       name: String,
       email: { type: String, unique: true },
       password: String
     });

     export const User = model('User', UserSchema);
     ```

2. **Perform CRUD Operations**:
   - Use Mongoose methods to perform CRUD operations.
   - Example to create a user:
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

## Conclusion

By following the detailed guide and using the provided codebase as a starting point, you can extend and customize the API to meet specific project requirements. This comprehensive project not only provides a practical example but also serves as an excellent learning tool for understanding modern web development practices with TypeScript, Express.js, and MongoDB.

Happy coding!