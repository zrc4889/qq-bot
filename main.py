import asyncio
import os
<<<<<<< HEAD
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour

import asyncio
import logging
from aiohttp.client import ClientSession
from graia.broadcast import Broadcast
from yarl import URL
from avilla.core import Avilla
from avilla.core.network.clients.aiohttp import AiohttpWebsocketClient
from avilla.onebot.config import OnebotConfig, WebsocketCommunication
from avilla.onebot.protocol import OnebotProtocol

loop = asyncio.get_event_loop()
broadcast = Broadcast(loop=loop)
session = ClientSession(loop=loop)

saya = Saya(broadcast)
avilla = Avilla(
    broadcast,
    OnebotProtocol,
    {"ws": AiohttpWebsocketClient(session)},
    {
        OnebotProtocol: OnebotConfig(
            bot_id=2324523071,
            communications={
                "ws": WebsocketCommunication(api_root=URL("ws://127.0.0.1:6700/"))
            },
        )
    },
)

logging.basicConfig(
    format="[%(asctime)s][%(levelname)s]: %(message)s",
    level=logging.INFO,
)

saya.install_behaviours(BroadcastBehaviour(broadcast))


with saya.module_context():
    saya.require("modules.twenty-translations")
    saya.require("modules.CloudMusic")


# @broadcast.receiver("ExampleEvent")
# async def do_something():
#     pass


loop.run_until_complete(avilla.launch())
loop.run_forever()
=======

from graia.application import GraiaMiraiApplication, Session
from graia.broadcast import Broadcast
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour

from utils import LoguruLogger, Config

loop = asyncio.get_event_loop()
broadcast = Broadcast(loop=loop)
saya = Saya(broadcast)  # 这里可以置空, 但是会丢失 Lifecycle 特性
config = Config()
miraiConf = config.get('miraiConf')
botConf = config.get('botConf')

saya.install_behaviours(BroadcastBehaviour(broadcast))
app = GraiaMiraiApplication(
    broadcast=broadcast,
    connect_info=Session(
        host=miraiConf['miraiHost'],  # 填入 httpapi 服务运行的地址
        authKey=miraiConf['miraiAuthKey'],  # 填入 authKey
        account=botConf['BotQQ'],  # 你的机器人的 qq 号
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

try:
    app.launch_blocking()
except KeyboardInterrupt:
    config.save()
    exit()
>>>>>>> origin/master
