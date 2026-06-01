from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.task_card import TaskCard
from app.services.card_service import CardService


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.card_service = CardService(db)

    def get_all_tasks(self) -> list[Task]:
        return self.db.query(Task).all()

    def get_task(self, task_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create_task(self, type_id: int, title: str, description: str, cards: list[dict]) -> Task:
        task = Task(type_id=type_id, title=title, description=description)
        self.db.add(task)
        self.db.flush()

        for item in cards:
            task_card = TaskCard(
                task_id=task.id,
                card_id=item["card_id"],
                order_index=item["order_index"],
            )
            self.db.add(task_card)

        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task(self, task_id: int, title: str, description: str, cards: list[dict]) -> Task:
        task = self.get_task(task_id)
        if not task:
            raise ValueError("Задание не найдено")

        task.title = title
        task.description = description

        # Удаляем старые связи
        self.db.query(TaskCard).filter(TaskCard.task_id == task_id).delete()

        # Добавляем новые
        for item in cards:
            task_card = TaskCard(
                task_id=task.id,
                card_id=item["card_id"],
                order_index=item["order_index"],
            )
            self.db.add(task_card)

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int, delete_cards: bool = False) -> None:
        task = self.get_task(task_id)
        if not task:
            raise ValueError("Задание не найдено")

        # Сохраняем карточки до удаления связей
        cards_to_delete = [tc.card for tc in task.task_cards] if delete_cards else []

        # Удаляем связи
        self.db.query(TaskCard).filter(TaskCard.task_id == task_id).delete()
        self.db.flush()

        # Удаляем карточки, если нужно
        for card in cards_to_delete:
            content = self.card_service._get_content(card)
            if content:
                self.db.delete(content)
            self.db.delete(card)

        self.db.delete(task)
        self.db.commit()

    def is_used_in_modules(self, task_id: int) -> bool:
        from app.models.module_task import ModuleTask
        exists = self.db.query(ModuleTask).filter(ModuleTask.task_id == task_id).first()
        return exists is not None