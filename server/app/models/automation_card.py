from sqlalchemy import Column, Integer, String
from app.models.base import Base

class AutomationCard(Base):
    __tablename__ = "automation_card"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    sound = Column(String, nullable=False)
    road_type = Column(Integer, nullable=False)
    frequency = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    media = Column(String, nullable=False)