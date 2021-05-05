import asyncio
import os

from graia.application import GraiaMiraiApplication, Session
from graia.broadcast import Broadcast
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour
from utils import LoguruLogger

loop = asyncio.get_event_loop()
broadcast = Broadcast(loop=loop)
saya = Saya(broadcast)  # 这里可以置空, 但是会丢失 Lifecycle 特性

saya.install_behaviours(BroadcastBehaviour(broadcast))
app = GraiaMiraiApplication(
    broadcast=broadcast,
    connect_info=Session(
        host="http://172.23.96.1:8080",  # 填入 httpapi 服务运行的地址
        authKey="graia-mirai-api-http-authkey",  # 填入 authKey
        account=2324523071,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    ),
    logger=LoguruLogger(),
)

ignore = ["__init__.py", "__pycache__"]

with saya.module_context():
    for module in os.listdir("modules"):
        if module in ignore:
            continue
        try:
            if os.path.isdir(module):
                saya.require(f"modules.{module}")
            else:
                saya.require(f"modules.{module.split('.')[0]}")
        except ModuleNotFoundError:
            pass

app.launch_blocking()
try:
    loop.run_forever()
except KeyboardInterrupt:
    exit()
