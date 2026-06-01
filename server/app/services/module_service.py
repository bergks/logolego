from sqlalchemy.orm import Session
from app.models.module import Module
from app.models.module_task import ModuleTask
from app.services.task_service import TaskService


class ModuleService:
    def __init__(self, db: Session):
        self.db = db
        self.task_service = TaskService(db)

    def get_all_modules(self) -> list[Module]:
        return self.db.query(Module).all()

    def get_module(self, module_id: int) -> Module | None:
        return self.db.query(Module).filter(Module.id == module_id).first()

    def create_module(self, title: str, description: str, tasks: list[dict]) -> Module:
        module = Module(title=title, description=description)
        self.db.add(module)
        self.db.flush()

        for item in tasks:
            module_task = ModuleTask(
                module_id=module.id,
                task_id=item["task_id"],
                order_index=item["order_index"],
            )
            self.db.add(module_task)

        self.db.commit()
        self.db.refresh(module)
        return module

    def update_module(self, module_id: int, title: str, description: str, tasks: list[dict]) -> Module:
        module = self.get_module(module_id)
        if not module:
            raise ValueError("Модуль не найден")

        module.title = title
        module.description = description

        # Удаляем старые связи
        self.db.query(ModuleTask).filter(ModuleTask.module_id == module_id).delete()

        # Добавляем новые
        for item in tasks:
            module_task = ModuleTask(
                module_id=module.id,
                task_id=item["task_id"],
                order_index=item["order_index"],
            )
            self.db.add(module_task)

        self.db.commit()
        self.db.refresh(module)
        return module

    def delete_module(self, module_id: int, delete_tasks: bool = False) -> None:
        module = self.get_module(module_id)
        if not module:
            raise ValueError("Модуль не найден")

        # Сохраняем задания до удаления связей
        task_ids = [mt.task_id for mt in module.module_tasks] if delete_tasks else []

        # Удаляем связи
        self.db.query(ModuleTask).filter(ModuleTask.module_id == module_id).delete()
        self.db.flush()

        # Удаляем задания с карточками, если нужно
        if delete_tasks:
            for task_id in task_ids:
                self.task_service.delete_task(task_id, delete_cards=True)

        self.db.delete(module)
        self.db.commit()