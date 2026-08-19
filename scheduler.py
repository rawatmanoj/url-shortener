from db.database import SessionLocal
from models import URL
from db.redis_client import redis_client
from sqlalchemy import update
import time
from redis.exceptions import ResponseError
from config.settings import FLUSH_INTERVAL


def flush_processing(short_code: str, session):
    clicks = redis_client.get(f"processing:{short_code}")

    if clicks is None:
        return

    stmt = (
        update(URL)
        .where(URL.short_code == short_code)
        .values(clicks=URL.clicks + int(clicks))
    )

    session.execute(stmt)

    # NOTE:
    # If we crash here after the DB commit but before deleting Redis,
    # this batch may be processed again after restart.
    redis_client.delete(f"processing:{short_code}")
    redis_client.srem("dirty_clicks", short_code)


while True:

    session = SessionLocal()

    try:
        # ------------------------
        # Recovery
        # ------------------------
        for key in redis_client.scan_iter(match="processing:*"):
            short_code = key.decode().split(":")[1]
            flush_processing(short_code, session)

        session.commit()

        # ------------------------
        # Normal Processing
        # ------------------------
        dirty_urls = redis_client.smembers("dirty_clicks")

        for short_code in dirty_urls:

            try:
                redis_client.rename(
                    f"clicks:{short_code}",
                    f"processing:{short_code}"
                )
            except ResponseError:
                # Source key doesn't exist
                continue

            flush_processing(short_code, session)

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

    time.sleep(FLUSH_INTERVAL)