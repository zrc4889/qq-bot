from re import I, sub
from typing import Union

from avilla.core import Avilla
from avilla.core.builtins.profile import MemberProfile
from avilla.core.event.message import MessageEvent
from avilla.core.execution.message import MessageSend
from avilla.core.message.chain import MessageChain
from avilla.core.network.clients.aiohttp import AiohttpWebsocketClient
from avilla.onebot.config import OnebotConfig, WebsocketCommunication
from avilla.onebot.protocol import OnebotProtocol
from avilla.core.provider import FileProvider
from avilla.core.relationship import Relationship
from avilla.core.builtins.elements import Image, Text, Notice
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema
import subprocess

saya = Saya.current()
channel = Channel.current()
channel.name(__name__)


class Minecraft:
    open_status = False

    async def open_server(self):
        if self.open_status:
            return
        self.open_status = True
        print("开启服务器")
        subprocess.run(["tmux", "send", "-t", "minecraft", "./start.sh", "ENTER"])

    async def close_server(self):
        if not self.open_status:
            return
        self.open_status = False
        subprocess.run(["tmux", "send", "-t", "minecraft", "stop", "ENTER"])

    async def judge(self, message: str):
        if message == "open":
            await self.open_server()
            return "已开启"
        if message == "close":
            await self.close_server()
            return "已关闭"
        if message == "status":
            return "当前服务器开启状态为：" + str(self.open_status)


minecraft = Minecraft()


@channel.use(ListenerSchema(listening_events=[MessageEvent]))
async def event_receiver(message: MessageChain, rs: Relationship):
    if message.as_display().startswith("#mc "):
        await rs.exec(
            MessageSend(
                MessageChain.create(
                    [
                        Notice(target=rs.ctx.id),
                        Text(await minecraft.judge(message.as_display()[4:])),
                    ]
                )
            )
        )
