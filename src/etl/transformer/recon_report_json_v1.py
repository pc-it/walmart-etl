from datetime import datetime
from typing import List, Dict, Tuple

from .abstract import AbstractTransformer
from src.schema.walmart.recon_report_v1 import WalmartReconReportV1Schema, WalmartReconReportV1TotalsSchema


class WalmartReconReportJsonV1Transformer(AbstractTransformer):

    def transform(self, data: List[Dict], report_date: datetime) -> Tuple[List[Dict], List[Dict]]:
        recon_report_data, recon_report_total_data = [], []
        for row in data:
            if 'Period End Date' in row:
                schema = WalmartReconReportV1TotalsSchema(**row)
                recon_report_total_data.append({**schema.model_dump(), 'report_date': report_date})
            else:
                schema = WalmartReconReportV1Schema(**row)
                recon_report_data.append({**schema.model_dump(), 'report_date': report_date})

        return recon_report_data, recon_report_total_data
