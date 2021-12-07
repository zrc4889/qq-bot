from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema


from graia.ariadne.message.element import Plain
from graia.ariadne.model import Group, Member
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.element import Plain, At
import subprocess

saya = Saya.current()
channel = Channel.current()
channel.name(__name__)


class Minecraft:
    run_status = False
    player_list = []

    async def start_server(self):
        if self.run_status:
            return
        try:
            subprocess.run(["tmux", "send", "-t", "minecraft", "./start.sh", "ENTER"])
        finally:
            self.run_status = True

    async def stop_server(self):
        if not self.run_status:
            return
        try:
            subprocess.run(["tmux", "send", "-t", "minecraft", "stop", "ENTER"])
        finally:
            self.run_status = False

    async def judge(self, message: str):
        if message == "start":
            await self.start_server()
            return "已开启" if self.run_status else "启动失败"
        elif message == "stop":
            await self.stop_server()
            return "已关闭" if not self.run_status else "关闭失败"
        elif message == "status":
            return "当前服务器开启状态为：" + str(self.run_status)
        else:
            return "服务器暂时不支持这个命令"


minecraft = Minecraft()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def event_receiver(
    app: Ariadne, message: MessageChain, group: Group, sender: Member
):
    if message.asDisplay().startswith("#mc "):
        await app.sendMessage(
            group,
            MessageChain.create(
                [At(sender.id), Plain(await minecraft.judge(message.asDisplay()[4:]))]
            ),
        )
