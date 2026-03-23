from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel


class RAGStatus(str, Enum):
    green = "Green"
    amber = "Amber"
    red = "Red"


class OFMBase(BaseModel):
    equipment_tag: str
    description: str
    supplier: Optional[str] = None
    expected_delivery: Optional[date] = None
    actual_delivery: Optional[date] = None
    rag_status: RAGStatus = RAGStatus.green
    notes: Optional[str] = None


class OFMCreate(OFMBase):
    pass


class OFMUpdate(BaseModel):
    equipment_tag: Optional[str] = None
    description: Optional[str] = None
    supplier: Optional[str] = None
    expected_delivery: Optional[date] = None
    actual_delivery: Optional[date] = None
    rag_status: Optional[RAGStatus] = None
    notes: Optional[str] = None


class OFMResponse(OFMBase):
    id: int
    variance_days: Optional[int] = None

    model_config = {"from_attributes": True}
