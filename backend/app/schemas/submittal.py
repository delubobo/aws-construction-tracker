from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel


class SubmittalStatus(str, Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
    revise_resubmit = "Revise & Resubmit"


class SubmittalBase(BaseModel):
    spec_section: Optional[str] = None
    description: str
    assigned_gc: Optional[str] = None
    reviewer: Optional[str] = None
    submitted_date: Optional[date] = None
    response_due: Optional[date] = None
    returned_date: Optional[date] = None
    status: SubmittalStatus = SubmittalStatus.pending
    revision: int = 1
    notes: Optional[str] = None


class SubmittalCreate(SubmittalBase):
    pass


class SubmittalUpdate(BaseModel):
    spec_section: Optional[str] = None
    description: Optional[str] = None
    assigned_gc: Optional[str] = None
    reviewer: Optional[str] = None
    submitted_date: Optional[date] = None
    response_due: Optional[date] = None
    returned_date: Optional[date] = None
    status: Optional[SubmittalStatus] = None
    revision: Optional[int] = None
    notes: Optional[str] = None


class SubmittalResponse(SubmittalBase):
    id: int
    submittal_number: str

    model_config = {"from_attributes": True}
