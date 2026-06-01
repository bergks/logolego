from sqlalchemy.orm import Session
from app.models.pupil import Pupil
from app.models.logoped_pupil import LogopedPupil


class PupilService:
    def __init__(self, db: Session):
        self.db = db

    def get_pupils(self, logoped_id: int) -> list[Pupil]:
        return (
            self.db.query(Pupil)
            .join(LogopedPupil)
            .filter(LogopedPupil.logoped_id == logoped_id)
            .all()
        )

    def get_pupil(self, pupil_id: int) -> Pupil | None:
        return self.db.query(Pupil).filter(Pupil.id == pupil_id).first()

    def create_pupil(self, logoped_id: int, name: str, surname: str) -> Pupil:
        pupil = Pupil(name=name, surname=surname)
        self.db.add(pupil)
        self.db.flush()

        link = LogopedPupil(logoped_id=logoped_id, pupil_id=pupil.id)
        self.db.add(link)

        self.db.commit()
        self.db.refresh(pupil)
        return pupil

    def update_pupil(self, pupil_id: int, name: str, surname: str) -> Pupil:
        pupil = self.get_pupil(pupil_id)
        if not pupil:
            raise ValueError("Ученик не найден")
        pupil.name = name
        pupil.surname = surname
        self.db.commit()
        self.db.refresh(pupil)
        return pupil

    def delete_pupil(self, pupil_id: int) -> None:
        pupil = self.get_pupil(pupil_id)
        if not pupil:
            raise ValueError("Ученик не найден")
        self.db.query(LogopedPupil).filter(LogopedPupil.pupil_id == pupil_id).delete()
        self.db.delete(pupil)
        self.db.commit()