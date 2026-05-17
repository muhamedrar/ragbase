from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,insert,text
from models.db_schema.chunk import Chunk
from openai import AsyncOpenAI
from helpers.settings import Settings
from models.db_schema.embedding import Embedding
from models.db_schema.chunk import Chunk
from typing import Optional,List
import logging


class GenerationModelService:
    def __init__(self,Settings:Settings,OpenAI_client:AsyncOpenAI,session:AsyncSession):
        self.Settings = Settings
        self.session = session
        self.OpenAI_client = OpenAI_client

    async def embed_query(self,query:str):
        response = await self.OpenAI_client.embeddings.create(
                input=query,
                dimensions=self.Settings.MODEL_DIMENSION_SIZE,
                model=self.Settings.OPENAI_EMBEDING_MODEL,
            )
        
        return response.data[0].embedding
    
    async def construct_prompt(self,query:str):
        prompt = query
        return prompt
    
    async def search_vector_db(self,query:str, limit:int):
        query_ebed = await self.embed_query(query=query)
        stmt = text("""
                        SELECT
                                e.id as id ,
                                c.content as content ,
                                (1 - (e.embedding <=> :embedding)) as score
                        FROM embedding e
                        INNER JOIN chunk c
                        ON e.chunk_id = c.id
                        ORDER BY e.embedding <=> :embedding
                        LIMIT :limit;
                    """)
        results = await self.session.execute(
                                            stmt, 
                                            {"embedding": str(query_ebed), "limit": limit}
                                        )
        return results.all()
