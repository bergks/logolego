from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Logoped(Base):
    __tablename__ = "logoped"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    logoped_auth = relationship("LogopedAuth", back_populates="logoped", uselist=False, lazy="joined")