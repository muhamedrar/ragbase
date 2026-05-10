from sqlmodel import SQLModel, Field , Index, Relationship, JSON, Column
from datetime import datetime ,UTC
from typing import Optional

class Document(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    doc_name_id: str = Field(nullable=False)
    meta: dict = Field( sa_column=Column(JSON))
    hash: str = Field(nullable=False, unique=True, index=True)
    department_id: int = Field(foreign_key="department.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.now(UTC), nullable=False)

    chunks: list["Chunk"] = Relationship(back_populates="document")
    department: Optional["Department"] = Relationship(back_populates="documents")

    __table_args__ = (
        Index("idx_department_id_hash", "department_id", "hash"),
    )