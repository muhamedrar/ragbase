from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,insert
from models.db_schema.chunk import Chunk
from openai import AsyncOpenAI
from helpers.settings import Settings
from models.db_schema.embedding import Embedding
from typing import Optional
import logging
from fastapi import HTTPException,status
import openai

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
    

    async def make_embedings_objs(self):
        chunks = await self.get_document_chunks()
        
        def batch_list(items: list, batch_size: int):
            for i in range(0, len(items), batch_size):
                yield items[i:i + batch_size]

        all_embeddings_objs = []
        
        total_chunks = len(chunks)
        total_batches = (total_chunks + self.batch_size - 1) // self.batch_size if total_chunks > 0 else 0
        current_batch_idx = 1

        try:
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

        except openai.RateLimitError as e:
            logger.error(f"OpenAI API Rate Limit Exceeded during batch {current_batch_idx}: {e}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="The embedding service is currently overloaded. Please try again later."
            )

        except openai.AuthenticationError as e:
            logger.critical(f"OpenAI Authentication Failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server configuration error (Authentication)."
            )

        except openai.BadRequestError as e:
            logger.error(f"OpenAI Invalid Request structure in batch {current_batch_idx}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid request data formatted for embedding: {e.message}"
            )

        except openai.APIConnectionError as e:
            logger.error(f"Network connection failed during batch {current_batch_idx}: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to reach the embedding service provider network."
            )

        except openai.APIError as e:
            logger.error(f"OpenAI API service error returned during batch {current_batch_idx}: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="The embedding service provider returned an invalid response."
            )

        except Exception as e:
            logger.exception(f"Unexpected processing breakdown on batch {current_batch_idx}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while compiling document embeddings."
            )
    
    
    async def insert_embedings(self):
        embedings = await self.make_embedings_objs()
        self.session.add_all(embedings)
        await self.session.commit()
        return len(embedings)