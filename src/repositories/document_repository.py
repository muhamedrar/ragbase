from models.db_schema.document import Document
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete , exists
import logging
from typing import Hashable

logger = logging.getLogger("uvicorn.error")

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
            logger.warning("Document with the same content already exists")
            return None
        else:
            await self.session.add(document)
            await self.session.commit()
            await self.session.refresh(document)

            return True
        

    async def insert_many_documents(self,documents:list[Document]):
        counter = 0
        for document in documents:
            if await self.is_document_exists(document.hash):
                logger.warning(f"Document {document.doc_name_id} with the same content already exists")
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