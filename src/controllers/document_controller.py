import os
from pathlib import Path
from fastapi import UploadFile
import aiofiles

class DocumentController:
    # extract meta data 
    # hash function and validation
    # document size validation in settings
    # create unique name
    # get document by id

    async def make_file_name(self,fileName:str):
        return fileName

    async def upload_document_to_department_path(self,department_path:str, file:UploadFile):

        file_name = await self.make_file_name(fileName=file.filename)
        file_path = os.path.join(department_path,file_name)

        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                await f.write(chunk)
        
        return True