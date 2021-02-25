from typing import Type
from .db_adapters import *
from .file_adapters import *
from .base import BaseAdapter


from conf.base import Settings


class BaseFactory:
    _map: dict

    @classmethod
    def get_adapter(cls, command: str) -> Type[BaseAdapter]:
        return cls._map[command]


class DbAdapterFactory(BaseFactory):
    _map = {
        'MOVE': MovableDbAdapter,
        'ROTATE': RotatableDbAdapter,
        'START': CreatableDbAdapter,
    }


class FileAdapterFactory(BaseFactory):
    _map = {
        'MOVE': MovableFileAdapter,
        'ROTATE': RotatableFileAdapter,
        'START': CreatableFileAdapter,
    }


class AbstractAdapterFactory:
    _MAPPING = {
        'local': DbAdapterFactory,
        'database': FileAdapterFactory,
    }

    @classmethod
    def get_adapter_factory(cls, conf: Settings) -> Type[BaseFactory]:
        return cls._MAPPING[conf.MODE]
