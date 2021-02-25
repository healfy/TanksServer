import numpy as np

from base_models import AbstractMovable, AbstractRotatable, AbstractCreatable


class BaseMixin:
    obj: dict
    save: callable


class CreatableMixin(AbstractCreatable, BaseMixin):

    async def create_object(self):
        self.obj['position'] = [0, 0, 0]
        self.obj['velocity'] = [0, 0, 0]
        self.obj['direction'] = 0
        self.obj['angular_velocity'] = 0
        await self.save()


class MovableMixin(AbstractMovable, BaseMixin):

    async def get_position(self) -> np.ndarray:
        return np.ndarray(self.obj['position'])

    async def get_velocity(self) -> np.ndarray:
        return np.ndarray(self.obj['velocity'])

    async def set_position(self, pos: np.ndarray):
        self.obj['position'] = pos.tolist()
        await self.save()


class RotatableMixin(AbstractRotatable, BaseMixin):

    async def get_direction(self) -> int:
        return self.obj['direction']

    async def set_direction(self, value: int):
        self.obj['direction'] = value
        await self.save()

    async def get_angular_velocity(self) -> int:
        return self.obj['angular_velocity']

