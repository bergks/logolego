from app.models.card import Card
from app.models.articulation_card import ArticulationCard
from app.models.differentiation_card import DifferentiationCard
from app.models.automation_card import AutomationCard
from app.models.personal_task import PersonalTaskCard

class CardFactory:

    TYPE_MAP = {
        1: ArticulationCard,
        2: DifferentiationCard,
        3: AutomationCard,
        4: PersonalTaskCard,
    }

    @staticmethod
    def create_content(type_id: int, data: dict):
        card_class = CardFactory.TYPE_MAP.get(type_id)
        if card_class is None:
            raise ValueError(f"Неизвестный тип карточки: {type_id}")
        return card_class(**data)