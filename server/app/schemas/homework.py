from pydantic import BaseModel
from datetime import datetime

class HomeworkCreate(BaseModel):
    pupil_id: int
    module_id: int

class HomeworkResponse(BaseModel):
    id: int
    pupil_id: int
    module_id: int
    public_token: str
    status: int
    assigned_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}

class HomeworkLinkResponse(BaseModel):
    link: str