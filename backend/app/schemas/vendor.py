from typing import Optional
from pydantic import BaseModel


class VendorBase(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    trade: Optional[str] = None
    nda_signed: bool = False
    orientation_complete: bool = False
    badge_issued: bool = False
    site_access_approved: bool = False
    notes: Optional[str] = None


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    trade: Optional[str] = None
    nda_signed: Optional[bool] = None
    orientation_complete: Optional[bool] = None
    badge_issued: Optional[bool] = None
    site_access_approved: Optional[bool] = None
    notes: Optional[str] = None


class VendorResponse(VendorBase):
    id: int
    onboarding_status: str  # derived label added by router

    model_config = {"from_attributes": True}
