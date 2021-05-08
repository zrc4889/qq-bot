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
__description__ = "自动加入群聊"
__author__ = "nullptr"
__usage__ = "向机器人发送加入群聊邀请，自动同意"
saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)

@channel.use(ListenerSchema(listening_events=[BotInvitedJoinGroupRequestEvent]))
async def group_message_listener(event: BotInvitedJoinGroupRequestEvent):
    await event.accept()

