from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.submittal import Submittal
from app.schemas.submittal import SubmittalCreate, SubmittalUpdate, SubmittalResponse

router = APIRouter(prefix="/api/submittals", tags=["submittals"])


def _next_sub_number(db: Session) -> str:
    count = db.query(Submittal).count()
    return f"SUB-{count + 1:03d}"


@router.get("", response_model=list[SubmittalResponse])
def list_submittals(
    status: Optional[str] = Query(None),
    assigned_gc: Optional[str] = Query(None),
    sort_by: str = Query("submitted_date"),
    sort_dir: str = Query("desc"),
    db: Session = Depends(get_db),
):
    q = db.query(Submittal)
    if status:
        q = q.filter(Submittal.status == status)
    if assigned_gc:
        q = q.filter(Submittal.assigned_gc == assigned_gc)
    col = getattr(Submittal, sort_by, Submittal.submitted_date)
    q = q.order_by(col.desc() if sort_dir == "desc" else col.asc())
    return q.all()


@router.post("", response_model=SubmittalResponse, status_code=201)
def create_submittal(payload: SubmittalCreate, db: Session = Depends(get_db)):
    sub = Submittal(**payload.model_dump(), submittal_number=_next_sub_number(db))
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


@router.patch("/{sub_id}", response_model=SubmittalResponse)
def update_submittal(sub_id: int, payload: SubmittalUpdate, db: Session = Depends(get_db)):
    sub = db.get(Submittal, sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Submittal not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(sub, field, value)
    db.commit()
    db.refresh(sub)
    return sub


@router.delete("/{sub_id}", status_code=204)
def delete_submittal(sub_id: int, db: Session = Depends(get_db)):
    sub = db.get(Submittal, sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Submittal not found")
    db.delete(sub)
    db.commit()
