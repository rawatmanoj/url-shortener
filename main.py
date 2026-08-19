from datetime import datetime, timezone
import os
import time

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from db.database import SessionLocal, get_DB
from schemas import ShortenRequest
from services import create_short_url, getOriginalUrl
app = FastAPI()

SERVER_NAME = os.getenv("SERVER_NAME", "Unknown")

@app.get("/db-test")
def db_test(session: Session = Depends(get_DB)):
    session.execute(text("SELECT pg_sleep(6)"))
    return {"ok": True}

@app.get("/")
def home(request: Request):
    return {
        "server": SERVER_NAME,
        "client": request.client.host if request.client else None,
        "host": request.headers.get("host"),
        "x_real_ip": request.headers.get("x-real-ip"),
        "x_forwarded_for": request.headers.get("x-forwarded-for"),
        "x_forwarded_proto": request.headers.get("x-forwarded-proto"),
    }

@app.get("/users")
def get_users():
    return ["Alice", "Bob"]

@app.get("/about")
def about():
    return {
        "application": "URL Shortener",
        "version": "1.0"
    }

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id
    }

@app.get("/cpu")
def cpu():
    total = 0

    for i in range(200_000_00):
        total += i

    return {"total": total}

@app.get("/slow")
def slow(request:Request):
    # print(f"Request handled by {SERVER_NAME}")
    if SERVER_NAME == "Server-1":
     time.sleep(5)
    print(f"Handled by {SERVER_NAME}")

    return {
        "server": SERVER_NAME,
        "client": request.client.host if request.client else None,
        "host": request.headers.get("host"),
        "x_real_ip": request.headers.get("x-real-ip"),
        "x_forwarded_for": request.headers.get("x-forwarded-for"),
        "x_forwarded_proto": request.headers.get("x-forwarded-proto"),
    }

@app.get("/time")
def get_time():
    print("🔥 FastAPI Executed")
    return {
        "time": datetime.now(timezone.utc).isoformat(),
        "server": SERVER_NAME
    }

@app.post("/shorten")
def shorten(request: ShortenRequest):

    session = SessionLocal()

    try:

        url = create_short_url(
            session=session,
            original_url=request.url
        )

        if not url:
            raise HTTPException(status_code=500, detail="Failed to create short URL")

        return {
            "short_code": url.short_code
        }

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

@app.get("/{short_code}")
def get_original_path(short_code: str,db: Session=Depends(get_DB)):

     url = getOriginalUrl(short_code,db)
     if url is None:
            raise HTTPException(
                status_code=404,
                detail="Short URL not found"
            )
      
     return RedirectResponse(url=url if isinstance(url, str) else url.decode())


    
