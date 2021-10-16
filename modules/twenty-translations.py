<<<<<<< HEAD
"""
Author: nullptr
Date: 2021-05-11 20:17:40
LastEditTime: 2021-07-27 20:19:13
"""
from re import I
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
from async_google_trans_new import google_translator
=======
from typing import Union

from google_trans_new import google_translator
from graia.application import GraiaMiraiApplication
from graia.application.event.messages import *
from graia.application.event.messages import Group
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema
from loguru import logger
>>>>>>> origin/master

__name__ = "twenty-translations"
__description__ = "使用谷歌翻译20次不同语言后返回"
__author__ = "nullptr"
__usage__ = "在群内发送 '/GT ' + 要翻译的内容 即可"
saya = Saya.current()
channel = Channel.current()
<<<<<<< HEAD
=======

>>>>>>> origin/master
channel.name(__name__)
channel.description(f"{__description__}\n使用方法：{__usage__}")
channel.author(__author__)


<<<<<<< HEAD
async def translation(result: str) -> str:
    translator = google_translator()
    trans_dict = {
        "苗语": "hmn",
        "挪威语": "no",
        "日语": "ja",
        "德语": "de",
        "荷兰语": "nl",
        "泰卢固语": "te",
        "卢旺达语": "rw",
        "旁遮普语": "pa",
        "意第绪语": "yi",
        "克罗地亚语": "hr",
        "奥利亚语": "or",
        "塔吉克语": "tg",
        "俄语": "ru",
        "古吉拉特语": "gu",
        "菲律宾语": "tl",
        "马尔加什语": "mg",
        "塞索托语": "st",
        "亚美尼亚语": "hy",
        "印尼爪哇语": "jw",
        "英语": "en",
        "返回中文": "zh-CN",
    }
    res = ""
    for key in trans_dict:
        target = trans_dict[key]
        result = await translator.translate(result, lang_tgt=target)
        res += key + " -> " + result + "\n"
    return res


@channel.use(ListenerSchema(listening_events=[MessageEvent]))
async def event_receiver(message: MessageChain, rs: Relationship):
    if message.as_display().startswith("/GT "):
        await rs.exec(
            MessageSend(
                MessageChain.create(
                    [
                        Notice(target=rs.ctx.id),
                        await formatted_output_translate(message.as_display()[4:]),
                    ]
                )
            )
        )


async def formatted_output_translate(result: str) -> Text:
    translated_text = await translation(result)
    temp_output_substring = [
        "\n------翻译结果------\n\n",
        translated_text,
        "\n\n----------------\n\n",
    ]
    content = "".join(temp_output_substring)
    return Text(text=content)
=======
async def translation(result: str):
    logger.debug('Starting Translate...')
    translator = google_translator()
    trans_dict = {
        '苗语': 'hmn',
        '挪威语': 'no',
        '日语': 'ja',
        '德语': 'de',
        '荷兰语': 'nl',
        '泰卢固语': 'te',
        '卢旺达语': 'rw',
        '旁遮普语': 'pa',
        '意第绪语': 'yi',
        '克罗地亚语': 'hr',
        '奥利亚语': 'or',
        '塔吉克语': 'tg',
        '俄语': 'ru',
        '古吉拉特语': 'gu',
        '菲律宾语': 'tl',
        '马尔加什语': 'mg',
        '塞索托语': 'st',
        '亚美尼亚语': 'hy',
        '印尼爪哇语': 'jw',
        '英语': 'en',
        '返回中文': 'zh-CN'
    }
    res = ''
    for key in trans_dict:
        target = trans_dict[key]
        result = translator.translate(result, lang_tgt=target)
        res += key + ' -> ' + result + '\n'
        logger.debug(result)
    return res


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def group_message_listener(app: GraiaMiraiApplication, group: Group,
                                 message: MessageChain):
    await judge(app, group, message)


@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def group_message_listener(app: GraiaMiraiApplication, friend: Friend,
                                 message: MessageChain):
    await judge(app, friend, message)


async def judge(app: GraiaMiraiApplication, some: Union[Friend, Group], message: MessageChain):
    message_text = message.asDisplay()
    if message_text.startswith('/GT '):
        logger.info("Get Result!")
        msg = MessageChain.create([Plain(text='正在翻译，请等待亿分钟……')])
        if type(some) is Friend:
            await app.sendFriendMessage(some, msg)
            await app.sendFriendMessage(
                some, await formatted_output_translate(message_text[5:]))
        else:
            await app.sendGroupMessage(some, msg)
            await app.sendGroupMessage(
                some, await formatted_output_translate(message_text[5:]))


async def formatted_output_translate(result: str):
    translated_text = await translation(result)
    temp_output_substring = ["------翻译结果------\n\n", translated_text, "\n\n----------------\n\n"]
    content = "".join(temp_output_substring)
    return MessageChain.create([Plain(text=content)])
>>>>>>> origin/master
