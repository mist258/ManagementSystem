# Management system

**Python version** - 3.13
**Database** - PostgreSQL 18
**Containerization** - Docker 28
**Framework** - FastAPI

**Development tools:** alembic, SQLAlchemy, uvicorn, pydantic, pydantic-settings, asyncpg,
pyjwt, bcrypt, isort, python-multipart, pytest, pytest-asyncio, httpx, pytest-cov


## INSTALLATION AND LAUNCHING GUIDE


```bash
    1) git clone https://github.com/mist258/ManagementSystem.git

    2) Choose python interpreter (# if you use PyCharm)

    3) Create a .env  & .env.test file and fill in the variables listed in .env.example & .env.example_test

    3) poetry shell  (#initaialize environment)

    4) poetry install  (#install dependencies)

    4) docker compose build optional[--no-cache]

    5) docker compose up optional[-d]

    Optional, if the database wasn’t created, run the following command:

       docker exec -it [container_name] psql -U postgres[user_name] -c "CREATE DATABASE [db_name]";

    6) cd backend/ (#move to working dir)

    7) mkdir certs (#create dir for public & private keys)

    8) cd certs/ (# move to dir 'certs/' to generate keys)

    9) openssl genrsa -out jwt-private.pem 2048 (#primary you should generate private key)

    10) openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem (#the next step is generate public key)

    11) docker compose exec app alembic upgrade head (#to execute this command you should move to root project dir ManagementSystem/)

    12) docker compose exec app python cli.py create-superuser (#create superuser)

    13) docker compose exec app python seed.py (#seed database with initial data)

    14) docker compose exec app pytest tests/ -v --cov=. --cov-report=term-missing (#run tests)

```
## Authentication

JWT-based authentication with RS256 asymmetric encryption.

**Flow:**
1. Superuser creates a user via `/api/v1/users`
2. User logs in via `/api/v1/auth/login` with email and password
3. Server returns `access_token` and `refresh_token`
4. Client sends `access_token` in `Authorization: Bearer <token>` header
5. Use `refresh_token` to get a new `access_token` via `/api/v1/auth/refresh`

**Roles:**
- `superuser` — full access (True: is_superuser, is_staff, is_active)
- `editor` — can view and update any articles (True: is_staff, is_active; False: is_superuser)
- `user` — can manage own articles and view other articles (True: is_active, False: is_superuser, is_staff)

**Keys:**
- Private key — signs tokens (server only)
- Public key — verifies tokens
- Generate with:  `openssl genrsa -out jwt-private.pem 2048`
                  `openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem`




## Users API

| Method |             Endpoint              | Permission         | Description         |
|--------|-----------------------------------|--------------------|---------------------|
| GET    | `/api/v1/users/authors`           | Superuser          | Get all users       |
| GET    | `/api/v1/users/editors`           | Superuser          | Get all editors     |
| GET    | `/api/v1/users/search`            | Any                | Search users by name|
| POST   | `/api/v1/users`                   | Superuser          | Create a new user   |
| POST   | `/api/v1/users/editor`            | Superuser          | Create a new editor |
| GET    | `/api/v1/users/{user_id}`         | Superuser          | Get user by ID      |
| PUT    | `/api/v1/users/{user_id}`         | Superuser or owner | Update user         |
| DELETE | `/api/v1/users/{user_id}`         | Superuser          | Delete user         |
| PATCH  | `/api/v1/users/{user_id}/block`   | Superuser          | Deactivate user     |
| PATCH  | `/api/v1/users/{user_id}/unblock` | Superuser          | Activate user       |

****************************************************************************************

## Articles API

| Method |            Endpoint             | Permission               |         Description      |
|--------|---------------------------------|--------------------------|--------------------------|
| GET    | `/api/v1/articles`              | Any                      | Get all articles         |
| GET    | `/api/v1/articles/search`       | Any                      | Search articles by title |
| GET    | `/api/v1/articles/{article_id}` | Any                      | Get article by ID        |
| POST   | `/api/v1/articles`              | User, Superuser          | Create article           | 
| PUT    | `/api/v1/articles/{article_id}` | Owner, Editor, Superuser | Update article           |
| DELETE | `/api/v1/articles/{article_id}` | Owner, Superuser         | Delete article           |

**************************************************************************************************


## Auth API

| Method |          Endpoint      | Permission    | Description          |
|--------|------------------------|---------------|----------------------|
| POST   | `/api/v1/auth/login`   | Any           | Login and get tokens |
| GET    | `/api/v1/auth/me`      | Authenticated | Get my info          |
| POST   | `/api/v1/auth/refresh` | Authenticated | Get new access token |


**Special links**
- Health check: http://localhost:8002/health
- Documentation: http://localhost:8002/docs
