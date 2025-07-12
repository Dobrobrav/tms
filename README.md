# Task Management System

______

## Overview

**Task Management System (TMS)** is an issue tracker built to practice Clean Architecture, Domain-Driven Design (DDD),
and separation of concerns.  
It implements realistic domain modeling with support for task creation, commenting, file attachments, and assignee
assignment — all encapsulated in a clean, testable backend structure.  
The system includes layered tests: unit (domain), integration (views), and API-level.


---

## Architecture

- Clean Architecture
- Domain-Driven Design (DDD)
- Modular separation: `domain`, `usecases`, `infrastructure`, `interfaces`

___

## Project Structure

```text
app/tasks/
├── domain/         # Entities, ValueObjects, Aggregates, repositories
├── use_cases/      # Application logic
├── views/          # Controllers
├── ...
└── api_tests/      
```

___

## Test Coverage

- **~97% overall coverage**
- Unit tests for domain logic (app/tasks/domain)
- Integration tests for Django views (app/tasks/views/views_tests.py)
- API-level tests (app/tasks/api_tests/)

___

## Tech Stack

- Python 3.13
- Django + Django REST Framework
- SQLite (for simplicity)
- AWS S3-compatible storage
- Pytest
- Docker + Docker Compose
- Bash (startup script for migrations and dev server)

___

## Features

- Create tasks
- Comment on tasks
- Attach files to tasks

___

## Telegram Bot

A basic Telegram bot is used as a basic chat-based interface to demonstrate core functionality.
https://t.me/tms_proj_bot