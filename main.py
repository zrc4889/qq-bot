import asyncio
import os
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


# with saya.module_context():
# saya.require("modules.twenty-translations")
# saya.require("modules.CloudMusic")


# @broadcast.receiver("ExampleEvent")
# async def do_something():
#     pass


loop.run_until_complete(avilla.launch())
loop.run_forever()
