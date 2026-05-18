from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,insert,text
from models.db_schema.chunk import Chunk
from openai import AsyncOpenAI
from helpers.settings import Settings
from models.db_schema.embedding import Embedding
from models.db_schema.chunk import Chunk
from typing import Optional,List
import logging
from fastapi import HTTPException,status
import openai


logger = logging.getLogger("uvicorn.error")


class GenerationModelService:
    def __init__(self,Settings:Settings,OpenAI_client:AsyncOpenAI,session:AsyncSession):
        self.Settings = Settings
        self.session = session
        self.OpenAI_client = OpenAI_client

    async def embed_query(self,query:str):
        try:
            response = await self.OpenAI_client.embeddings.create(
                    input=query,
                    dimensions=self.Settings.MODEL_DIMENSION_SIZE,
                    model=self.Settings.OPENAI_EMBEDING_MODEL,
                )
            
            return response.data[0].embedding
        except openai.RateLimitError as e:
            logger.error(f"OpenAI API Rate Limit Exceeded: {e}")
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
            logger.error(f"OpenAI Invalid Request: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid request parameters for embedding: {e.message}"
            )

        except openai.APIConnectionError as e:
            logger.error(f"Failed to connect to OpenAI API: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to reach the embedding service provider network."
            )

        except openai.APIError as e:
            logger.error(f"OpenAI API returned a generic error: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="The embedding service provider returned an invalid response."
            )

        except Exception as e:
            logger.exception(f"Unexpected error while generating embedding: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected internal error occurred while processing your query."
            )
        
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
