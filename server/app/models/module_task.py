from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class ModuleTask(Base):
    __tablename__ = "module_task"

    module_id = Column(Integer, ForeignKey("module.id"), primary_key=True)
    task_id = Column(Integer, ForeignKey("task.id"), primary_key=True)
    order_index = Column(Integer, nullable=False)

    module = relationship("Module", back_populates="module_tasks")
    task = relationship("Task", lazy="joined")