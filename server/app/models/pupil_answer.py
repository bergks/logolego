from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base

class PupilAnswer(Base):
    __tablename__ = "pupil_answer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    homework_id = Column(Integer, ForeignKey("pupil_homework.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("card.id"), nullable=False)
    answer_url = Column(String, nullable=True)
    status = Column(Integer, nullable=False, default=0)