from pydantic import BaseModel

class AnswerResponse(BaseModel):
    id: int
    homework_id: int
    card_id: int
    answer_url: str | None = None
    status: int

    model_config = {"from_attributes": True}