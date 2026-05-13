import os
from pathlib import Path
from fastapi import UploadFile
import aiofiles
import hashlib
import uuid
from models.db_schema.document import Document
from controllers.department_controller import DepartmentController

class DocumentController:
    # document size validation in settings

    async def generate_file_name(self,fileName:str):
        path = Path(fileName)
        clean_name = path.stem.replace(" ", "_")
        return f"{uuid.uuid4().hex[:8]}_{clean_name}{path.suffix.lower()}"

    async def upload_document_to_department_path(self,department_path:str, file:UploadFile):

        file_name =file.filename
        file_path = os.path.join(department_path,file_name)

        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                await f.write(chunk)
        
        return True
    
   

    async def create_document_object(self,file:UploadFile,department_id:int) ->Document :
        file.filename = await self.generate_file_name(file.filename)
        meta = {
            "file_extension": Path(file.filename).suffix.lower(),
            "content_type": file.content_type,
        }
        hash = await self.generate_file_hash(file)

        document = Document(
            doc_name_id= file.filename,
            hash=hash,
            meta = meta,
            department_id=department_id
        )

        return document

    async def generate_file_hash(self,file:UploadFile):

        hasher = hashlib.sha256()

        while chunk := await file.read(1024 * 1024):
            hasher.update(chunk)

        await file.seek(0)

        return hasher.hexdigest()
    
    async def remove_document_from_storage(self,doc_name_id:str,department_name:str):
        department_controller = DepartmentController()
        department_path = department_controller.get_department_path(department_name=department_name)
        document_path = os.path.join(department_path,doc_name_id)
        os.remove(document_path)
        return True


