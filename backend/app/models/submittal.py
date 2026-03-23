from sqlalchemy import Column, Integer, String, Text, Date
from app.database import Base


class Submittal(Base):
    __tablename__ = "submittals"

    id = Column(Integer, primary_key=True, index=True)
    submittal_number = Column(String(20), unique=True, nullable=False, index=True)
    spec_section = Column(String(50), nullable=True)
    description = Column(String(255), nullable=False)
    assigned_gc = Column(String(100), nullable=True)
    reviewer = Column(String(100), nullable=True)
    submitted_date = Column(Date, nullable=True)
    response_due = Column(Date, nullable=True)
    returned_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=False, default="Pending")    # Pending | Approved | Rejected | Revise & Resubmit
    revision = Column(Integer, nullable=False, default=1)
    notes = Column(Text, nullable=True)
