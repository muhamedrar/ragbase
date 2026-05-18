from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,insert
from models.db_schema.chunk import Chunk
from openai import AsyncOpenAI
from helpers.settings import Settings
from models.db_schema.embedding import Embedding
from typing import Optional
import logging
from utils.openai_decorators import handle_openai_errors

logger = logging.getLogger("uvicorn.error")


class EmbeddingService:
    def __init__(self,Settings:Settings,OpenAI_client:AsyncOpenAI,session:AsyncSession,document_id:int ,batch_size:Optional[int]=10):
        self.Settings = Settings
        self.session = session
        self.document_id = document_id
        self.OpenAI_client = OpenAI_client
        self.batch_size = batch_size
        
    async def get_document_chunks(self):
        stmt = select(Chunk).where(Chunk.document_id==self.document_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    @handle_openai_errors
    async def make_embedings_objs(self):
        chunks = await self.get_document_chunks()
        
        def batch_list(items: list, batch_size: int):
            for i in range(0, len(items), batch_size):
                yield items[i:i + batch_size]

        all_embeddings_objs = []
        
        total_chunks = len(chunks)
        total_batches = (total_chunks + self.batch_size - 1) // self.batch_size if total_chunks > 0 else 0
        current_batch_idx = 1

        for batch in batch_list(chunks, self.batch_size):

            logger.info(f"Processing batch {current_batch_idx}/{total_batches} (Size: {len(batch)} chunks)")
            
            texts = [c.content for c in batch]

            response = await self.OpenAI_client.embeddings.create(
                input=texts,
                dimensions=self.Settings.MODEL_DIMENSION_SIZE,
                model=self.Settings.OPENAI_EMBEDING_MODEL,
            )

            embeddings = [item.embedding for item in response.data]

            embedings_obj = [
                Embedding(
                    chunk_id=chunk.id,
                    embedding=emb
                )
                for chunk, emb in zip(batch, embeddings)
            ]

            all_embeddings_objs.extend(embedings_obj)
            current_batch_idx += 1
            
        logger.info(f"Finished embedding all {total_chunks} chunks across {total_batches} batches.")
        return all_embeddings_objs

      
    
    async def insert_embedings(self):
        embedings = await self.make_embedings_objs()
        self.session.add_all(embedings)
        await self.session.commit()
        return len(embedings)