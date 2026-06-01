from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class LogopedAuth(Base):
    __tablename__ = "logoped_auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    logoped_id = Column(Integer, ForeignKey("logoped.id"), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    logoped = relationship("Logoped", back_populates="logoped_auth")