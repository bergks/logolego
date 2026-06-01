from pydantic import BaseModel

class PupilCreate(BaseModel):
    name: str
    surname: str

class PupilResponse(BaseModel):
    id: int
    name: str
    surname: str

    model_config = {"from_attributes": True}