import time
from loguru import logger
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
        recon_report = self.api.recon_report_json
        recon_report_generator = recon_report(params=params)
        retry = None
        try_count = 0

        while True:
            page = recon_report_generator.send(retry)

            page_data = page.json()
            report_data = page_data.get('reportData')

            if report_data is None:

                if try_count > 5:
                    logger.warning('Too many retries. Stop.')
                    raise OSError('Too many retries')

                logger.warning(f'{self} - Issue with request {page_data}. Sleep and try again.')

                try_count += 1
                time.sleep(10)
                retry = True
                continue

            result.extend(report_data)

            if recon_report.last_page:
                break

        return result
