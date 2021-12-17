from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from loguru import logger

from graia.ariadne.message.element import Plain
from graia.ariadne.model import Group, Member
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.element import Plain, At
import subprocess
import os

saya = Saya.current()
channel = Channel.current()
channel.name(__name__)


class Minecraft:
    run_status = False
    player_list = []
    save_list = []

    def __init__(self, config: dict = {"mc_dir": "/opt/minecraft/"}):
        save_list = os.listdir(config["mc_dir"])

    async def start_server(self):
        if self.run_status:
            return False
        try:
            subprocess.run(["tmux", "send", "-t", "minecraft", "./start.sh", "ENTER"])
        finally:
            self.run_status = True
            return True

    async def stop_server(self):
        if not self.run_status:
            return False
        try:
            subprocess.run(["tmux", "send", "-t", "minecraft", "stop", "ENTER"])
        finally:
            self.run_status = False
            return True

    async def save(self, operator: str) -> str:

        if operator == "list":
            result = "当前服务器有：\n"
            result = "\n".join(self.save_list)
            logger.debug(result)
            return result
        elif operator == "switch":
            if self.run_status:
                return "服务器正在运行！请先关闭服务器！"
            save = operator[6:]
            if save in self.save_list:
                try:
                    subprocess.run(
                        ["tmux", "send", "-t", "cd", "../{}".format(save), "ENTER"]
                    )
                except:
                    return "切换存档失败！"
                finally:
                    return "切换成功！"
        return "命令错误"

    async def judge(self, message: str) -> str:
        if message == "start":
            return "已开启" if await self.start_server() else "启动失败"
        elif message == "stop":
            await self.stop_server()
            return "已关闭" if await self.stop_server() else "关闭失败"
        elif message == "status":
            return "当前服务器开启状态为：" + str(self.run_status)
        elif message.startswith("saves "):
            return await self.save(message[6:])
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
                [
                    At(sender.id),
                    Plain(await minecraft.judge(message.asDisplay()[4:].strip())),
                ]
            ),
        )
