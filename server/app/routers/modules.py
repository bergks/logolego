from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.module import ModuleCreate, ModuleResponse
from app.services.module_service import ModuleService

router = APIRouter(prefix="/modules", tags=["modules"])


def _module_to_response(module):
    return {
        "id": module.id,
        "title": module.title,
        "description": module.description,
        "tasks": [
            {"task_id": mt.task_id, "order_index": mt.order_index}
            for mt in module.module_tasks
        ],
    }


@router.get("/", response_model=list[ModuleResponse])
def list_modules(db: Session = Depends(get_db)):
    service = ModuleService(db)
    modules = service.get_all_modules()
    return [_module_to_response(m) for m in modules]


@router.get("/{module_id}", response_model=ModuleResponse)
def get_module(module_id: int, db: Session = Depends(get_db)):
    service = ModuleService(db)
    module = service.get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Модуль не найден")
    return _module_to_response(module)


@router.post("/", response_model=ModuleResponse, status_code=201)
def create_module(data: ModuleCreate, db: Session = Depends(get_db)):
    service = ModuleService(db)
    try:
        module = service.create_module(
            title=data.title,
            description=data.description,
            tasks=[t.model_dump() for t in data.tasks],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _module_to_response(module)


@router.put("/{module_id}", response_model=ModuleResponse)
def update_module(module_id: int, data: ModuleCreate, db: Session = Depends(get_db)):
    service = ModuleService(db)
    try:
        module = service.update_module(
            module_id=module_id,
            title=data.title,
            description=data.description,
            tasks=[t.model_dump() for t in data.tasks],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return _module_to_response(module)


@router.delete("/{module_id}", status_code=204)
def delete_module(module_id: int, delete_tasks: bool = Query(default=False), db: Session = Depends(get_db)):
    service = ModuleService(db)
    try:
        service.delete_module(module_id, delete_tasks=delete_tasks)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))