from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.rfi import RFI
from app.schemas.rfi import RFICreate, RFIUpdate, RFIResponse

router = APIRouter(prefix="/api/rfis", tags=["rfis"])


def _next_rfi_number(db: Session) -> str:
    count = db.query(RFI).count()
    return f"RFI-{count + 1:03d}"


@router.get("", response_model=list[RFIResponse])
def list_rfis(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    assigned_gc: Optional[str] = Query(None),
    sort_by: str = Query("submitted_date"),
    sort_dir: str = Query("desc"),
    db: Session = Depends(get_db),
):
    q = db.query(RFI)
    if status:
        q = q.filter(RFI.status == status)
    if priority:
        q = q.filter(RFI.priority == priority)
    if assigned_gc:
        q = q.filter(RFI.assigned_gc == assigned_gc)

    col = getattr(RFI, sort_by, RFI.submitted_date)
    q = q.order_by(col.desc() if sort_dir == "desc" else col.asc())
    return q.all()


@router.post("", response_model=RFIResponse, status_code=201)
def create_rfi(payload: RFICreate, db: Session = Depends(get_db)):
    rfi = RFI(**payload.model_dump(), rfi_number=_next_rfi_number(db))
    db.add(rfi)
    db.commit()
    db.refresh(rfi)
    return rfi


@router.patch("/{rfi_id}", response_model=RFIResponse)
def update_rfi(rfi_id: int, payload: RFIUpdate, db: Session = Depends(get_db)):
    rfi = db.get(RFI, rfi_id)
    if not rfi:
        raise HTTPException(status_code=404, detail="RFI not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(rfi, field, value)
    db.commit()
    db.refresh(rfi)
    return rfi


@router.delete("/{rfi_id}", status_code=204)
def delete_rfi(rfi_id: int, db: Session = Depends(get_db)):
    rfi = db.get(RFI, rfi_id)
    if not rfi:
        raise HTTPException(status_code=404, detail="RFI not found")
    db.delete(rfi)
    db.commit()
