import json
import peewee_async
from database.models import GameObject
from database import db_manager
from .base import BaseAdapter
from .mixins import MovableMixin, RotatableMixin, CreatableMixin

__all__ = [
    'BaseDbAdapter',
    'CreatableDbAdapter',
    'MovableDbAdapter',
    'RotatableDbAdapter',
]


class BaseDbAdapter(BaseAdapter):
    db_client: peewee_async.Manager = db_manager

    def __init__(self, db_object: GameObject):
        self.obj: dict = json.loads(db_object.params)
        self.db_obj = db_object

    @classmethod
    async def _get_object(cls, param: str):
        return await cls.db_client.get(GameObject, name=param)

    async def save(self):
        self.db_obj.params = json.dumps(self.obj)
        await self.db_client.update(self.db_obj)

    @classmethod
    async def create(cls, param: str) -> 'BaseAdapter':
        return cls(await cls._get_object(param))


class CreatableDbAdapter(BaseDbAdapter, CreatableMixin):

    @classmethod
    async def _get_object(cls, param: str):
        return await cls.db_client.get_or_create(GameObject, name=param)


class MovableDbAdapter(BaseDbAdapter, MovableMixin):
    pass


class RotatableDbAdapter(BaseDbAdapter, RotatableMixin):
    pass
