from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
from pgvector.sqlalchemy import Vector
from typing import Optional


class Embedding(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)

    chunk_id: int = Field(
        sa_column=Column(
            ForeignKey("chunk.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
            index=True
        )
    )

    embedding: list[float] = Field(
        sa_column=Column(
            Vector(1024),   
            nullable=False
        )
    )

    chunk: Optional["Chunk"] = Relationship()