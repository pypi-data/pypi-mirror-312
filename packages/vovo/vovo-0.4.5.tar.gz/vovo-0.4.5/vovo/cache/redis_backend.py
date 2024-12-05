import pickle
from typing import Any
import json
from redis import asyncio as redis

from vovo.cache.base.backend import BaseBackend


class RedisBackend(BaseBackend):
    """Redis backend for caching."""

    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(url=redis_url, decode_responses=True)

    async def get(self, *, key: str) -> Any:
        result = await self.redis_client.get(key)
        if not result:
            return

        return json.loads(result)

    async def set(self, *, response: Any, key: str, ttl: int = 60) -> None:
        if isinstance(response, dict):
            response = json.dumps(response)
        else:
            response = json.dumps(response)

        await self.redis_client.set(name=key, value=response, ex=ttl)

    async def delete_startswith(self, *, value: str) -> None:
        async for key in self.redis_client.scan_iter(f"{value}*"):
            await self.redis_client.delete(key)
