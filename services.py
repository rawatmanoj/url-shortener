from models import URL
from utils import generate_short_code
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select,update
from db.redis_client import redis_client

def create_short_url(session, original_url: str):

    short_code = generate_short_code()

    url = URL(
        short_code=short_code,
        original_url=original_url
    )
    for _ in range(5):
        try:
            session.add(url)
            session.commit()

            return url
        except IntegrityError:
            session.rollback()
    
    RuntimeError("Failed to generate a unique short code")

def getOriginalUrl(shortUrl,session):
   cached_url = redis_client.get(f"url:{shortUrl}")
   
   if(cached_url):
     redis_client.incr(f"clicks:{shortUrl}")
     redis_client.sadd("dirty_clicks",shortUrl)
     return cached_url
   
   statement =  select(URL).where(URL.short_code == shortUrl)
   url = session.execute(statement).scalar_one_or_none()
   if url is None:
        return None

   try:
    redis_client.set(f"url:{shortUrl}", url.original_url)
    redis_client.incr(f"clicks:{shortUrl}")
    redis_client.sadd("dirty_clicks",shortUrl)

   except Exception:
    print("redis set failed")
    pass


   return url.original_url

