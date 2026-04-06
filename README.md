# Finance Dashboard System - Finance Data Processing and Access Control Backend

A role-based financial records management system built with **FastAPI**, **SQLAlchemy**, and **MySQL**. Designed as a backend-only REST API with JWT authentication, tiered access control, and dashboard analytics endpoints.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Server](#running-the-server)
- [API Reference](#api-reference)
- [Role-Based Access Control](#role-based-access-control)
- [Assumptions Made](#assumptions-made)
- [Tradeoffs Considered](#tradeoffs-considered)

---

## Project Overview

This API serves as the backend for a finance dashboard used internally by organizations. It supports three user roles with different levels of access:

| Role | Capabilities |
|------|-------------|
| Viewer | Read-only access to financial records |
| Analyst | Read + create + update financial records |
| Admin | Full access including user management and deletions |

Core features: JWT authentication, financial records CRUD, dashboard summary/analytics endpoints, and role-based route protection via FastAPI dependency injection.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| ORM | SQLAlchemy (sync) |
| Database | MySQL |
| DB Driver | PyMySQL |
| Validation | Pydantic v2 |
| Authentication | python-jose (JWT), passlib (bcrypt) |
| Config | python-dotenv |
| Server | Uvicorn |

---

## Project Structure

```
finance-dashboard/
├── app/
│   ├── models/
│   │   ├── role.py          # Role table (Viewer, Analyst, Admin)
│   │   ├── user.py          # User table with FK to Role
│   │   └── finance.py       # FinancialRecord table
│   ├── schemas/
│   │   ├── user.py          # Pydantic schemas for user I/O
│   │   └── finance.py       # Pydantic schemas for finance I/O
│   ├── routers/
│   │   ├── auth.py          # /login endpoint
│   │   ├── users.py         # User management (Admin only)
│   │   └── finance.py       # Financial record CRUD
│   ├── core/
│   │   ├── config.py        # Settings class (reads .env)
│   │   ├── database.py      # SQLAlchemy engine + SessionLocal
│   │   └── security.py      # JWT creation, bcrypt hashing
│   ├── dependencies.py      # get_db(), get_current_user(), role guards
│   └── main.py              # App entry point, router registration
├── .env                     # Local environment variables (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- MySQL 8.0+ running locally
- `pip` and `venv`

### 1. Clone the repository

```bash
git clone https://github.com/your-username/finance-dashboard.git
cd finance-dashboard
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt`:
```
fastapi
uvicorn
sqlalchemy
pymysql
pydantic[email]
python-dotenv
passlib[bcrypt]
python-jose[cryptography]
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=finance_db
DB_USER=root
DB_PASSWORD=your_mysql_password

SECRET_KEY=your_super_secret_jwt_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Never commit `.env` to version control — it is listed in `.gitignore`. The `config.py` Settings class reads all values via `os.getenv()` and exposes them as typed attributes consumed by `database.py` and `security.py`.

---

## Database Setup

### 1. Create the database in MySQL

```sql
CREATE DATABASE finance_db;
```

### 2. Seed roles (required before creating any users)

Roles are not auto-seeded on startup. Run this once manually:

```sql
USE finance_db;
INSERT INTO roles (name) VALUES ('Viewer'), ('Analyst'), ('Admin');
```

### 3. Tables are created automatically

On first run, `Base.metadata.create_all(bind=engine)` in `main.py` creates all tables defined in the models. No migration tool is used (see Tradeoffs).

---

## Running the Server

```bash
uvicorn app.main:app --reload
```

- API base URL: `http://127.0.0.1:8000`
- Swagger UI (interactive docs): `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## API Reference

### Authentication

#### `POST /auth/login`
Authenticate a user and receive a JWT access token.

Request body:
```json
{
  "email": "john@example.com",
  "password": "secret123"
}
```

Response:
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

All subsequent requests must include:
```
Authorization: Bearer <access_token>
```

---

### Users *(Admin only)*

#### `GET /users/`
Returns a list of all registered users.

#### `POST /users/`
Create a new user and assign a role.

Request body:
```json
{
  "email": "jane@example.com",
  "password": "securepass",
  "role_id": 2
}
```

#### `DELETE /users/{user_id}`
Permanently delete a user by ID.

---

### Financial Records

#### `GET /finance/`
Returns all financial records. Accessible by all roles.

#### `GET /finance/{record_id}`
Returns a single record by ID. Accessible by all roles.

#### `POST /finance/`
Create a new financial record. **Analyst and Admin only.**

Request body:
```json
{
  "title": "Server hosting fee",
  "amount": 4999.00,
  "type": "expense",
  "category": "Infrastructure",
  "date": "2025-04-01"
}
```

#### `PUT /finance/{record_id}`
Update an existing record. **Analyst and Admin only.**

#### `DELETE /finance/{record_id}`
Delete a record. **Admin only.**

---

### Dashboard Analytics

#### `GET /dashboard/summary`
Aggregate totals for the current month.

Response:
```json
{
  "total_income": 150000.00,
  "total_expenses": 87500.00,
  "net": 62500.00
}
```

#### `GET /dashboard/by-category`
Expense totals grouped by category.

Response:
```json
[
  { "category": "Infrastructure", "total": 12000.00 },
  { "category": "Salaries", "total": 75000.00 }
]
```

#### `GET /dashboard/trends`
Monthly income vs. expense totals over the past 6 months, suitable for charting.

---

## Role-Based Access Control

Access control is enforced at the dependency layer using FastAPI's `Depends()` system. Each protected route declares a role guard:

```python
@router.delete("/{record_id}", dependencies=[Depends(require_role("Admin"))])
```

`require_role()` is a factory function in `dependencies.py` that decodes the JWT via `get_current_user()`, checks the user's role, and raises `HTTP 403 Forbidden` if it doesn't match. Authorization logic is kept entirely out of route handlers.

---

## Assumptions Made

**1. Single organization, flat user model.** All users share the same record pool. Multi-tenancy (org-scoped data) was out of scope.

**2. Email is the username.** Users authenticate with their email rather than a separate username field — realistic for internal tools and simpler to model.

**3. Roles are fixed and seeded manually.** The three roles are fixed by design. There is no API to create custom roles, since dynamic roles would require a full permission matrix.

**4. Hard deletes only.** Records are permanently deleted. A production system would use `is_deleted` or `deleted_at` to preserve audit history, but that added complexity without serving the learning goal.

**5. No pagination.** `GET /finance/` returns the full record set. Fine for a portfolio project; a real system would add `limit`/`offset` or cursor-based pagination.

**6. Stateless JWT — no token revocation.** A logged-out token stays valid until expiry. Revocation would require a server-side blocklist (e.g., Redis), which is a production concern beyond this scope.

**7. Passwords hashed with bcrypt.** Plain-text passwords are never stored. `passlib` handles hashing and verification.

**8. Dates stored as `DATE`, not `DATETIME`.** Financial records represent calendar-day entries, not precise timestamps.

---

## Tradeoffs Considered

**`create_all` vs. Alembic migrations**
`Base.metadata.create_all()` creates tables on startup with zero configuration, which is perfect for a learning project. The tradeoff is it cannot handle schema *changes* (e.g., adding a column) without dropping tables. Alembic solves this with versioned migration files but adds meaningful setup overhead. For production, Alembic is the right choice.

**Synchronous SQLAlchemy vs. async**
The synchronous ORM is easier to reason about and debug. Async SQLAlchemy with `aiomysql` would allow non-blocking DB calls in FastAPI's event loop, which matters at high concurrency. For this project, the bottleneck is not I/O volume, so sync is the pragmatic call.

**JWT in Authorization header vs. HttpOnly cookies**
Bearer tokens are the REST API standard and work cleanly with Swagger UI and non-browser clients. HttpOnly cookies are more XSS-resistant but require CSRF protection and are browser-coupled. Since this project has no frontend, the header approach is correct.

**Flat role hierarchy vs. permission-based access control**
Three named roles are easy to implement, test, and explain. A permission-flag system (`can_delete: bool`, `can_create: bool` per user) is more flexible but requires a permissions table, more complex dependency logic, and a more involved admin interface. For three well-defined roles, simpler wins.

**MySQL vs. PostgreSQL**
MySQL was chosen for local familiarity. PostgreSQL is generally preferred in production FastAPI stacks — better JSON support, more advanced indexing, and `asyncpg` is more mature than `aiomysql`. SQLAlchemy abstracts most dialect differences, so switching would mainly involve changing the connection string and driver.

---

## Author

Built by **Mani** as a portfolio/learning project demonstrating backend API design with FastAPI, SQLAlchemy, and role-based access control.
