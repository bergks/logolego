from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import TaskService
from app.auth import get_current_logoped
from app.models.logoped import Logoped

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _task_to_response(service, task):
    return {
        "id": task.id,
        "type_id": task.type_id,
        "title": task.title,
        "description": task.description,
        "cards": [
            {"card_id": tc.card_id, "order_index": tc.order_index}
            for tc in task.task_cards
        ],
        "used_in_modules": service.is_used_in_modules(task.id),
    }


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    current: Logoped = Depends(get_current_logoped),
    db: Session = Depends(get_db),
):
    service = TaskService(db)
    tasks = service.get_all_tasks()
    return [_task_to_response(service, task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current: Logoped = Depends(get_current_logoped),
    db: Session = Depends(get_db),
):
    service = TaskService(db)
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задание не найдено")
    return _task_to_response(service, task)


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    data: TaskCreate,
    current: Logoped = Depends(get_current_logoped),
    db: Session = Depends(get_db),
):
    service = TaskService(db)
    try:
        task = service.create_task(
            type_id=data.type_id,
            title=data.title,
            description=data.description,
            cards=[c.model_dump() for c in data.cards],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _task_to_response(service, task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskCreate,
    current: Logoped = Depends(get_current_logoped),
    db: Session = Depends(get_db),
):
    service = TaskService(db)
    try:
        task = service.update_task(
            task_id=task_id,
            title=data.title,
            description=data.description,
            cards=[c.model_dump() for c in data.cards],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return _task_to_response(service, task)


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    delete_cards: bool = Query(default=False),
    current: Logoped = Depends(get_current_logoped),
    db: Session = Depends(get_db),
):
    service = TaskService(db)
    try:
        service.delete_task(task_id, delete_cards=delete_cards)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))