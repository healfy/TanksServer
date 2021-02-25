import asyncio
from grpclib.server import Server
from gateway.server import TankService
from .utils import end_gracefully_tasks

from conf import settings


def serve():
    addr, port = settings.HOST, settings.PORT
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(None)
    server = Server([TankService()], loop=loop)
    loop.run_until_complete(server.start(addr, port))
    print(f"starting Tanks server {addr}:{port}")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Got signal SIGINT, "shutting down"')

    end_gracefully_tasks(loop)
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
