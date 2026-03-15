# backend/app/main.py — InvoMatch DEMO VERSION
# Full version: https://github.com/your-username/invomatch

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.core.exceptions import BusinessRuleError, NotFoundError
from app.core.monitoring import metrics_middleware, metrics_endpoint

from app.modules.users.routes import router as users_router
from app.modules.clients.routes import router as clients_router
from app.modules.invoices.routes import router as invoices_router
from app.modules.dashboard.routes import router as dashboard_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=f"{settings.APP_NAME} — Demo",
        version=settings.APP_VERSION,
        description=(
            "⚠️ **This is the DEMO version of InvoMatch.**\n\n"
            "Limits: 1 client, 1 invoice per account. "
            "Payments, background workers, Redis caching, "
            "Prometheus monitoring, CI/CD pipelines, and AWS Terraform "
            "are available in the **full version**.\n\n"
            "👉 [Get the full version](https://github.com/your-username/invomatch)"
        ),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.middleware("http")(metrics_middleware)

    init_db()

    @app.exception_handler(BusinessRuleError)
    async def business_rule_handler(request: Request, exc: BusinessRuleError):
        return JSONResponse(status_code=422, content={"detail": exc.message})

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": exc.message})

    app.include_router(users_router,    prefix="/api/v1/users",    tags=["Users"])
    app.include_router(clients_router,  prefix="/api/v1/clients",  tags=["Clients"])
    app.include_router(invoices_router, prefix="/api/v1/invoices", tags=["Invoices"])
    app.include_router(dashboard_router,prefix="/api/v1/dashboard",tags=["Dashboard"])

    @app.get("/health", tags=["System"])
    async def health():
        return {
            "status": "ok",
            "version": settings.APP_VERSION,
            "mode": "demo",
            "limits": {"clients": 1, "invoices": 1},
            "upgrade": "https://github.com/your-username/invomatch"
        }

    app.add_route("/metrics", metrics_endpoint)

    return app


app = create_app()
