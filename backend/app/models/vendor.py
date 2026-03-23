from sqlalchemy import Column, Integer, String, Text, Boolean
from app.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(150), nullable=False)
    contact_name = Column(String(100), nullable=True)
    contact_email = Column(String(150), nullable=True)
    trade = Column(String(100), nullable=True)
    nda_signed = Column(Boolean, nullable=False, default=False)
    orientation_complete = Column(Boolean, nullable=False, default=False)
    badge_issued = Column(Boolean, nullable=False, default=False)
    site_access_approved = Column(Boolean, nullable=False, default=False)
    # onboarding_status is derived — not stored; computed in the router
    notes = Column(Text, nullable=True)
