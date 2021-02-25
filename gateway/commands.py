import abc
from base_models.base import UObj


class BaseCommand(abc.ABC):
    name: str

    def __init__(self, obj: UObj):
        self.obj = obj

    @abc.abstractmethod
    async def execute(self):
        raise NotImplementedError()


class Start(BaseCommand):
    name = 'START'

    async def execute(self):
        await self.obj.create_object()


class Move(BaseCommand):
    name = 'MOVE'

    async def execute(self):
        obj = self.obj
        await obj.set_position(
            await obj.get_velocity() + await obj.get_position()
        )


class Rotate(BaseCommand):
    name = 'ROTATE'

    async def execute(self):
        obj = self.obj
        await obj.set_direction(
            await obj.get_direction() + await obj.get_angular_velocity()
        )


COMMANDS = {cls.name: cls for cls in BaseCommand.__subclasses__()}
