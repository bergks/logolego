from pydantic import BaseModel, EmailStr

class LogopedRegister(BaseModel):
    email: EmailStr
    name: str
    surname: str
    password: str

class LogopedLogin(BaseModel):
    email: EmailStr
    password: str

class LogopedResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str

    model_config = {"from_attributes": True}