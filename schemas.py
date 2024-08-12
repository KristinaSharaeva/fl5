from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str = None
    is_completed: bool = False

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    is_completed: bool = None
