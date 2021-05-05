from graia.application.event.messages import *
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.saya.event import SayaModuleInstalled
from loguru import logger
from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain
from graia.application.event.messages import Group
from graia.application.event.mirai import BotInvitedJoinGroupRequestEvent
from graia.application.message.elements.internal import Plain
__description__ = "使用谷歌翻译20次不同语言后返回"
__author__ = "nullptr"
__usage__ = "在群内发送 '/GT ' + 要翻译的内容 即可"
saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

@channel.use(ListenerSchema(listening_events=[BotInvitedJoinGroupRequestEvent]))
async def group_message_listener(event: BotInvitedJoinGroupRequestEvent):
    await event.accept()

