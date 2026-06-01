from pydantic import BaseModel

class TaskCardItem(BaseModel):
    card_id: int
    order_index: int

class TaskCreate(BaseModel):
    type_id: int
    title: str
    description: str
    cards: list[TaskCardItem]

class TaskResponse(BaseModel):
    id: int
    type_id: int
    title: str
    description: str
    cards: list[TaskCardItem]
    used_in_modules: bool | None = None

    model_config = {"from_attributes": True}