'''
Author: nullptr
Date: 2021-06-13 18:08:06
LastEditTime: 2021-06-17 19:11:35
'''
from .MinecraftApi import MinecraftJsonApi
from graia.application import GraiaMiraiApplication
from graia.application.event.messages import *
from graia.application.event.messages import Group
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema
from loguru import logger
from graia.application.message.elements.internal import At
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter
from utils import Config

__description__ = "自动加入群聊"
__author__ = "nullptr"
__usage__ = "向机器人发送加入群聊邀请，自动同意"
saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)
config = Config().get('minecraft')

api = MinecraftJsonApi(host=config['host'],
                       port=20059,
                       username='admin',
                       password='demo')

print(api.call('getServer'))
