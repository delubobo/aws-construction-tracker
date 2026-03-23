from typing import Any
from pydantic import BaseModel


class COByGC(BaseModel):
    gc: str
    value: float


class DashboardSummary(BaseModel):
    # RFIs
    open_rfis: int
    in_review_rfis: int
    overdue_rfis: int
    total_rfis: int
    # Submittals
    pending_submittals: int
    overdue_submittals: int
    # Change Orders
    pending_co_value: float
    total_co_value: float
    # OFM
    ofm_compliance_pct: float
    # Vendors
    fully_onboarded_vendors: int
    total_vendors: int
    # Chart data
    rfi_by_status: dict[str, int]
    co_by_gc: list[COByGC]
