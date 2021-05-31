'''
Author: nullptr
Date: 2021-05-30 21:19:59
LastEditTime: 2021-05-31 21:41:36
'''
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

__name__ = "config"
__description__ = "配置相关"
__author__ = "nullptr"
__usage__ = "在群内发送 '/config' + 命令(需要是管理员) 即可"
saya = Saya.current()
channel = Channel.current()
config = Config()

channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)
inc = InterruptControl(saya.broadcast)


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def group_message_listener(app: GraiaMiraiApplication, group: Group,
                                 message: MessageChain, member: Member):
    message_text = message.asDisplay()
    if message_text := message_text[:8] == '/config' and (
            member.id == config.get("HostQQ")):

        if message_text == 'save':
            await app.sendGroupMessage(
                group,
                MessageChain.create(
                    [At(member.id), Plain("发送 /confirm 以继续运行")]))

            @Waiter.create_using_function([GroupMessage])
            def waiter(event: GroupMessage, waiter_group: Group,
                       waiter_member: Member, waiter_message: MessageChain):
                if all([
                        waiter_group.id == group.id,
                        waiter_member.id == member.id,
                        waiter_message.asDisplay().startswith("/confirm")
                ]):
                    return event

            await inc.wait(waiter)
            config.save()
            logger.info('Config saved')


@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def group_message_listener(friend: Friend, message: MessageChain):
    message_text = message.asDisplay()
    if message_text.startswith('/config') and (friend.id
                                               == config.get("HostQQ")):
        message_text = message_text[8:]
        logger.info(message_text)
        logger.info('ok')
        if message_text.startswith('save'):

            @Waiter.create_using_function([FriendMessage])
            def waiter(event: FriendMessage, waiter_friend: Friend,
                       waiter_message: MessageChain):
                if all([
                        waiter_friend.id == friend.id,
                        waiter_message.asDisplay().startswith("/confirm")
                ]):
                    return event

            await inc.wait(waiter)
            logger.debug(config)

            config.save()
            logger.info('Config saved')
