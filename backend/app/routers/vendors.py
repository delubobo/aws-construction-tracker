from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate, VendorResponse

router = APIRouter(prefix="/api/vendors", tags=["vendors"])


def _derive_status(v: Vendor) -> str:
    steps = [v.nda_signed, v.orientation_complete, v.badge_issued, v.site_access_approved]
    completed = sum(steps)
    if completed == 4:
        return "Fully Onboarded"
    if v.nda_signed is False:
        return "NDA Outstanding"
    if v.orientation_complete is False:
        return "Orientation Pending"
    if v.badge_issued is False:
        return "Badge Pending"
    return "Site Access Pending"


def _to_response(v: Vendor) -> dict:
    d = {c.name: getattr(v, c.name) for c in v.__table__.columns}
    d["onboarding_status"] = _derive_status(v)
    return d


@router.get("", response_model=list[VendorResponse])
def list_vendors(
    trade: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(Vendor)
    if trade:
        q = q.filter(Vendor.trade == trade)
    return [_to_response(v) for v in q.all()]


@router.post("", response_model=VendorResponse, status_code=201)
def create_vendor(payload: VendorCreate, db: Session = Depends(get_db)):
    v = Vendor(**payload.model_dump())
    db.add(v)
    db.commit()
    db.refresh(v)
    return _to_response(v)


@router.patch("/{vendor_id}", response_model=VendorResponse)
def update_vendor(vendor_id: int, payload: VendorUpdate, db: Session = Depends(get_db)):
    v = db.get(Vendor, vendor_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vendor not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(v, field, value)
    db.commit()
    db.refresh(v)
    return _to_response(v)


@router.delete("/{vendor_id}", status_code=204)
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    v = db.get(Vendor, vendor_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vendor not found")
    db.delete(v)
    db.commit()
