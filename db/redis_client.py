
import redis

from config.settings import REDIS_URL

if REDIS_URL is None:
    raise RuntimeError("REDIS_URL environment variable is not set")

redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=True,
)