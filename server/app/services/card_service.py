# app/services/card_service.py
from sqlalchemy.orm import Session
from app.models.card import Card
from typing import List
from app.models.articulation_card import ArticulationCard
from app.models.differentiation_card import DifferentiationCard
from app.models.automation_card import AutomationCard
from app.models.personal_task import PersonalTaskCard
from app.factories.card_factory import CardFactory


class CardService:
    def __init__(self, db: Session):
        self.db = db

    def get_cards_by_type(self, type_id: int) -> list[Card]:
        return self.db.query(Card).filter(Card.type_id == type_id).all()

    def get_card(self, card_id: int) -> Card | None:
        return self.db.query(Card).filter(Card.id == card_id).first()

    def get_all_cards(self) -> list[Card]:
        return self.db.query(Card).all()

    def get_card_with_content(self, card_id: int) -> tuple[Card, object] | None:
        card = self.get_card(card_id)
        if not card:
            return None
        content = self._get_content(card)
        return card, content

    def create_card(self, type_id: int, content_data: dict) -> Card:
        content = CardFactory.create_content(type_id, content_data)
        self.db.add(content)
        self.db.flush()  # чтобы получить content.id

        card = Card(type_id=type_id, content_id=content.id)
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def update_card(self, card_id: int, content_data: dict) -> Card:
        card = self.get_card(card_id)
        if not card:
            raise ValueError("Карточка не найдена")

        content = self._get_content(card)
        for key, value in content_data.items():
            setattr(content, key, value)

        self.db.commit()
        self.db.refresh(card)
        return card

    def delete_card(self, card_id: int) -> None:
        card = self.get_card(card_id)
        if not card:
            raise ValueError("Карточка не найдена")

        content = self._get_content(card)
        self.db.delete(content)
        self.db.delete(card)
        self.db.commit()

    def is_used_in_tasks(self, card_id: int) -> bool:
        from app.models.task_card import TaskCard
        exists = self.db.query(TaskCard).filter(TaskCard.card_id == card_id).first()
        return exists is not None

    def get_content(self, card: Card):
        return self._get_content(card)

    def _get_content(self, card: Card):
        model_class = CardFactory.TYPE_MAP.get(card.type_id)
        if not model_class:
            raise ValueError(f"Неизвестный тип карточки: {card.type_id}")
        return self.db.query(model_class).filter(model_class.id == card.content_id).first()