from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import Base

class LogopedModule(Base):
    __tablename__ = "logoped_module"

    logoped_id = Column(Integer, ForeignKey("logoped.id"), primary_key=True)
    module_id = Column(Integer, ForeignKey("module.id"), primary_key=True)