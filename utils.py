import random
import string
from db.database import SessionLocal


def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits

    return "".join(
        random.choice(characters)
        for _ in range(length)
    )


        

