import time
import pickle
import textwrap
import types
from pathlib import Path
from loguru import logger
from datetime import datetime
from typing import Dict, Generator
from functools import wraps, update_wrapper

import requests
from requests.auth import HTTPBasicAuth


BASE_DIR = Path(__file__).parent


class WalmartBaseAPI:
    host = 'https://marketplace.walmartapis.com'

    class Decorator:

        @classmethod
        def sign_request(cls, func):
            @wraps(func)
            def wrapper(obj, *args, **kwargs):
                logger.debug(f'{obj} - Sign request {args}, {kwargs}')
                headers = kwargs.pop('headers', {})
                signed_headers = {
                    'Accept': 'application/json',
                    'WM_SEC.ACCESS_TOKEN': obj.local_token,
                    'WM_CONSUMER.CHANNEL.TYPE': obj.consumer_channel_type,
                    'WM_SVC.NAME': 'Walmart Marketplace',
                    'WM_QOS.CORRELATION_ID': obj.qos_correlation_id,
                    **headers
                }
                response = func(obj, *args, **kwargs, headers=signed_headers, auth=HTTPBasicAuth(obj.client_id, obj.client_secret))
                return response
            return wrapper

        class recon_report_json_v1_pagination:

            def __init__(self, func):
                self._func = func
                self.page_count = 1
                self.last_page = False
                update_wrapper(self, func)

            def __get__(self, instance, owner):
                if instance is None:
                    return self
                return types.MethodType(self, instance)

            def __call__(self, obj, *args, **kwargs) -> Generator[(requests.Response, None, None)]:
                while True:
                    logger.debug(f'{obj.__class__.__name__}: request {self.page_count} page.')
                    response = self._func(obj, *args, **kwargs)
                    logger.debug(f'{obj.__class__.__name__}: received {self.page_count} page.')

                    next_offset = response.json().get('nextOffset', None)
                    self.last_page = next_offset is None or next_offset == -1

                    yield response

                    if self.last_page:
                        logger.debug(f'{obj.__class__.__name__} - Last page.')
                        break

                    kwargs['params']['offset'] = next_offset
                    self.page_count += 1
                return response

    def __repr__(self):
        return self.__class__.__name__

    def __init__(self, client_id: str, client_secret: str, consumer_channel_type: str, qos_correlation_id: str, token_file_name: str = 'access_token.pickle'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_file_name = token_file_name
        self.consumer_channel_type = consumer_channel_type
        self.qos_correlation_id = qos_correlation_id

    @staticmethod
    def request_response_data(response):
        format_headers = lambda d: '\n'.join(f'{k}: {v}' for k, v in d.items())
        # Remove Access Token value from headers to use in the message
        headers = response.request.headers
        result = textwrap.dedent('''
            ---------------- request ----------------
            {req.method} {req.url}
            {reqhdrs}

            {req.body}
            ---------------- response ----------------
            {res.status_code} {res.reason} {res.url}
            {reshdrs}

            {res.text}
        ''').format(
            req=response.request,
            res=response,
            reqhdrs=format_headers(headers),
            reshdrs=format_headers(response.headers),
        )
        return result

    def __save_token(self, response) -> Dict:
        """
        Method to save token to the local .pickle file

        :param response: response with token data that received via request_token method
        :return: token_data, dict
        """
        token_data = response.json()
        token_data.update({'timestamp': datetime.timestamp(datetime.now())})

        with open(BASE_DIR / self.token_file_name, 'wb') as f:
            pickle.dump(file=f, obj=token_data)

        logger.debug(f'{self}: Save token to the {self.token_file_name}')
        return token_data

    def __request_token(self):
        body = 'grant_type=client_credentials'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'WM_SVC.NAME': 'Walmart Marketplace',
            'WM_QOS.CORRELATION_ID': self.qos_correlation_id
        }
        return requests.request(method='POST', url=f'{self.host}/v3/token', data=body, headers=headers, auth=HTTPBasicAuth(self.client_id, self.client_secret))

    @property
    def local_token(self) -> str:
        """
        Method to load token from local pickle file

        # if file is missed or token is expired - call 2 methods
        # to request token via API and store in the local file

        :return: API token from local file
        """
        logger.debug(f'{self}: Load token from local {self.token_file_name}')
        if not Path(BASE_DIR / self.token_file_name).is_file():
            logger.debug(f'{self}: Local token missed.')
            self.__save_token(self.__request_token())

        with open(BASE_DIR / self.token_file_name, 'rb') as f:
            token_data = pickle.load(f)

        logger.debug(f'{self}: Check token lifetime.')

        if token_data['timestamp'] < time.time() - 60:
            logger.debug(f'{self}: Token has been expired.')
            token_data = self.__save_token(self.__request_token())
        else:
            logger.debug(f'{self}: Token is not expired.')

        logger.debug(f'{self}: Token has been loaded from {self.token_file_name}')
        return token_data['access_token']

    @Decorator.sign_request
    def make_request(self, *, method: str, endpoint: str, **kwargs):
        logger.info(f'{self} - Make request {method}, {endpoint}')
        return requests.request(url=f'{self.host}{endpoint}', method=method, **kwargs)
