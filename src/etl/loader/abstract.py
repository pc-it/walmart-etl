from abc import ABC, abstractmethod


class AbstractLoader(ABC):

    def __init__(self, orm_model):
        self.orm_model = orm_model

    def __repr__(self):
        return self.__class__.__name__

    @abstractmethod
    def load(self, *args, **kwargs) -> bool:
        pass
