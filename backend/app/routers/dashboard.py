from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy import func, case
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.rfi import RFI
from app.models.submittal import Submittal
from app.models.change_order import ChangeOrder
from app.models.ofm import OFMItem
from app.models.vendor import Vendor
from app.schemas.dashboard import DashboardSummary, COByGC

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardSummary)
def get_dashboard(db: Session = Depends(get_db)):
    today = date.today()

    # --- RFI aggregates ---
    rfi_rows = (
        db.query(RFI.status, func.count(RFI.id))
        .group_by(RFI.status)
        .all()
    )
    rfi_by_status = {status: count for status, count in rfi_rows}
    total_rfis = sum(rfi_by_status.values())
    open_rfis = rfi_by_status.get("Open", 0)
    in_review_rfis = rfi_by_status.get("In Review", 0)
    overdue_rfis = (
        db.query(func.count(RFI.id))
        .filter(RFI.status != "Closed", RFI.due_date < today)
        .scalar()
        or 0
    )

    # --- Submittal aggregates ---
    pending_submittals = (
        db.query(func.count(Submittal.id))
        .filter(Submittal.status == "Pending")
        .scalar()
        or 0
    )
    overdue_submittals = (
        db.query(func.count(Submittal.id))
        .filter(Submittal.status == "Pending", Submittal.response_due < today)
        .scalar()
        or 0
    )

    # --- Change order aggregates ---
    co_value_rows = (
        db.query(
            func.sum(case((ChangeOrder.status == "Pending Approval", ChangeOrder.cost_impact), else_=0)),
            func.sum(ChangeOrder.cost_impact),
        )
        .one()
    )
    pending_co_value = float(co_value_rows[0] or 0)
    total_co_value = float(co_value_rows[1] or 0)

    co_by_gc_rows = (
        db.query(ChangeOrder.assigned_gc, func.sum(ChangeOrder.cost_impact))
        .group_by(ChangeOrder.assigned_gc)
        .all()
    )
    co_by_gc = [COByGC(gc=gc or "Unknown", value=float(v or 0)) for gc, v in co_by_gc_rows]

    # --- OFM compliance ---
    total_ofm = db.query(func.count(OFMItem.id)).scalar() or 0
    green_ofm = (
        db.query(func.count(OFMItem.id)).filter(OFMItem.rag_status == "Green").scalar() or 0
    )
    ofm_compliance_pct = (green_ofm / total_ofm * 100) if total_ofm > 0 else 0.0

    # --- Vendor aggregates ---
    total_vendors = db.query(func.count(Vendor.id)).scalar() or 0
    fully_onboarded = (
        db.query(func.count(Vendor.id))
        .filter(
            Vendor.nda_signed == True,
            Vendor.orientation_complete == True,
            Vendor.badge_issued == True,
            Vendor.site_access_approved == True,
        )
        .scalar()
        or 0
    )

    return DashboardSummary(
        open_rfis=open_rfis,
        in_review_rfis=in_review_rfis,
        overdue_rfis=overdue_rfis,
        total_rfis=total_rfis,
        pending_submittals=pending_submittals,
        overdue_submittals=overdue_submittals,
        pending_co_value=pending_co_value,
        total_co_value=total_co_value,
        ofm_compliance_pct=round(ofm_compliance_pct, 1),
        fully_onboarded_vendors=fully_onboarded,
        total_vendors=total_vendors,
        rfi_by_status=rfi_by_status,
        co_by_gc=co_by_gc,
    )
