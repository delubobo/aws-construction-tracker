from sqlalchemy import Column, Integer, String, Text, Date
from app.database import Base


class OFMItem(Base):
    __tablename__ = "ofm_items"

    id = Column(Integer, primary_key=True, index=True)
    equipment_tag = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=False)
    supplier = Column(String(100), nullable=True)
    expected_delivery = Column(Date, nullable=True)
    actual_delivery = Column(Date, nullable=True)
    variance_days = Column(Integer, nullable=True)                     # computed: actual - expected (positive = late)
    rag_status = Column(String(10), nullable=False, default="Green")  # Green | Amber | Red
    notes = Column(Text, nullable=True)
