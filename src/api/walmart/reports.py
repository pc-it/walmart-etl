from typing import Dict

from .base import WalmartBaseAPI


class WalmartReportAPI(WalmartBaseAPI):

    @WalmartBaseAPI.Decorator.recon_report_json_v1_pagination
    def recon_report_json(self, params: Dict):
        endpoint = '/v3/report/reconreport/reconFileJson'
        return self.make_request(method='GET', endpoint=endpoint, params=params)

    def recon_report(self, params: Dict):
        headers = {
            'Accept': 'application/octet-stream'
        }
        endpoint = '/v3/report/reconreport/reconFile'
        return self.make_request(method='GET', endpoint=endpoint, params=params, headers=headers)

    def available_recon_report_dates(self, params: Dict):
        endpoint = '/v3/report/reconreport/availableReconFiles'
        return self.make_request(method='GET', endpoint=endpoint, params=params)
