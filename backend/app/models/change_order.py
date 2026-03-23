from sqlalchemy import Column, Integer, String, Text, Date, Float
from app.database import Base


class ChangeOrder(Base):
    __tablename__ = "change_orders"

    id = Column(Integer, primary_key=True, index=True)
    co_number = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    scope = Column(Text, nullable=True)
    assigned_gc = Column(String(100), nullable=True)
    cost_impact = Column(Float, nullable=False, default=0.0)          # USD
    schedule_impact = Column(Integer, nullable=False, default=0)      # days
    status = Column(String(50), nullable=False, default="Pending Approval")  # Pending Approval | Approved | Rejected | On Hold
    submitted_date = Column(Date, nullable=True)
    approved_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
