import uuid
from sqlalchemy.orm import Session
from app.models.pupil_homework import PupilHomework
from app.models.pupil_answer import PupilAnswer
from app.models.module import Module


class HomeworkService:
    def __init__(self, db: Session):
        self.db = db

    def assign(self, pupil_id: int, module_id: int) -> PupilHomework:
        # Проверяем, что модуль существует
        module = self.db.query(Module).filter(Module.id == module_id).first()
        if not module:
            raise ValueError("Модуль не найден")

        homework = PupilHomework(
            pupil_id=pupil_id,
            module_id=module_id,
            public_token=str(uuid.uuid4()),
            status=0,
        )
        self.db.add(homework)
        self.db.commit()
        self.db.refresh(homework)
        return homework

    def get_by_pupil(self, pupil_id: int) -> list[PupilHomework]:
        return (
            self.db.query(PupilHomework)
            .filter(PupilHomework.pupil_id == pupil_id)
            .all()
        )

    def get_by_token(self, token: str) -> PupilHomework | None:
        return (
            self.db.query(PupilHomework)
            .filter(PupilHomework.public_token == token)
            .first()
        )

    def get_link(self, homework_id: int) -> str:
        homework = (
            self.db.query(PupilHomework)
            .filter(PupilHomework.id == homework_id)
            .first()
        )
        if not homework:
            raise ValueError("Домашнее задание не найдено")
        return f"/public/homework/{homework.public_token}"

    def get_answers(self, homework_id: int) -> list[PupilAnswer]:
        return (
            self.db.query(PupilAnswer)
            .filter(PupilAnswer.homework_id == homework_id)
            .all()
        )

    def get_answer(self, answer_id: int) -> PupilAnswer | None:
        return self.db.query(PupilAnswer).filter(PupilAnswer.id == answer_id).first()

    def submit_answer(self, token: str, card_id: int, file_url: str | None = None) -> PupilAnswer:
        homework = self.get_by_token(token)
        if not homework:
            raise ValueError("Домашнее задание не найдено")

        answer = PupilAnswer(
            homework_id=homework.id,
            card_id=card_id,
            answer_url=file_url,
            status=1,
        )
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer