from datetime import datetime
from sqlalchemy import String, Integer, JSON, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncAttrs


class PostRequest(BaseModel):
    title: str
    content: str
    category: str
    tags: list[str]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now())


class Post(Base):
    __tablename__ = "posts"

    post_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(String(500))
    category: Mapped[str] = mapped_column(String(50))
    tags: Mapped[dict] = mapped_column(JSON)

    def to_dict(self) -> dict:
        return {
            'post_id': self.post_id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
