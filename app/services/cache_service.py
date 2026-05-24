import hashlib
import json
from typing import Any

from app.core.redis import redis_client


class CacheService:
    @staticmethod
    def build_key(prefix: str, *parts: str) -> str:
        """Build a stable cache key from a prefix and raw value.

        The raw value is hashed to keep Redis keys short and avoid storing
        potentially large or sensitive input directly in the key.
        """
        raw_key = ":".join(parts)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        return f"{prefix}:{key_hash}"

    @staticmethod
    async def get_json(key: str) -> Any | None:
        cached_value = await redis_client.get(key)

        if cached_value is None:
            return None

        return json.loads(cached_value)

    @staticmethod
    async def set_json(
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:
        await redis_client.set(
            key,
            json.dumps(value),
            ex=ttl,
        )
