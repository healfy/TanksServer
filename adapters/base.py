import abc
from typing import Union
from base_models.base import UObj


class BaseAdapter(abc.ABC):

    @classmethod
    @abc.abstractmethod
    async def _get_object(cls, param: str):
        raise NotImplementedError()

    @abc.abstractmethod
    async def save(self):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    async def create(cls, param: str) -> Union['BaseAdapter', 'UObj']:
        raise NotImplementedError
