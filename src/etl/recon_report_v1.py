import time

from loguru import logger
from datetime import datetime
from typing import List, Dict, Tuple

from src.etl.base import BaseETL

from src.api.walmart.reports import WalmartReportAPI
from src.etl.extractor.recon_report_v1 import WalmartReconReportJsonV1Extractor

from src.etl.transformer.recon_report_json_v1 import WalmartReconReportJsonV1Transformer

from src.etl.loader.sql import SqlLoader
from src.orm.recon_report_v1 import WalmartReconReportV1ORM
from src.orm.recon_report_v1_total import WalmartReconReportV1TotalORM

from src.config.walmart_config import walmart_settings

CONFIG = {
    'extractor': {
        '_class': WalmartReconReportJsonV1Extractor,
        'params': {
            'api': WalmartReportAPI(
                client_id=walmart_settings.WALMART_CLIENT_ID,
                client_secret=walmart_settings.WALMART_CLIENT_SECRET,
                consumer_channel_type=walmart_settings.WALMART_CONSUMER_CHANNEL_TYPE,
                qos_correlation_id=walmart_settings.WALMART_QOS_CORRELATION_ID
            )
        }
    },
    'transformer': {
        '_class': WalmartReconReportJsonV1Transformer,
        'params': {
            'schema': None,
        }
    },
    'loader': {
        '_class': SqlLoader,
        'params': {
            'orm_model': None
        }
    }
}


class WalmartReconReportV1ETL(BaseETL):

    def extract(self, report_date: datetime) -> List[Dict]:
        logger.info(f'{self} - Extract data for {report_date.date()} report date.')
        return self.extractor.extract(report_date=report_date.strftime('%m%d%Y'))

    def transform(self, data: List[Dict], report_date: datetime) -> Tuple[List[Dict], List[Dict]]:
        logger.info(f'{self} - Transform data.')
        return self.transformer.transform(data=data, report_date=report_date)

    def load(self, recon_report_data: List[Dict], recon_report_total_data: List[Dict], report_date: datetime):
        logger.info(f'{self} - Load regular data')
        filters_to_delete = (
            WalmartReconReportV1ORM.report_date == report_date,
        )
        self.loader.load(data_to_insert=recon_report_data, orm_model=WalmartReconReportV1ORM, filters_to_delete=filters_to_delete)

        logger.info(f'{self} - Load Total data')
        filters_to_delete = (
            WalmartReconReportV1TotalORM.report_date == report_date,
        )
        self.loader.load(data_to_insert=recon_report_total_data, orm_model=WalmartReconReportV1TotalORM, filters_to_delete=filters_to_delete)

    def run(self, report_date: datetime):
        data = self.extract(report_date=report_date)
        recon_report_data, recon_report_total_data = self.transform(data=data, report_date=report_date)
        self.load(recon_report_data=recon_report_data, recon_report_total_data=recon_report_total_data, report_date=report_date)

    def run_available_dates(self, dates_limit=200):
        dates = self.extractor.available_dates()
        dates = dates[-dates_limit:]
        dates = [each for each in dates if each >= datetime(year=2023, month=3, day=28)]
        for _date in dates:
            self.run(report_date=_date)
            time.sleep(5)
