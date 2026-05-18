from pydantic import BaseModel, Field
from fastapi import Form

class DepartmentCreateParam(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=50
        
    )

class NlpSearchParam(BaseModel):
    query: str = Field(
        ...,
        min_length=5,   
        description="The natural language query string to search for."
    )
    limit :int = Field(
        default=3,  
        ge=1,      
        le=12,      
        description="The maximum number of search results to return."
    )

class DocumentProcessParam:
    def __init__(
        self,
        department_id:int = Form(...),
        chunk_size: int = Form(500), 
        chunk_overlap:int =  Form(100),
        do_reset: int = Form(1),
        
    ):
        self.department_id = department_id
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.do_reset = do_reset



