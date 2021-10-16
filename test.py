import asyncio
import logging
from aiohttp.client import ClientSession
from graia.broadcast import Broadcast
from yarl import URL
from avilla import Avilla
from avilla.event.message import MessageEvent
from avilla.execution.message import MessageSend
from avilla.message.chain import MessageChain
from avilla.network.clients.aiohttp import AiohttpWebsocketClient
from avilla.onebot.config import OnebotConfig, WebsocketCommunication
from avilla.onebot.protocol import OnebotProtocol
from avilla.relationship import Relationship
from avilla.builtins.elements import PlainText

loop: asyncio.AbstractEventLoop
broadcast: Broadcast
session: ClientSession
avilla: Avilla


async def main():
    global loop, broadcast, session, avilla
    loop = asyncio.get_event_loop()
    broadcast = Broadcast(loop=loop)
    session = ClientSession(loop=loop)
    avilla = Avilla(
        broadcast,
        OnebotProtocol,
        {"ws": AiohttpWebsocketClient(session)},
        {
            OnebotProtocol: OnebotConfig(
                access_token="avilla-test",
                bot_id=208924405,
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

    loop.run_until_complete(avilla.launch())
    loop.run_forever()


asyncio.run(main())


@broadcast.receiver(MessageEvent)
async def event_receiver(rs: Relationship, message: MessageChain):
    print(message.as_display())
    await rs.exec(MessageSend([PlainText("Hello, World!")]))
