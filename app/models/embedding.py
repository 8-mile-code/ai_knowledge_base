from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from app.db.base import Base, TimestampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .chunk import Chunk


class Embedding(Base, TimestampMixin):
    __tablename__ = "embeddings"

    id: Mapped[int] = mapped_column(primary_key=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))

    chunk_id: Mapped[int] = mapped_column(
        ForeignKey("chunks.id"), unique=True, index=True
    )

    chunk: Mapped["Chunk"] = relationship(back_populates="embedding")
