from typing import Optional
from datetime import datetime, date
from pydantic import Field, field_validator

from src.schema.base import BaseModel


class WalmartReconReportV1TotalsSchema(BaseModel):
    period_start_date: Optional[date] = Field(alias='Period Start Date', default=None)
    period_end_date: Optional[date] = Field(alias='Period End Date', default=None)
    total_payable: Optional[float] = Field(alias='Total Payable', default=None)
    currency: Optional[str] = Field(alias='Currency', default=None)
    transaction_posted_timestamp: Optional[date] = Field(alias='Transaction Posted Timestamp', default=None)
    transaction_type: Optional[str] = Field(alias='Transaction Type', default=None)
    transaction_description: Optional[str] = Field(alias='Transaction Description', default=None)
    amount: Optional[float] = Field(alias='Amount', default=None)
    amount_type: Optional[str] = Field(alias='Amount Type', default=None)
    campaign_id: Optional[str] = Field(alias='Campaign Id', default=None)
    customer_promo_type: Optional[str] = Field(alias='Customer Promo Type', default=None)

    @field_validator('period_start_date', 'period_end_date', 'transaction_posted_timestamp', mode='before')
    def str_to_date(cls, v):
        v = datetime.strptime(v, '%m/%d/%Y')
        return v


class WalmartReconReportV1Schema(BaseModel):
    period_start_date: Optional[str] = Field(alias='Period Start Date', default=None)
    transaction_key: Optional[str] = Field(alias='Transaction Key', default=None)
    transaction_posted_timestamp: Optional[date] = Field(alias='Transaction Posted Timestamp', default=None)
    transaction_type: Optional[str] = Field(alias='Transaction Type', default=None)
    transaction_description: Optional[str] = Field(alias='Transaction Description', default=None)
    customer_order_number: Optional[str] = Field(alias='Customer Order #', default=None)
    customer_order_line_number: Optional[int] = Field(alias='Customer Order line #', default=None)
    purchase_order_number: Optional[str] = Field(alias='Purchase Order #', default=None)
    purchase_order_line_number: Optional[str] = Field(alias='Purchase Order line #', default=None)
    amount: Optional[float] = Field(alias='Amount', default=None)
    amount_type: Optional[str] = Field(alias='Amount Type', default=None)
    ship_qty: Optional[int] = Field(alias='Ship Qty', default=None)
    commission_rate: Optional[float] = Field(alias='Commission Rate', default=None)
    transaction_reason_description: Optional[str] = Field(alias='Transaction Reason Description', default=None)
    partner_item_id: Optional[str] = Field(alias='Partner Item Id', default=None)
    partner_gtin: Optional[str] = Field(alias='Partner GTIN', default=None)
    partner_item_name: Optional[str] = Field(alias='Partner Item Name', default=None)
    product_tax_code: Optional[str] = Field(alias='Product Tax Code', default=None)
    ship_to_state: Optional[str] = Field(alias='Ship to State', default=None)
    ship_to_city: Optional[str] = Field(alias='Ship to City', default=None)
    ship_to_zipcode: Optional[str] = Field(alias='Ship to Zipcode', default=None)
    contract_category: Optional[str] = Field(alias='Contract Category', default=None)
    product_type: Optional[str] = Field(alias='Product Type', default=None)
    commission_rule: Optional[str] = Field(alias='Commission Rule', default=None)
    shipping_method: Optional[str] = Field(alias='Shipping Method', default=None)
    fulfillment_type: Optional[str] = Field(alias='Fulfillment Type', default=None)
    fulfillment_details: Optional[str] = Field(alias='Fulfillment Details', default=None)
    original_commission: Optional[float] = Field(alias='Original Commission', default=None)
    commission_incentive_program: Optional[str] = Field(alias='Commission Incentive Program', default=None)
    commission_saving: Optional[float] = Field(alias='Commission Saving', default=None)
    customer_promo_type: Optional[str] = Field(alias='Customer Promo Type', default=None)
    total_walmart_funded_savings_program: Optional[str] = Field(alias='Total Walmart Funded Savings Program', default=None)
    campaign_id: Optional[str] = Field(alias='Campaign Id', default=None)
    item_condition: Optional[str] = Field(alias='Item Condition', default=None)

    @field_validator('transaction_posted_timestamp', mode='before')
    def str_to_date(cls, v):
        v = datetime.strptime(v, '%m/%d/%Y')
        return v
