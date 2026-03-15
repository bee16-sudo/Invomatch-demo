# backend/app/core/cache.py
# Redis caching is available in the full version
# https://github.com/your-username/invomatch-full

async def get_cached_dashboard(user_id: str):
    return None  # No cache in demo — upgrade for Redis caching

async def set_cached_dashboard(user_id: str, data: dict, ttl: int = 300):
    pass  # No cache in demo
