from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    is_done: bool

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    is_done: bool
