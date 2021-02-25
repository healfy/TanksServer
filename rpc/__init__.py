import sys
import os

sys.path.extend((os.path.abspath('..'), os.path.abspath('../..'), os.path.abspath('.'),  os.path.abspath('rpc'),))

from proto.tanks_grpc import TankServiceBase

