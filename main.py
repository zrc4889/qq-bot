'''
Author: nullptr
Date: 2021-05-06 11:59:44
LastEditTime: 2021-05-31 21:36:39
'''
import asyncio
import os
from loguru import logger

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

saya.install_behaviours(BroadcastBehaviour(broadcast))
app = GraiaMiraiApplication(
    broadcast=broadcast,
    connect_info=Session(
        host=miraiConf['miraiHost'],  # 填入 httpapi 服务运行的地址
        authKey=miraiConf['miraiAuthKey'],  # 填入 authKey
        account=config.get('BotQQ'),  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    ),
    logger=LoguruLogger(config.get('logConf')),
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
except Exception as e:
    logger.error(e)
