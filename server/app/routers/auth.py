from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.logoped import LogopedRegister, LogopedLogin, LogopedResponse
from app.schemas.token import TokenResponse, TokenRefresh
from app.services.auth_service import AuthService
from app.auth import get_current_logoped
from app.models.logoped import Logoped

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(data: LogopedRegister, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        tokens = service.register(data.email, data.password, data.name, data.surname)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return tokens


@router.post("/login", response_model=TokenResponse)
def login(data: LogopedLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        tokens = service.login(data.email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return tokens


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: TokenRefresh, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        tokens = service.refresh(data.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return tokens


@router.get("/me", response_model=LogopedResponse)
def get_me(current: Logoped = Depends(get_current_logoped)):
    auth = current.logoped_auth
    return {
        "id": current.id,
        "name": current.name,
        "surname": current.surname,
        "email": auth.email if auth else "",
    }