from models.db_schema.document import Document
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete , exists
from typing import Hashable



class DocumentRepository:
    
    def __init__(self, session:AsyncSession):
        self.session = session


    async def is_document_exists(self,hash:Hashable):
        stmt = select(
            exists().where(Document.hash==hash)
        )
        result = await self.session.execute(stmt)

        return result.scalar()
    
    async def insert_document(self,document:Document):
        if await self.is_document_exists(document.hash): 
            return False
        else:
            self.session.add(document)
            await self.session.commit()
            await self.session.refresh(document)

            return True
        

    async def insert_many_documents(self,documents:list[Document]):
        counter = 0
        for document in documents:
            if await self.is_document_exists(document.hash):
                
                continue
            else:
                counter += 1
                await self.session.add(document)
        
        await self.session.commit()
        return True , counter
    
    async def delete_document(self,document_id:int):
        stmt = delete(Document).where(Document.id==document_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount
    
    async def delete_documents_by_department_id(self,departmet_id:int):
        stmt = delete(Document).where(Document.department_id==departmet_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount
    

    async def get_documents_by_department_id(self,departmet_id:int):
        stmt = select(Document).where(Document.department_id == departmet_id)

        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_document_by_id(self,document_id:int):
        stmt = select(Document).where(Document.id == document_id)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()