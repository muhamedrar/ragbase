from sqlmodel import SQLModel, Field ,Relationship, JSON, Column
from datetime import datetime ,UTC
from sqlalchemy import Column, DateTime
from typing import Optional

class Chunk(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(nullable=False)
    meta: dict = Field( sa_column=Column(JSON))
    order: int = Field(nullable=False, index=True)
    document_id: int = Field(foreign_key="document.id", nullable=False,ondelete="CASCADE")
    department_id: int = Field(foreign_key="department.id", index=True, nullable=False,ondelete="CASCADE") 
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(UTC)
    )

    document: Optional["Document"] = Relationship(back_populates="chunks")
    department: Optional["Department"] = Relationship(back_populates="chunks")


