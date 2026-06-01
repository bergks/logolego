from pydantic import BaseModel

class ModuleTaskItem(BaseModel):
    task_id: int
    order_index: int

class ModuleCreate(BaseModel):
    title: str
    description: str
    tasks: list[ModuleTaskItem]

class ModuleResponse(BaseModel):
    id: int
    title: str
    description: str
    tasks: list[ModuleTaskItem]

    model_config = {"from_attributes": True}