from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):
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



