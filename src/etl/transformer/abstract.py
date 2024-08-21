from abc import ABC, abstractmethod
from typing import List, Dict, Union, Tuple


class AbstractTransformer(ABC):

    def __repr__(self):
        return self.__class__.__name__

    def __init__(self, schema):
        self.schema = schema

    @abstractmethod
    def transform(self, *args, **kwargs) -> Union[List[Dict], Tuple[List[Dict], List[Dict]]]:
        pass
