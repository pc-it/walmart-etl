from typing import Dict
from datetime import datetime

from src.etl.extractor.abstract import AbstractExtractor
from src.etl.transformer.abstract import AbstractTransformer
from src.etl.loader.abstract import AbstractLoader


class BaseETL:

    def __init__(self, config: Dict):
        self.extractor: AbstractExtractor = self.__build_instance(**config.get('extractor'))
        self.transformer: AbstractTransformer = self.__build_instance(**config.get('transformer'))
        self.loader: AbstractLoader = self.__build_instance(**config.get('loader'))

    def __repr__(self):
        return self.__class__.__name__

    @staticmethod
    def __build_instance(_class, params=None):
        if params is not None:
            return _class(**params)
        else:
            return _class()

    def extract(self, *args, **kwargs):
        return self.extractor.extract()

    def transform(self, *args, **kwargs):
        return self.transformer.transform(data=kwargs['data'])

    def load(self, *args, **kwargs):
        self.loader.load(data_to_insert=kwargs['data_to_insert'])
        return True
