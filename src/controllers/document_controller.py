import os
from pathlib import Path
from fastapi import UploadFile
import aiofiles
import hashlib
import uuid

class DocumentController:
    # extract meta data 
    # hash function and validation
    # document size validation in settings
    # create unique name
    # get document by id

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
    
   


    async def generate_file_hash(self,file:UploadFile):

        hasher = hashlib.sha256()

        while chunk := await file.read(1024 * 1024):
            hasher.update(chunk)

        await file.seek(0)

        return hasher.hexdigest()