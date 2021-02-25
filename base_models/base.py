import abc
import numpy as np
from typing import Union


class AbstractCreatable(abc.ABC):

    @abc.abstractmethod
    async def create_object(self):
        raise NotImplementedError


class AbstractMovable(abc.ABC):

    @abc.abstractmethod
    async def get_velocity(self) -> np.ndarray:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_position(self) -> np.ndarray:
        raise NotImplementedError()

    @abc.abstractmethod
    async def set_position(self, pos: np.ndarray):
        raise NotImplementedError()


class AbstractRotatable(abc.ABC):

    @abc.abstractmethod
    async def get_direction(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def set_direction(self, value: int):
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_angular_velocity(self) -> int:
        raise NotImplementedError()


UObj = Union[AbstractRotatable, AbstractMovable, AbstractCreatable]
