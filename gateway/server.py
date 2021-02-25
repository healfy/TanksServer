from gateway import metod_classes
from rpc import TankServiceBase


class TankService(TankServiceBase):

    async def Healthz(self, stream) -> None:
        request = await stream.recv_message()
        await stream.send_message(
            await metod_classes.HeathzMethod.process(request)
        )

    async def RunCommands(self, stream) -> None:
        request = await stream.recv_message()
        await stream.send_message(
            await metod_classes.RunCommandsMethod.process(request)
        )

    async def StartGame(self, stream) -> None:
        request = await stream.recv_message()
        await stream.send_message(
            await metod_classes.StartGameMethod.process(request)
        )
