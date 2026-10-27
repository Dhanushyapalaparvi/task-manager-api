from pydantic import BaseModel,ConfigDict,Field
from typing import Literal

Priority = Literal["low","medium","high"]

class TaskCreate(BaseModel):
    title:str = Field(min_length=1,max_length=100)
    description: str | None = Field(default=None,max_length=500)
    completed:bool = False
    priority: Priority = "medium"

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    title: str
    description: str | None
    completed: bool
    priority: Priority

class TaskUpdate(BaseModel):
    title : str = Field(min_length=1,max_length=100)
    description: str | None = Field(default=None,max_length=500)
    completed: bool
    priority : Priority = "medium"

class TaskPatch(BaseModel):
    title: str = Field(
        default= None,
        min_length=1,
        max_length=100,
    )
    description: str | None = Field(
        default = None,
        max_length = 500,
    )
    completed: bool = None
    priority: Priority  = None    
    