from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime ,UTC



class Department(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True,index=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda:datetime.now(UTC), nullable=False)

    documents: list["Document"] = Relationship(back_populates="department")
    chunks: list["Chunk"] = Relationship(back_populates="department")