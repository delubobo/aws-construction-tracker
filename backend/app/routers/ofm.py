from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ofm import OFMItem
from app.schemas.ofm import OFMCreate, OFMUpdate, OFMResponse

router = APIRouter(prefix="/api/ofm", tags=["ofm"])


def _compute_variance(item: OFMItem) -> None:
    """Compute variance_days in place: positive = late."""
    if item.actual_delivery and item.expected_delivery:
        item.variance_days = (item.actual_delivery - item.expected_delivery).days
    else:
        item.variance_days = None


@router.get("", response_model=list[OFMResponse])
def list_ofm(
    rag_status: Optional[str] = Query(None),
    sort_by: str = Query("expected_delivery"),
    sort_dir: str = Query("asc"),
    db: Session = Depends(get_db),
):
    q = db.query(OFMItem)
    if rag_status:
        q = q.filter(OFMItem.rag_status == rag_status)
    col = getattr(OFMItem, sort_by, OFMItem.expected_delivery)
    q = q.order_by(col.desc() if sort_dir == "desc" else col.asc())
    return q.all()


@router.post("", response_model=OFMResponse, status_code=201)
def create_ofm(payload: OFMCreate, db: Session = Depends(get_db)):
    item = OFMItem(**payload.model_dump())
    _compute_variance(item)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{item_id}", response_model=OFMResponse)
def update_ofm(item_id: int, payload: OFMUpdate, db: Session = Depends(get_db)):
    item = db.get(OFMItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="OFM item not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    _compute_variance(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204)
def delete_ofm(item_id: int, db: Session = Depends(get_db)):
    item = db.get(OFMItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="OFM item not found")
    db.delete(item)
    db.commit()
