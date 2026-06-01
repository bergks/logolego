from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.card import CardCreate, CardResponse
from app.services.card_service import CardService

router = APIRouter(prefix="/cards", tags=["cards"])


def _card_to_response(service, card):
    content = service.get_content(card)
    return {
        "id": card.id,
        "type_id": card.type_id,
        "content": content.__dict__ if content else None,
        "used_in_tasks": service.is_used_in_tasks(card.id),
    }


@router.get("/", response_model=list[CardResponse])
def list_cards(type_id: int | None = None, db: Session = Depends(get_db)):
    service = CardService(db)
    cards = service.get_cards_by_type(type_id) if type_id else service.get_all_cards()
    return [_card_to_response(service, card) for card in cards]


@router.get("/{card_id}", response_model=CardResponse)
def get_card(card_id: int, db: Session = Depends(get_db)):
    service = CardService(db)
    card_and_content = service.get_card_with_content(card_id)
    if not card_and_content:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    card, _ = card_and_content
    return _card_to_response(service, card)


@router.post("/", response_model=CardResponse, status_code=201)
def create_card(data: CardCreate, db: Session = Depends(get_db)):
    service = CardService(db)
    try:
        card = service.create_card(data.type_id, data.content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _card_to_response(service, card)


@router.put("/{card_id}", response_model=CardResponse)
def update_card(card_id: int, data: CardCreate, db: Session = Depends(get_db)):
    service = CardService(db)
    try:
        card = service.update_card(card_id, data.content)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return _card_to_response(service, card)


@router.delete("/{card_id}", status_code=204)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    service = CardService(db)
    try:
        service.delete_card(card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))