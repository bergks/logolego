from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.pupil import PupilCreate, PupilResponse
from app.services.pupil_service import PupilService
from app.auth import get_current_logoped
from app.models.logoped import Logoped

router = APIRouter(prefix="/pupils", tags=["pupils"])


@router.get("/", response_model=list[PupilResponse])
def list_pupils(
    current: Logoped = Depends(get_current_logoped),
    db: Session = Depends(get_db),
):
    service = PupilService(db)
    return service.get_pupils(current.id)


@router.get("/{pupil_id}", response_model=PupilResponse)
def get_pupil(pupil_id: int, db: Session = Depends(get_db)):
    service = PupilService(db)
    pupil = service.get_pupil(pupil_id)
    if not pupil:
        raise HTTPException(status_code=404, detail="Ученик не найден")
    return pupil


@router.post("/", response_model=PupilResponse, status_code=201)
def create_pupil(
    data: PupilCreate,
    current: Logoped = Depends(get_current_logoped),
    db: Session = Depends(get_db),
):
    service = PupilService(db)
    return service.create_pupil(current.id, data.name, data.surname)


@router.put("/{pupil_id}", response_model=PupilResponse)
def update_pupil(pupil_id: int, data: PupilCreate, db: Session = Depends(get_db)):
    service = PupilService(db)
    try:
        return service.update_pupil(pupil_id, data.name, data.surname)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{pupil_id}", status_code=204)
def delete_pupil(pupil_id: int, db: Session = Depends(get_db)):
    service = PupilService(db)
    try:
        service.delete_pupil(pupil_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))