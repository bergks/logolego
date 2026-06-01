from app.db import SessionLocal
from app.models.task_type import TaskType


def seed_task_types():
    db = SessionLocal()
    try:
        existing = db.query(TaskType).count()
        if existing > 0:
            print(f"Таблица task_types уже содержит {existing} записей, пропускаем.")
            return

        types = [
            TaskType(id=1, name="Артикуляционная гимнастика"),
            TaskType(id=2, name="Дифференциация звуков"),
            TaskType(id=3, name="Автоматизация звука"),
            TaskType(id=4, name="Авторское задание"),
        ]
        db.add_all(types)
        db.commit()
        print("Типы заданий добавлены.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_task_types()