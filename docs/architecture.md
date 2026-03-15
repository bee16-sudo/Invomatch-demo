# InvoMatch — Architecture

## Overview

InvoMatch is a modular-monolith SaaS platform for invoice verification and payment tracking.
It is built to start simple and evolve toward microservices without redesign.

## System Diagram

```
┌──────────┐     ┌─────────────────┐
│  Browser │────▶│ Next.js Frontend│
└──────────┘     └────────┬────────┘
                          │ HTTPS
                          ▼
           ┌──────────────────────────┐
           │  FastAPI (Modular Monolith)│
           │                          │
           │  /users  /clients        │
           │  /invoices  /payments    │
           │  /dashboard              │
           └────┬─────────────────────┘
                │
       ┌────────┴────────┐
       ▼                 ▼
 ┌──────────┐     ┌────────────┐
 │PostgreSQL│     │Redis Cache │
 └──────────┘     └────┬───────┘
                       │ broker
                       ▼
                ┌──────────────┐
                │Celery Workers│
                │- verification│
                │- email       │
                └──────────────┘
```

## Modules

| Module        | Responsibility                         |
|---------------|----------------------------------------|
| `users`       | Registration, login, JWT auth          |
| `clients`     | Client CRUD, owned by user             |
| `invoices`    | Invoice lifecycle, business rules      |
| `payments`    | Payment recording, reconciliation      |
| `dashboard`   | Aggregated stats with Redis cache      |
| `workers`     | Background verification, email tasks   |

## Key Design Decisions

- **Repository pattern** — data access is encapsulated; services never touch the ORM directly
- **Service layer** — all business rules live in service classes; routes are thin
- **JWT auth** — stateless, scoped to `user_id`; every data query is user-scoped
- **Redis caching** — dashboard stats cached for 5 minutes; invalidated on mutation
- **Celery workers** — invoice verification runs async; retries up to 3× on failure
- **Modular monolith** — each feature in its own directory; can be extracted to a service later

## Data Model

```
User ─── Client ─── Invoice ─── Payment
                └── AuditLog
```

## Infrastructure

- Docker + Docker Compose for local development
- AWS ECS (Fargate) for production containers
- AWS RDS (PostgreSQL 15) for the database
- AWS ElastiCache (Redis 7) for caching and task broker
- AWS ECR for container images
- GitHub Actions for CI/CD
- Terraform for infrastructure as code
