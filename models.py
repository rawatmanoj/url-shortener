from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class URL(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_code: Mapped[str] = mapped_column(String(8), unique=True)
    original_url: Mapped[str] = mapped_column(Text)
    clicks: Mapped[int] = mapped_column(Integer, default=0)

