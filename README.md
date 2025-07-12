# Task Management System (TMS)


**Task Management System (TMS)** is an issue tracker built to practice Clean Architecture and Domain-Driven Design (DDD).
<br>
It implements domain modeling with support for task creation, commenting and file attachments — all encapsulated in a clean, testable backend structure.  
The system includes layered tests: unit (domain), integration (views), and API-level.


<br>

## Architecture

- Clean Architecture
- Domain-Driven Design (DDD)
- File uploads to S3 are streamed to avoid memory overhead


<br>

## Project Structure

```text
app/tasks/
├── domain/         # Entities, ValueObjects, Aggregates, repositories
├── use_cases/      # Application logic
├── views/          # Controllers
├── ...
└── api_tests/      
```

<br>

## Test Coverage

- **~97% overall coverage**
- Unit tests for domain logic (app/tasks/domain)
- Integration tests for Django views (app/tasks/views/views_tests.py)
- API-level tests (app/tasks/api_tests/)

<br>

## Tech Stack

- Python 3.13
- Django + Django REST Framework
- SQLite (for simplicity)
- AWS S3-compatible storage
- Pytest
- Docker + Docker Compose
- Bash (startup script for migrations and dev server)

<br>
 

## CI/CD

- CI: tests are automatically run on every push via GitHub Actions
- CD: successful builds are deployed to a personal server via SSH


 <br>

## Features

- Create tasks
- Comment on tasks
- Attach files to tasks


 <br>

## Telegram Bot

A Telegram bot is used as a basic chat-based interface to demonstrate core functionality.
<br>
**Bot chat:** https://t.me/tms_proj_bot
<br>
**Bot source code:** https://github.com/Dobrobrav/tms_bot
<br>
<br>
**Note:** due to Telegram Bot API limitations, file uploads are currently restricted to small files (up to ~20 MB).  
Support for large file uploads (e.g. via external links) is planned.
