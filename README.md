# Task Manager API

A high-performance, asynchronous RESTful API built with **FastAPI**, **SQLAlchemy ORM**, and **Pydantic** for managing tasks and user workflows. This project features database migrations managed via **Alembic** and an automated testing setup using **Pytest**.

## Features

* **RESTful Endpoints**: Full CRUD functionality for task creation, retrieval, updates, and deletion.
* **Data Validation**: Request/response payload validation using Pydantic schemas.
* **Database & ORM**: Database interactions powered by SQLAlchemy.
* **Migrations**: Database schema version control using Alembic.
* **Automated Testing**: Test suite implemented with Pytest using isolated test database execution.

## Tech Stack

* **Framework**: FastAPI
* **ORM**: SQLAlchemy
* **Database**: SQLite (Development)
* **Migrations**: Alembic
* **Testing**: Pytest
* **Language**: Python 3.x

## Project Structure

```text
task-manager-api/
├── migrations/          # Alembic database migration scripts
├── tests/               # Pytest suite
├── alembic.ini          # Alembic configuration
├── database.py         # Database engine and session setup
├── main.py             # FastAPI application entry point & routes
├── models.py           # SQLAlchemy database models
└── schemas.py          # Pydantic validation schemas
