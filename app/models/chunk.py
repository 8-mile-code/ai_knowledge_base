from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from .document import Document
    from .embedding import Embedding


class Chunk(Base, TimestampMixin):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    index: Mapped[int] = mapped_column(Integer)

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"), index=True
    )

    document: Mapped["Document"] = relationship(back_populates="chunks")
    embedding: Mapped["Embedding"] = relationship(
        back_populates="chunk",
        cascade="all, delete-orphan",
        uselist=False,
    )
