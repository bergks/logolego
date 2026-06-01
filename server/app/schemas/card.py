from pydantic import BaseModel
from typing import Union


class ArticulationCardContent(BaseModel):
    id: int
    title: str
    media: str
    description: str | None = None
    answer_type: int


class DifferentiationCardContent(BaseModel):
    id: int
    name: str
    media: str
    sound: str


class AutomationCardContent(BaseModel):
    id: int
    title: str
    sound: str
    road_type: int
    frequency: int
    speed: int
    media: str


class PersonalTaskContent(BaseModel):
    id: int
    title: str
    media: str
    description: str | None = None
    answer_type: int


CardContent = Union[
    ArticulationCardContent,
    DifferentiationCardContent,
    AutomationCardContent,
    PersonalTaskContent,
]


class CardCreate(BaseModel):
    type_id: int
    content: dict


class CardResponse(BaseModel):
    id: int
    type_id: int
    content: CardContent
    used_in_tasks: bool | None = None

    model_config = {"from_attributes": True}