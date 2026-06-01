from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Module(Base):
    __tablename__ = "module"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    module_tasks = relationship("ModuleTask", lazy="joined", cascade="all, delete-orphan")