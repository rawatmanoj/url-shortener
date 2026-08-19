from db.database import SessionLocal
from models import URL

session = SessionLocal()

url = URL(
    short_code="abc1234",
    original_url="https://google.com"
)

session.add(url)
session.commit()

print("Inserted successfully!")

session.close()