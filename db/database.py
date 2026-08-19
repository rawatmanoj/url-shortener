import os

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL

# Ensure DATABASE_URL is set and non-None for type checkers and runtime
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=2,
    max_overflow=1,
)

SessionLocal = sessionmaker(bind=engine)

@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    print("🟢 New TCP Connection Created")


@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    print("📤 Connection Checked Out")


@event.listens_for(engine, "checkin")
def checkin(dbapi_connection, connection_record):
    print("📥 Connection Returned")

def get_DB():
    session = None
    try:
        session = SessionLocal()
        yield session
    finally:
        if session is not None:
            session.close()