from fastapi import UploadFile
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from models.db_schema.chunk import Chunk
from typing import List
# think in chunking and spliiter logic first

class _MarkdownOrTextLoader:

    def __init__(self, path: str):
        self.path = path

    def load(self):

        with open(self.path, "r", encoding="utf-8") as file:
            content = file.read()

        return [
            Document(
                page_content=content,
                metadata={
                    "source": self.path
                }
            )
        ]

class ChunckController:

    def __init__(self,path:str):
        self.path = path

    def get_file_ext(self):
        ext = Path(self.path).suffix
        return ext
    
    def get_loader(self):
        ext = self.get_file_ext()
        if ext in ['.txt','.md']:
            return _MarkdownOrTextLoader(self.path) 
        if ext == '.pdf':
            return PyMuPDFLoader(self.path)
        
    def split_text(self):
        loader = self.get_loader()
        ext = self.get_file_ext()


        content = loader.load()

        if ext == '.md':
            text_splitter = MarkdownHeaderTextSplitter(
                                    headers_to_split_on=[
                                                ("#", "h1"),
                                                ("##", "h2"),
                                                ("###", "h3"),
                                                ("####", "h4"),
                                            ]
                                        )
            markdown_text = content[0].page_content
            return text_splitter.split_text(markdown_text)
        

        if ext in ['.txt','.pdf']:
            text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
            )

            return text_splitter.split_documents(content)
        

    def make_chunk_object(self,chunks:List[Document] ,document_id:int,department_id:int) -> List[Chunk]:
        chunk_objs = []

        for idx, chunk in enumerate(chunks):

            chunk_objs.append(
                Chunk(
                    content=chunk.page_content,
                    meta=chunk.metadata,
                    order=idx,
                    department_id=department_id,
                    document_id=document_id
                )
            )

        return chunk_objs

        



    