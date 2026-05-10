from sqlmodel import SQLModel, Field ,Relationship
from datetime import datetime ,UTC
from typing import Optional

class Chunk(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(nullable=False)
    meta: dict = Field(nullable=False)
    order: int = Field(nullable=False, index=True)
    document_id: int = Field(foreign_key="document.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.now(UTC), nullable=False)

    document: Optional["Department"] = Relationship(back_populates="chunks")


