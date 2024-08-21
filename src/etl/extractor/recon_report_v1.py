from datetime import datetime
from typing import Dict, List

from .abstract import AbstractExtractor
from src.api.walmart.reports import WalmartReportAPI


class WalmartReconReportJsonV1Extractor(AbstractExtractor):

    def __init__(self, api: WalmartReportAPI):
        self.api = api

    def available_dates(self):
        params = {
            'reportVersion': 'v1'
        }
        response = self.api.available_recon_report_dates(params=params)
        dates = response.json()['availableApReportDates']
        dates = [datetime.strptime(each, '%m%d%Y') for each in dates]
        return sorted(dates)

    def extract(self, report_date, *args, **kwargs) -> List[Dict]:
        params = {
            'reportDate': report_date,
            'offset': 0,
            'noOfRecords': 1000
        }
        result = []
        for page in self.api.recon_report_json(params=params):
            page_data = page.json()
            report_data = page_data.get('reportData')
            if report_data is None:
                print(page_data)
                raise ValueError
            result.extend(page.json()['reportData'])
        return result
