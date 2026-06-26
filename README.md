# Plux

Sistema de gestión de SRGs (Service Request Guarantee) para concesionarias automotrices. Permite administrar solicitudes de garantía y campañas de recall, con trazabilidad de estados, checklist por rol y registro de auditoría.

---

## Stack

| Layer     | Technology                                     |
|-----------|------------------------------------------------|
| Frontend  | Next.js 15, React 19, TypeScript, Tailwind CSS |
| Backend   | Django 5, Django REST Framework, SimpleJWT     |
| Database  | PostgreSQL 17                                  |
| Docs API  | drf-spectacular (Swagger / ReDoc)              |
| Container | Docker + Docker Compose                        |

**Backend architecture:** Hexagonal (Clean Architecture) — `domain / application / infrastructure / interfaces`

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) ≥ 4.x
- Docker Compose v2 (bundled with Docker Desktop)

> Running without Docker requires Python ≥ 3.12 and Node.js ≥ 20.

---

## Quick Start (Docker — recommended)

```bash
# 1. Clone the repo
git clone <repo-url>
cd plux

# 2. Set up environment variables
cp .env.example .env
#    Edit .env and set a real SECRET_KEY at minimum

# 3. Start all services (postgres + backend + frontend)
docker compose up --build
```

| Service  | URL                                    |
|----------|----------------------------------------|
| Frontend | http://localhost:3000                  |
| Backend  | http://localhost:8000                  |
| Swagger  | http://localhost:8000/api/v1/docs/     |
| ReDoc    | http://localhost:8000/api/v1/redoc/    |

On first run, `docker compose up` will:
1. Pull the PostgreSQL image and initialize the schema via `infrastructure/postgres/init.sql`
2. Build the Django image, run migrations, and start the dev server
3. Build the Next.js image and start the dev server with hot reload

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```env
# Database
POSTGRES_DB=plux_db
POSTGRES_USER=plux_user
POSTGRES_PASSWORD=plux_password

# Django
SECRET_KEY=your-secret-key-here   # generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,backend

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

> `SECRET_KEY` is the only value that **must** be changed before running in any environment.

---

## Running Without Docker

### Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# Install dependencies
pip install -r requirements.txt
pip install -r requirements.dev.txt   # dev extras (pytest, etc.)

# Configure environment
cp ../.env.example ../.env
# Edit .env with your local DB credentials

# Run migrations and start server
python manage.py migrate
python manage.py runserver
```

Backend available at `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at `http://localhost:3000`.

---

## Project Structure

```
plux/
├── backend/
│   └── src/
│       ├── config/          # Django settings (base / development / production)
│       ├── domain/          # Entities, value objects, domain services, exceptions
│       ├── application/     # Use cases / application services
│       ├── infrastructure/  # ORM models, repositories, external integrations
│       └── interfaces/
│           ├── api/         # DRF controllers, serializers, URL routing
│           └── admin/       # Django Admin configuration
├── frontend/
│   └── src/
│       ├── app/             # Next.js App Router pages and layouts
│       ├── modules/         # Feature modules (auth, srg, catalog, dashboard, users, audit)
│       ├── components/      # Shared UI components
│       ├── services/        # API client layer (axios + React Query)
│       ├── store/           # Global state (Zustand)
│       ├── hooks/           # Custom React hooks
│       └── types/           # TypeScript type definitions
├── infrastructure/
│   └── postgres/
│       └── init.sql         # DB initialization script
├── docker-compose.yml
└── .env.example
```

---

## API Overview

Base path: `/api/v1/`

| Resource              | Endpoint                                    | Description                        |
|-----------------------|---------------------------------------------|------------------------------------|
| Auth — login          | `POST /auth/login/`                         | Obtain JWT access + refresh tokens |
| Auth — refresh        | `POST /auth/refresh/`                       | Refresh access token               |
| Auth — logout         | `POST /auth/logout/`                        | Blacklist refresh token            |
| SRGs                  | `GET/POST /srgs/`                           | List and create SRGs               |
| SRG — warranty        | `POST /srgs/warranty/`                      | Create warranty SRG                |
| SRG — campaign        | `POST /srgs/campaign/`                      | Create campaign (recall) SRG       |
| SRG — transition      | `POST /srgs/{id}/transition/`               | Advance SRG status                 |
| SRG — parts           | `GET/POST /srgs/{id}/parts/`                | Manage spare parts for an SRG      |
| SRG — checklist       | `GET/PATCH /srgs/{id}/checklist/{role}/`    | Role-based checklist               |
| SRG — campaign body   | `GET/PUT /srgs/{id}/campaign-body/`         | Campaign-specific body data        |
| Dashboard             | `GET /dashboard/`                           | Aggregate KPIs                     |
| Users                 | `GET/POST /users/`                          | User management                    |
| Catalog params        | `GET /catalog/params/`                      | Lookup/catalog parameters          |
| Spare parts catalog   | `GET /catalog/spare-parts/`                 | Spare parts catalog                |
| Audits                | `GET /audits/`                              | Audit log                          |

Full interactive docs at `http://localhost:8000/api/v1/docs/`.

---

## Demo Data & Login Credentials

The project ships with a **seed command** that loads one account per role plus a
realistic set of SRGs (warranty and campaign), catalog parameters, spare parts
and audits across the three dealerships. Run it once after the database is up:

```bash
# Docker
docker compose exec backend python manage.py seed

# Without Docker
cd backend && python manage.py seed
```

> The command is **idempotent** — run it again to refresh data without
> duplicating rows. Use `python manage.py seed --flush` to wipe the demo SRGs
> and audits before reseeding.

Then log in at `http://localhost:3000`. Every demo account uses the same
password: **`Plux2024!`**

| Role           | Email                  | Password    | Dealership      | Sees                                            |
|----------------|------------------------|-------------|-----------------|-------------------------------------------------|
| `SUPER_ADMIN`  | `superadmin@plux.com`  | `Plux2024!` | All (consolidated) | Everything: dashboard, SRGs, catalog, users, audits |
| `JEFE_TALLER`  | `jefe@plux.com`        | `Plux2024!` | Surmotor        | Dashboard, SRGs, catalog, users, audits          |
| `ASESOR`       | `asesor@plux.com`      | `Plux2024!` | Surmotor        | SRGs (create + advance status)                   |
| `BODEGUERO`    | `bodeguero@plux.com`   | `Plux2024!` | Surmotor        | SRGs + warehouse checklist                        |
| `AUDITOR`      | `auditor@plux.com`     | `Plux2024!` | Surmotor        | SRGs + audits                                     |

> **Tip:** the login screen has quick-fill buttons for each role — one click
> fills the form so you can jump in without typing.

Two extra advisor accounts (`asesor.granda@plux.com`, `asesor.shyris@plux.com`,
same password) own the SRGs of the other dealerships so the super-admin
consolidated view spans all three. To create more users with specific roles and
dealership (`concesionaria`), use the Users API or the Django Admin at
`http://localhost:8000/admin/` (log in with `superadmin@plux.com`).

---

## SRG Status Flow

```
PROCESO → PENDIENTE → PREAPROBADO → APROBADO → CERRADO
                                  ↘ RECHAZADO
```

**Campaign SRGs** can transition directly `PROCESO → APROBADO`, skipping intermediate states.

The checklist becomes available only when an SRG reaches `APROBADO` status.

---

## Running Tests

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm test           # unit tests (Vitest)
npm run test:e2e   # end-to-end (Playwright)
```

---

## Useful Commands

```bash
# Rebuild a single service without restarting others
docker compose up --build backend

# Run a one-off Django management command inside the container
docker compose exec backend python manage.py createsuperuser

# Reset the database (WARNING: destroys all data)
docker compose down -v
docker compose up --build

# View logs for a specific service
docker compose logs -f backend
```
