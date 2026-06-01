from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.homework import HomeworkCreate, HomeworkResponse, HomeworkLinkResponse
from app.schemas.answer import AnswerResponse
from app.services.homework_service import HomeworkService
from app.auth import get_current_logoped
from app.models.logoped import Logoped

logoped_router = APIRouter(prefix="/homework", tags=["homework"])
public_router = APIRouter(prefix="/public/homework", tags=["public"])


# === Логопед ===

@logoped_router.post("/", response_model=HomeworkResponse, status_code=201)
def assign_homework(
    data: HomeworkCreate,
    current: Logoped = Depends(get_current_logoped),
    db: Session = Depends(get_db),
):
    service = HomeworkService(db)
    try:
        return service.assign(data.pupil_id, data.module_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@logoped_router.get("/", response_model=list[HomeworkResponse])
def list_homework(
    pupil_id: int,
    current: Logoped = Depends(get_current_logoped),
    db: Session = Depends(get_db),
):
    service = HomeworkService(db)
    return service.get_by_pupil(pupil_id)


@logoped_router.get("/{homework_id}/link", response_model=HomeworkLinkResponse)
def get_homework_link(
    homework_id: int,
    current: Logoped = Depends(get_current_logoped),
    db: Session = Depends(get_db),
):
    service = HomeworkService(db)
    try:
        link = service.get_link(homework_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"link": link}


@logoped_router.get("/{homework_id}/answers", response_model=list[AnswerResponse])
def get_answers(
    homework_id: int,
    current: Logoped = Depends(get_current_logoped),
    db: Session = Depends(get_db),
):
    service = HomeworkService(db)
    return service.get_answers(homework_id)


@logoped_router.get("/answers/{answer_id}", response_model=AnswerResponse)
def get_answer(
    answer_id: int,
    current: Logoped = Depends(get_current_logoped),
    db: Session = Depends(get_db),
):
    service = HomeworkService(db)
    answer = service.get_answer(answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Ответ не найден")
    return answer


# === Ученик (публичные) ===

@public_router.get("/{token}")
def get_public_module(token: str, db: Session = Depends(get_db)):
    service = HomeworkService(db)
    homework = service.get_by_token(token)
    if not homework:
        raise HTTPException(status_code=404, detail="Задание не найдено")

    module = homework.module
    return {
        "id": module.id,
        "title": module.title,
        "description": module.description,
        "homework_id": homework.id,
        "status": homework.status,
        "tasks": [
            {
                "task_id": mt.task_id,
                "order_index": mt.order_index,
                "title": mt.task.title,
                "description": mt.task.description,
            }
            for mt in module.module_tasks
        ],
    }


@public_router.post("/{token}/answer", response_model=AnswerResponse)
def submit_answer(
    token: str,
    card_id: int = Form(...),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    service = HomeworkService(db)
    try:
        file_url = None
        if file:
            file_url = f"/uploads/{file.filename}"
        return service.submit_answer(token, card_id, file_url)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@public_router.get("/{token}/status")
def get_homework_status(token: str, db: Session = Depends(get_db)):
    service = HomeworkService(db)
    homework = service.get_by_token(token)
    if not homework:
        raise HTTPException(status_code=404, detail="Задание не найдено")
    return {
        "status": homework.status,
        "assigned_at": homework.assigned_at,
        "completed_at": homework.completed_at,
    }