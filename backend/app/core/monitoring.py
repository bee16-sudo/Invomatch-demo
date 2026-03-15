# backend/app/core/monitoring.py
# Prometheus monitoring is available in the full version
# https://github.com/your-username/invomatch-full

from starlette.requests import Request
from starlette.responses import Response

async def metrics_middleware(request: Request, call_next):
    return await call_next(request)

async def metrics_endpoint(request: Request) -> Response:
    return Response(content="# Metrics available in full version", media_type="text/plain")
