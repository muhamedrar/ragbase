from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime ,UTC



class Department(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True,index=True, nullable=False)
    created_at: str = Field(default_factory=datetime.now(UTC), nullable=False)

    documents: list["Document"] = Relationship(back_populates="department")
    