import abc
import typing

from typing import Type, Dict
from pydantic import ValidationError
from google.protobuf.reflection import GeneratedProtocolMessageType

from rpc.proto import tanks_pb2
from conf import settings, Settings
from gateway import request_objects
from gateway.commands import COMMANDS, BaseCommand, UObj
from adapters.factory import AbstractAdapterFactory, BaseFactory


class ServerMethod(abc.ABC):
    """Base class for abstracting server-side logic.
    The main method is "process", it must be called to process the request.
    To describe the new server method, you need to create a sub class and
    implement method "_execute" in it,
    which contains the logic for processing the request.

    Attributes:
    request_obj_cls: request object class(BaseRequestObject sub class ) for
    this server method.
    response_msg_cls: class of the message that this server method
    should return.
    """
    request_obj_cls: request_objects.BaseRequestObject
    response_msg_cls: GeneratedProtocolMessageType

    @classmethod
    def _get_response_msg(cls):
        response = cls.response_msg_cls()
        response.header.status = tanks_pb2.ERROR
        return response

    @classmethod
    def _get_req_object(cls, request):
        return cls.request_obj_cls.parse_obj(request)

    @classmethod
    async def process(cls, request):
        """
        The main method, which is called to process the request by the server.
        Must return an object of the message class that is defined individually
        for each method using
        response_msg_cls attribute.
        """
        response = cls._get_response_msg()

        try:
            return await cls._execute(cls._get_req_object(request), response)
        except Exception as exc:
            if isinstance(exc, ValidationError):
                response.header.status = tanks_pb2.INVALID_REQUEST
            response.header.description = str(exc)
        return response

    @classmethod
    def _get_response_msg(cls):
        return cls.response_msg_cls()

    @classmethod
    async def _execute(cls, request_obj, response_msg):
        """Contains the individual logic for processing a request specific to
        the server method.
        Must return a message class object (response_msg_cls instance) with a
        filled status.
        :param request_obj - request_obj_cls instance with request data.
        :param response_msg - response_msg_cls instance.
        :return response_msg_cls instance.
        """
        raise NotImplementedError


class HeathzMethod(ServerMethod):
    request_obj_cls = request_objects.HealthzRObject
    response_msg_cls = tanks_pb2.HealthzResponse

    @classmethod
    async def _execute(
            cls,
            request_obj: request_objects.HealthzRObject,
            response_msg: tanks_pb2.HealthzResponse,
    ) -> tanks_pb2.HealthzResponse:
        response_msg.header.status = tanks_pb2.SUCCESS
        return response_msg


class BaseGameMethod(ServerMethod):

    response_msg_cls = tanks_pb2.GameResp

    _commands: Dict[str, Type[BaseCommand]] = COMMANDS
    _settings: Settings = settings

    @classmethod
    def _get_factory(cls):
        return AbstractAdapterFactory.get_adapter_factory(cls._settings)

    @staticmethod
    async def _run_command(cmd: Type[BaseCommand], obj: UObj):
        await cmd(obj).execute()

    @classmethod
    async def _run_commands(
            cls,
            factory: BaseFactory,
            commands: typing.List[str],
            param: str
    ):
        for cmd in commands:
            adapter = factory.get_adapter(cmd)
            await cls._run_command(
                cls._commands[cmd], await adapter.create(param)
            )

    @classmethod
    async def _execute(
            cls,
            request_obj: request_objects.BaseGameRequest,
            response_msg: tanks_pb2.GameResp
    ) -> tanks_pb2.GameResp:

        await cls._run_commands(
            cls._get_factory(), request_obj.get_commands(), request_obj.username
        )
        response_msg.header.status = tanks_pb2.SUCCESS
        return response_msg


class StartGameMethod(BaseGameMethod):

    request_obj_cls = request_objects.StartGameRObject


class RunCommandsMethod(BaseGameMethod):

    request_obj_cls = request_objects.RunCommandsRObject
