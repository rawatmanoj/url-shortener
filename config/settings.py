import os

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
FLUSH_INTERVAL = int(os.getenv("FLUSH_INTERVAL", "300"))