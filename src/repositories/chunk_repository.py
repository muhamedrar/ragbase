from models.db_schema import chunk
from sqlalchemy.ext.asyncio import AsyncSession

class ChunkRepository:

    def __init__(self, session:AsyncSession):
        self.session = session


    async def create_chunk(self,data_chunk:dict):
        new_chunk = chunk(**data_chunk)
        
        self.session.add(new_chunk)
        self.session.commit(new_chunk)
        self.session.refresh(new_chunk)

        return chunk