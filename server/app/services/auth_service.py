from sqlalchemy.orm import Session
from app.models.logoped import Logoped
from app.models.logoped_auth import LogopedAuth
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, email: str, password: str, name: str, surname: str) -> dict:
        if self.db.query(LogopedAuth).filter(LogopedAuth.email == email).first():
            raise ValueError("Email уже зарегистрирован")

        logoped = Logoped(name=name, surname=surname)
        self.db.add(logoped)
        self.db.flush()

        auth = LogopedAuth(
            logoped_id=logoped.id,
            email=email,
            password_hash=hash_password(password),
        )
        self.db.add(auth)
        self.db.commit()

        return {
            "access_token": create_access_token(logoped.id),
            "refresh_token": create_refresh_token(logoped.id),
        }

    def login(self, email: str, password: str) -> dict:
        auth = self.db.query(LogopedAuth).filter(LogopedAuth.email == email).first()
        if not auth or not verify_password(password, auth.password_hash):
            raise ValueError("Неверный email или пароль")

        return {
            "access_token": create_access_token(auth.logoped_id),
            "refresh_token": create_refresh_token(auth.logoped_id),
        }

    def refresh(self, refresh_token: str) -> dict:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("Требуется refresh-токен")

        logoped_id = int(payload["sub"])
        logoped = self.db.query(Logoped).filter(Logoped.id == logoped_id).first()
        if not logoped:
            raise ValueError("Пользователь не найден")

        return {
            "access_token": create_access_token(logoped.id),
            "refresh_token": create_refresh_token(logoped.id),
        }

    def get_me(self, logoped_id: int) -> Logoped:
        logoped = self.db.query(Logoped).filter(Logoped.id == logoped_id).first()
        if not logoped:
            raise ValueError("Пользователь не найден")
        return logoped