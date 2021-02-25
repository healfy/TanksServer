import abc
import typing
from google.protobuf.json_format import MessageToDict
from pydantic import BaseModel


class BaseRequestObject(BaseModel):

    @classmethod
    def parse_obj(cls, msg):
        data: dict = MessageToDict(msg, preserving_proto_field_name=True)
        return super().parse_obj(data)


class HealthzRObject(BaseRequestObject):
    pass


class BaseGameRequest(abc.ABC):
    username: str

    @abc.abstractmethod
    def get_commands(self):
        raise NotImplementedError()


class StartGameRObject(BaseGameRequest, BaseRequestObject):

    def get_commands(self) -> typing.List[str]:
        return ['START']


class CommandMessage(BaseModel):
    name: str


class RunCommandsRObject(BaseGameRequest, BaseRequestObject):
    commands: typing.List[CommandMessage]

    def get_commands(self) -> typing.List[str]:
        return [c.name.upper() for cmd in self.commands for c in cmd]
