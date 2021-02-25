import json
import os
from .base import BaseAdapter
from .mixins import RotatableMixin, MovableMixin, CreatableMixin


__all__ = [
    'BaseFileAdapter',
    'CreatableFileAdapter',
    'MovableFileAdapter',
    'RotatableFileAdapter',
]


class BaseFileAdapter(BaseAdapter):
    FOLDER = '/tmp/tanks/'

    def __init__(self, path: str, obj: dict):
        self.path = path
        self.obj: dict = obj

    @classmethod
    async def _get_object(cls, param: str):
        with open(param, 'r') as f:
            return json.load(f)

    async def save(self):
        with open(f'{self.path}', 'w+') as f:
            f.write(json.dumps(self.obj))

    @classmethod
    async def create(cls, param: str) -> 'BaseAdapter':
        path = f'{cls.FOLDER}{param}.json'
        return cls(path, await cls._get_object(path))


class CreatableFileAdapter(BaseFileAdapter, CreatableMixin):

    @classmethod
    async def _get_object(cls, param: str):
        os.makedirs(cls.FOLDER)
        with open(param, 'w+') as _:
            pass
        return {}


class MovableFileAdapter(BaseFileAdapter, MovableMixin):
    pass


class RotatableFileAdapter(BaseFileAdapter, RotatableMixin):
    pass

