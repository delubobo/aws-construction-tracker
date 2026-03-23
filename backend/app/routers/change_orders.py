from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.change_order import ChangeOrder
from app.schemas.change_order import ChangeOrderCreate, ChangeOrderUpdate, ChangeOrderResponse

router = APIRouter(prefix="/api/change-orders", tags=["change_orders"])


def _next_co_number(db: Session) -> str:
    count = db.query(ChangeOrder).count()
    return f"CO-{count + 1:03d}"


@router.get("", response_model=list[ChangeOrderResponse])
def list_change_orders(
    status: Optional[str] = Query(None),
    assigned_gc: Optional[str] = Query(None),
    sort_by: str = Query("submitted_date"),
    sort_dir: str = Query("desc"),
    db: Session = Depends(get_db),
):
    q = db.query(ChangeOrder)
    if status:
        q = q.filter(ChangeOrder.status == status)
    if assigned_gc:
        q = q.filter(ChangeOrder.assigned_gc == assigned_gc)
    col = getattr(ChangeOrder, sort_by, ChangeOrder.submitted_date)
    q = q.order_by(col.desc() if sort_dir == "desc" else col.asc())
    return q.all()


@router.post("", response_model=ChangeOrderResponse, status_code=201)
def create_change_order(payload: ChangeOrderCreate, db: Session = Depends(get_db)):
    co = ChangeOrder(**payload.model_dump(), co_number=_next_co_number(db))
    db.add(co)
    db.commit()
    db.refresh(co)
    return co


@router.patch("/{co_id}", response_model=ChangeOrderResponse)
def update_change_order(co_id: int, payload: ChangeOrderUpdate, db: Session = Depends(get_db)):
    co = db.get(ChangeOrder, co_id)
    if not co:
        raise HTTPException(status_code=404, detail="Change order not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(co, field, value)
    db.commit()
    db.refresh(co)
    return co


@router.delete("/{co_id}", status_code=204)
def delete_change_order(co_id: int, db: Session = Depends(get_db)):
    co = db.get(ChangeOrder, co_id)
    if not co:
        raise HTTPException(status_code=404, detail="Change order not found")
    db.delete(co)
    db.commit()
