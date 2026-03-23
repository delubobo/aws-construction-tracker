from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel


class RFIStatus(str, Enum):
    open = "Open"
    in_review = "In Review"
    closed = "Closed"


class RFIPriority(str, Enum):
    high = "High"
    medium = "Medium"
    low = "Low"


class RFIBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: RFIStatus = RFIStatus.open
    priority: RFIPriority = RFIPriority.medium
    assigned_gc: Optional[str] = None
    submitted_by: Optional[str] = None
    submitted_date: Optional[date] = None
    due_date: Optional[date] = None
    closed_date: Optional[date] = None
    spec_section: Optional[str] = None
    notes: Optional[str] = None


class RFICreate(RFIBase):
    pass


class RFIUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[RFIStatus] = None
    priority: Optional[RFIPriority] = None
    assigned_gc: Optional[str] = None
    submitted_by: Optional[str] = None
    submitted_date: Optional[date] = None
    due_date: Optional[date] = None
    closed_date: Optional[date] = None
    spec_section: Optional[str] = None
    notes: Optional[str] = None


class RFIResponse(RFIBase):
    id: int
    rfi_number: str

    model_config = {"from_attributes": True}
