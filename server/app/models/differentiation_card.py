from sqlalchemy import Column, Integer, String
from app.models.base import Base

class DifferentiationCard(Base):
    __tablename__ = "differentiation_card"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    media = Column(String, nullable=False)
    sound = Column(String, nullable=False)