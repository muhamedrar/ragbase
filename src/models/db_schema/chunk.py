from sqlmodel import SQLModel, Field ,Relationship, JSON, Column
from datetime import datetime ,UTC
from typing import Optional

class Chunk(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(nullable=False)
    meta: dict = Field( sa_column=Column(JSON))
    order: int = Field(nullable=False, index=True)
    document_id: int = Field(foreign_key="document.id", nullable=False)
    department_id: int = Field(foreign_key="department.id", index=True) 
    created_at: datetime = Field(default_factory=datetime.now(UTC), nullable=False)

    document: Optional["Document"] = Relationship(back_populates="chunks")


