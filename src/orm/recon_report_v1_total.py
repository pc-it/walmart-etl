from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Text, Date, Float

from .base import Base


class WalmartReconReportV1TotalORM(Base):
    __tablename__ = 'recon_report_v1_total'
    __table_args__ = {'schema': 'api'}

    id = Column(Integer, primary_key=True)
    record_created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    report_date = Column(Date)
    period_start_date = Column(Date, index=True)
    period_end_date = Column(Date, index=True)
    total_payable = Column(Float)
    currency = Column(Text)
    transaction_posted_timestamp = Column(Date, index=True)
    transaction_type = Column(Text)
    transaction_description = Column(Text)
    amount = Column(Float)
    amount_type = Column(Text)
    campaign_id = Column(Text)
    customer_promo_type = Column(Text)
