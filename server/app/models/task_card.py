from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import Base

class TaskCard(Base):
    __tablename__ = "task_card"

    task_id = Column(Integer, ForeignKey("task.id"), primary_key=True)
    card_id = Column(Integer, ForeignKey("card.id"), primary_key=True)
    order_index = Column(Integer, nullable=False)