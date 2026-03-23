from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel


class COStatus(str, Enum):
    pending_approval = "Pending Approval"
    approved = "Approved"
    rejected = "Rejected"
    on_hold = "On Hold"


class ChangeOrderBase(BaseModel):
    title: str
    scope: Optional[str] = None
    assigned_gc: Optional[str] = None
    cost_impact: float = 0.0
    schedule_impact: int = 0
    status: COStatus = COStatus.pending_approval
    submitted_date: Optional[date] = None
    approved_date: Optional[date] = None
    notes: Optional[str] = None


class ChangeOrderCreate(ChangeOrderBase):
    pass


class ChangeOrderUpdate(BaseModel):
    title: Optional[str] = None
    scope: Optional[str] = None
    assigned_gc: Optional[str] = None
    cost_impact: Optional[float] = None
    schedule_impact: Optional[int] = None
    status: Optional[COStatus] = None
    submitted_date: Optional[date] = None
    approved_date: Optional[date] = None
    notes: Optional[str] = None


class ChangeOrderResponse(ChangeOrderBase):
    id: int
    co_number: str

    model_config = {"from_attributes": True}
