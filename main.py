import sys
import time
from loguru import logger

from src.etl.recon_report_v1 import WalmartReconReportV1ETL, CONFIG

from pc_error_handler.catcher import ErrorCatcher
from pc_error_handler.handlers.slack import SlackHandler

from src.config.slack_config import slack_settings


handler = SlackHandler(slack_token=slack_settings.TOKEN, channel=slack_settings.CHANNEL)
ErrorCatcher(handler, name='`Walmart ETL`')

handler = {'sink': sys.stdout, 'level': 'INFO'}
logger.configure(handlers=[handler])


def main():
    etl = WalmartReconReportV1ETL(config=CONFIG)
    etl.run_available_dates(dates_limit=1)


if __name__ == '__main__':
    start = time.perf_counter()
    logger.info('Start script.')
    main()
    end = time.perf_counter()
    duration = end - start
    logger.info(f'Finish script. Duration: {duration}')
