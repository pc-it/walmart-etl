from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Text, Date, Float

from .base import Base


class WalmartReconReportV1ORM(Base):
    __tablename__ = 'recon_report_v1'
    __table_args__ = {'schema': 'api'}

    id = Column(Integer, primary_key=True)
    record_created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    report_date = Column(Date)
    period_start_date = Column(Text)
    transaction_key = Column(Text)
    transaction_posted_timestamp = Column(Date, index=True)
    transaction_type = Column(Text)
    transaction_description = Column(Text)
    customer_order_number = Column(Text)
    customer_order_line_number = Column(Integer)
    purchase_order_number = Column(Text)
    purchase_order_line_number = Column(Text)
    amount = Column(Float)
    amount_type = Column(Text)
    ship_qty = Column(Integer)
    commission_rate = Column(Float)
    transaction_reason_description = Column(Text)
    partner_item_id = Column(Text)
    partner_gtin = Column(Text)
    partner_item_name = Column(Text)
    product_tax_code = Column(Text)
    ship_to_state = Column(Text)
    ship_to_city = Column(Text)
    ship_to_zipcode = Column(Text)
    contract_category = Column(Text)
    product_type = Column(Text)
    commission_rule = Column(Text)
    shipping_method = Column(Text)
    fulfillment_type = Column(Text)
    fulfillment_details = Column(Text)
    original_commission = Column(Float)
    commission_incentive_program = Column(Text)
    commission_saving = Column(Float)
    customer_promo_type = Column(Text)
    total_walmart_funded_savings_program = Column(Text)
    campaign_id = Column(Text)
    item_condition = Column(Text)
