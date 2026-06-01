from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class PupilHomework(Base):
    __tablename__ = "pupil_homework"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pupil_id = Column(Integer, ForeignKey("pupil.id"), nullable=False)
    module_id = Column(Integer, ForeignKey("module.id"), nullable=False)
    public_token = Column(String, unique=True, nullable=False)
    status = Column(Integer, nullable=False, default=0)
    assigned_at = Column(DateTime, nullable=False, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

    module = relationship("Module", lazy="joined")
    pupil = relationship("Pupil", lazy="joined")