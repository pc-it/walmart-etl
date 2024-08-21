from typing import List, Dict, Union
from abc import abstractmethod, ABC


class AbstractExtractor(ABC):

    def __repr__(self):
        return self.__class__.__name__

    @abstractmethod
    def extract(self, *args, **kwargs) -> Union[Dict, List[Dict]]:
        pass
