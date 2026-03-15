<div align="center">

# InvoMatch

**Production-ready SaaS boilerplate — invoice management & payment tracking**

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square)](https://postgresql.org)
[![Demo](https://img.shields.io/badge/Version-Demo-orange?style=flat-square)](#)

### Stop spending 3 months building auth, databases, and deployment pipelines.
### Start with a working SaaS on day one.

[🚀 Live Demo](#live-demo) · [📦 Full Version](#get-the-full-version) · [📖 Docs](#api-overview)

</div>

---

## What is this?

InvoMatch is a **complete, working SaaS backend** built with FastAPI, PostgreSQL, and modern Python. It handles everything a real invoice management product needs — user accounts, client management, invoice lifecycle, payments, and a dashboard.

This is the **free demo version**. It lets you explore the code, run it locally, and see exactly what you're getting before you buy the full version.

---

## Live Demo

Try it right now — no setup needed:

> 🌐 **API:** [https://invomatch.onrender.com](https://invomatch.onrender.com/health)
>
> 📖 **Interactive Docs:** [https://invomatch.onrender.com/api/docs](https://invomatch.onrender.com/api/docs)

Register an account, create a client, raise an invoice — the full flow works live.

---

## Demo vs Full Version

| Feature | Demo (this repo) | Full Version |
|---------|:---:|:---:|
| User registration & login | ✅ | ✅ |
| JWT authentication | ✅ | ✅ |
| Client management | ✅ 1 max | ✅ Unlimited |
| Invoice management | ✅ 1 max | ✅ Unlimited |
| Basic dashboard | ✅ | ✅ |
| **Payment recording** | ❌ | ✅ |
| **Auto-reconciliation** | ❌ | ✅ |
| **Redis caching** | ❌ | ✅ |
| **Background workers (Celery)** | ❌ | ✅ |
| **Email notifications** | ❌ | ✅ |
| **Prometheus monitoring** | ❌ | ✅ |
| **AWS Terraform infrastructure** | ❌ | ✅ |
| **GitHub Actions CI/CD** | ❌ | ✅ |
| **Full test suite** | ❌ | ✅ |
| **Commercial license** | ❌ | ✅ |
| **Priority support** | ❌ | ✅ |

---

## Screenshots

### API Docs
> Interactive Swagger UI — test every endpoint directly in the browser

![API Docs](https://via.placeholder.com/800x400?text=API+Docs+Screenshot)

### Dashboard Response
```json
{
  "total_invoices": 12,
  "invoice_status": {
    "pending": 4,
    "verified": 1,
    "paid": 7,
    "disputed": 0
  },
  "total_clients": 4,
  "total_collected": "24850.00"
}
```

---

## Quick Start

```bash
git clone https://github.com/your-username/invomatch-demo
cd invomatch-demo
cp backend/.env.example backend/.env
docker-compose up --build
```

- API: http://localhost:8000
- Docs: http://localhost:8000/api/docs

Or deploy to **Render in 5 minutes** — see [docs/development.md](docs/development.md)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Python 3.11 |
| Database | PostgreSQL 15 |
| Auth | JWT + bcrypt |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic v2 |
| Deploy | Render / Docker |

---

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/register` | Register account |
| POST | `/api/v1/users/login` | Login, get JWT token |
| GET | `/api/v1/users/me` | Current user |
| POST | `/api/v1/clients` | Create client *(1 max in demo)* |
| GET | `/api/v1/clients` | List clients |
| POST | `/api/v1/invoices` | Create invoice *(1 max in demo)* |
| GET | `/api/v1/invoices` | List invoices |
| GET | `/api/v1/dashboard` | Stats |
| GET | `/health` | Health check |

---

## Project Structure

```
invomatch-demo/
├── backend/
│   ├── app/
│   │   ├── core/          # config, database, security
│   │   └── modules/
│   │       ├── users/     # auth — full in demo
│   │       ├── clients/   # CRUD — limited in demo
│   │       ├── invoices/  # lifecycle — limited in demo
│   │       └── dashboard/ # stats — basic in demo
├── frontend/              # HTML/CSS/JS UI
├── docs/                  # Architecture & setup guides
├── render.yaml            # Render deployment config
├── docker-compose.yml     # Local dev
└── start.sh               # Production start script
```

---

## Get the Full Version

The full version includes everything in this demo plus:

- ✅ **Unlimited** clients and invoices
- ✅ Payment recording with auto-reconciliation
- ✅ Redis caching for performance
- ✅ Celery background workers
- ✅ Email notifications
- ✅ Prometheus + Grafana monitoring
- ✅ AWS infrastructure with Terraform
- ✅ GitHub Actions CI/CD pipelines
- ✅ Full unit, integration and E2E test suite
- ✅ Commercial license — use in your product
- ✅ Priority support

### 💰 $39 — one-time payment, yours forever

> **[https://nowpayments.io/payment/?iid=5337662070](#)** *(crypto payments accepted)*
### If you wish to contact:
> **[bee613743@gmail.com](#)** *(Email me here)*
---

## License

This demo version is released under the **MIT License** — free to use, modify, and learn from.

The full version is sold under a Commercial License. See [full version](#get-the-full-version) for details.

---

## Questions?

Open an issue or email support@invomatch.io

---

<div align="center">
Built with FastAPI · PostgreSQL · Python 3.11
</div>
