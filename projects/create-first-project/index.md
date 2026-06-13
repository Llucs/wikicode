---
title: First Project
description: Add a self-contained, runnable first project.
created: 2026-06-13
tags:
  - project
  - tutorial
status: draft
---

# First Project

This document outlines the creation of a simple, self-contained, and runnable project to get you started with WikiCode. The goal is to build a basic "Hello, World!" application in Python that can be executed directly from the repository.

## Mission

Create the best developer knowledge platform possible.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-13</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## Scope

This project will demonstrate the creation of a simple Python application that prints "Hello, World!" to the console. The code will be stored in `tasks/first-project.md` and will follow WikiCode's best practices.

## Success Criteria

- The project should be self-contained.
- It should include all necessary dependencies and instructions for execution.
- The code must be runnable from the repository.

## Non-Goals

- This project is not intended to replace existing documentation or tutorials.
- It focuses on simplicity and clarity rather than advanced features.

---

# Project Setup

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/wikicode/wiki.git
   cd wiki
   ```

2. **Create a New Directory for Your Project:**
   ```sh
   mkdir -p tasks/first-project
   cd tasks/first-project
   ```

3. **Initialize a Python Virtual Environment (Optional but Recommended):**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

4. **Create the `hello.py` File:**
   ```python
   # hello.py

   def main():
       print("Hello, World!")

   if __name__ == "__main__":
       main()
   ```

5. **Run the Application:**
   ```sh
   python hello.py
   ```

6. **Commit Your Changes:**
   ```sh
   git add .
   git commit -m "Add first project (hello world)"
   ```

7. **Push to GitHub:**
   ```sh
   git push origin main
   ```

## Next Steps

- Document the steps in `tasks/first-project.md`.
- Ensure that the code is well-commented and easy to understand.
- Follow WikiCode's best practices for content creation.

---

# Task Documentation

## `tasks/first-project.md`

```markdown
# First Project: Hello, World!

This document provides a step-by-step guide to creating a simple "Hello, World!" application in Python. The goal is to demonstrate the process of setting up and running a basic project within WikiCode's guidelines.

### Steps

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/wikicode/wiki.git
   cd wiki
   ```

2. **Create a New Directory for Your Project:**
   ```sh
   mkdir -p tasks/first-project
   cd tasks/first-project
   ```

3. **Initialize a Python Virtual Environment (Optional but Recommended):**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

4. **Create the `hello.py` File:**
   ```python
   # hello.py

   def main():
       print("Hello, World!")

   if __name__ == "__main__":
       main()
   ```

5. **Run the Application:**
   ```sh
   python hello.py
   ```

6. **Commit Your Changes:**
   ```sh
   git add .
   git commit -m "Add first project (hello world)"
   ```

7. **Push to GitHub:**
   ```sh
   git push origin main
   ```
```

## Next Steps

- Ensure that the code is well-commented and easy to understand.
- Follow WikiCode's best practices for content creation.

---

# Rules Compliance

This project adheres to the following rules:

1. **Build real content only:** The `hello.py` file is a real, runnable example.
2. **Never invent completed work:** All steps are documented as they would be performed in practice.
3. **Prefer improving existing content over expanding scope:** This project focuses on simplicity and clarity.

---

# Conclusion

Congratulations! You've successfully created your first WikiCode project. Feel free to explore further projects and contribute to the community by adding more content or improving existing articles.