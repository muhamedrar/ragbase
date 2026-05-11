from models.db_schema.chunk import Chunk
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete


class ChunkRepository:

    def __init__(self, session:AsyncSession):
        self.session = session


    async def create_chunk(self,data_chunk:Chunk):
        new_chunk = Chunk(**data_chunk)
        
        await self.session.add(new_chunk)
        await self.session.commit()
        await self.session.refresh(new_chunk)

        return new_chunk
    

    
    async def delete_chunks_by_department_id(self,department_id:int):
        stmt = delete(Chunk).where(Chunk.department_id==department_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount
    

    async def get_chunk(self,chunk_id:int):
        chunk = await self.session.get(Chunk,chunk_id)
        if chunk == None:
            return None
        else:
            return chunk


    async def get_chunks_by_department_id(self,department_id:int, page:int= 1, page_limit:int = 20):

        stmt = select(Chunk)\
                .where(Chunk.department_id==department_id)\
                .order_by(Chunk.order)\
                .offset((page-1)*page_limit)\
                .limit(page_limit)
                
        
        result = await self.session.execute(stmt)

        return result.scalars().all()
    