from sqlalchemy import Column, Integer, String, Text, Date
from app.database import Base


class RFI(Base):
    __tablename__ = "rfis"

    id = Column(Integer, primary_key=True, index=True)
    rfi_number = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="Open")       # Open | In Review | Closed
    priority = Column(String(20), nullable=False, default="Medium")   # High | Medium | Low
    assigned_gc = Column(String(100), nullable=True)
    submitted_by = Column(String(100), nullable=True)
    submitted_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    closed_date = Column(Date, nullable=True)
    spec_section = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
