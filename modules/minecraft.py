from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema


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

class MinecraftCommand(Twilight):
    start = ArgumentMatch("--start", "-o", action="store_true")
    stop = ArgumentMatch("--stop", "-c", action="store_true")
    save = FullMatch("save")
    pass

class Minecraft:
    run_status = False
    player_list = []
    saves = []
	
	def __init__(self, **config = {mc_dir = "/opt/minecraft/"}):
		saves = os.lsdir(mc_dir)
	
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
            
    async def save(self, operator):
    	if operator == "list":
    		result = "当前服务器有：\n"
            result += '\n'.join(list)
            return result

    	elif operator == "switch":
    		pass
    	
    	

    async def judge(self, message: str) -> str`:
        if message == "start":
            return "已开启" if await self.start_server() else "启动失败"
        elif message == "stop":
            await self.stop_server()
            return "已关闭" if await self.stop_server() else "关闭失败"
        elif message == "status":
            return "当前服务器开启状态为：" + str(self.run_status)
        elif message.startwith("saves "):
        	return await self.swtich_save(message[6:])
        else:
            return "服务器暂时不支持这个命令"


minecraft = Minecraft()


@channel.use(ListenerSchema(listening_events=[MessageEvent], dispatchers=[
    Twilight(
        [FullMatch(".command")],
        {"arg": RegexMatch(r"\d+", optional=True)}
)]))
async def event_receiver(
    app: Ariadne, message: MessageChain, group: Group, sender: Member
):
    if message.asDisplay().startswith("#mc "):
        await app.sendMessage(
            group,
            MessageChain.create(
                [At(sender.id), Plain(await minecraft.judge(message.asDisplay()[4:].strip()))]
            ),
        )