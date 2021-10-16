import os
import json
import time
import asyncio
import requests
from io import BytesIO
import aiohttp
from pathlib import Path

# from graiax import silkcoder
from graia.saya import Saya, Channel
from graia.broadcast.interrupt.waiter import Waiter
from graia.broadcast.interrupt import InterruptControl
from graia.saya.builtins.broadcast.schema import ListenerSchema
from avilla.core import Avilla, profile
from avilla.core.builtins.profile import MemberProfile, GroupProfile, FriendProfile
from avilla.core.tools.filter import Filter
from avilla.core.event.message import MessageEvent
from avilla.core.execution.message import MessageId, MessageSend
from avilla.core.message.chain import MessageChain
from avilla.core.network.clients.aiohttp import AiohttpWebsocketClient
from avilla.onebot.config import OnebotConfig, WebsocketCommunication
from avilla.onebot.protocol import OnebotProtocol
from avilla.core.relationship import Relationship
from avilla.core.builtins.elements import Image, Text, Voice, Notice
from avilla.core.tools.literature import Literature
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema

saya = Saya.current()
channel = Channel.current()
bcc = saya.broadcast
inc = InterruptControl(bcc)

if not os.path.exists("./modules/CloudMusic/temp/"):
    print("正在创建音乐缓存文件夹")
    os.mkdir("./modules/CloudMusic/temp/")
    # os.mkdir("./modules/CloudMusic/temp/out")

phone = 18065063388
password = "wfx26239291/"
HOST = "http://netease.weifx.ml"
login = requests.get(
    f"{HOST}/login/cellphone?phone={phone}&password={password}"
).cookies

WAITING = []


async def check(rs1: Relationship, rs2: Relationship) -> bool:
    return (
        (
            all(
                [
                    isinstance(rs1.ctx.profile, FriendProfile),
                    isinstance(rs2.ctx.profile, FriendProfile),
                ]
            )
            and all([rs2.ctx.id == rs1.ctx.id])
        )
    ) or (
        all(
            [
                isinstance(rs1.ctx.profile, MemberProfile),
                isinstance(rs2.ctx.profile, MemberProfile),
            ]
        )
        and all(
            [
                rs2.ctx.profile.group.id == rs1.ctx.profile.group.id,
                rs2.ctx.id == rs1.ctx.id,
            ]
        )
    )


@channel.use(
    ListenerSchema(
        listening_events=[MessageEvent], inline_dispatchers=[Literature("网易云点歌")]
    )
)
async def what_are_you_saying(rs: Relationship, message: MessageChain):
    @Waiter.create_using_function([MessageEvent])
    async def waiter1(waiter1_rs: Relationship, waiter1_message: MessageChain):
        if await check(rs, waiter1_rs):
            waiter1_saying = waiter1_message.as_display()
            if waiter1_saying == "取消":
                return False
            else:
                return waiter1_saying

    @Waiter.create_using_function([MessageEvent])
    async def waiter2(waiter2_rs: Relationship, waiter2_message: MessageChain):

        if await check(rs, waiter2_rs):
            if waiter2_message.as_display() == "取消":
                return False
            elif waiter2_message.as_display() in [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "8",
                "10",
            ]:
                return waiter2_message.as_display()
            else:
                await rs.exec(
                    MessageSend(
                        (MessageChain.create([Text("请发送歌曲 id<1-10> 来点歌，发送取消可终止本次点歌")]))
                    ).render(sender=Notice(rs.ctx.id))
                )

    if rs.ctx.id not in WAITING:
        saying = message.as_display().split(" ", 1)
        WAITING.append(rs.ctx.id)

        if len(saying) == 1:
            waite_musicmessageId = await rs.exec(
                MessageSend(MessageChain.create([Text(f"请发送歌曲名，发送取消即可终止点歌")]))
            )
            try:
                musicname = await asyncio.wait_for(inc.wait(waiter1), timeout=15)
                if not musicname:
                    WAITING.remove(rs.ctx.id)
                    return await rs.exec(
                        MessageSend(MessageChain.create([Text("已取消点歌")]))
                    )
            except asyncio.TimeoutError:
                WAITING.remove(rs.ctx.id)
                return await rs.exec(MessageSend(MessageChain.create([Text("点歌超时")])))
        else:
            musicname = saying[1]
        times = str(int(time.time()))
        search = requests.get(
            url=f"{HOST}/cloudsearch?keywords={musicname}&timestamp={times}",
            cookies=login,
        )
        if json.loads(search.text)["result"]["songCount"] == 0:
            WAITING.remove(rs.ctx.id)
            return await rs.exec(MessageSend(MessageChain.create([Text("未找到此歌曲")])))
        musiclist = json.loads(search.text)["result"]["songs"]
        musicIdList = []
        msg = "为你在网易云音乐找到以下歌曲！\n==============================="
        num = 1
        for music in musiclist:
            if num > 10:
                break
            music_id = music["id"]
            music_name = music["name"]
            music_ar = []
            for ar in music["ar"]:
                music_ar.append(ar["name"])
            music_ar = "/".join(music_ar)
            msg += f"\n{num}　--->　{music_name} - {music_ar}"
            musicIdList.append(music_id)
            num += 1
        msg += f"\n===============================\n发送歌曲id可完成点歌\n发送取消可终止当前点歌\n"
        waite_musicmessageId = await rs.exec(
            MessageSend(MessageChain.create([Text(msg)]))
        )

        try:
            wantMusicID = await asyncio.wait_for(inc.wait(waiter2), timeout=30)
            if not wantMusicID:
                WAITING.remove(rs.ctx.id)
                return await rs.exec(MessageSend(MessageChain.create([Text("已取消点歌")])))
        except asyncio.TimeoutError:
            WAITING.remove(rs.ctx.id)
            return await rs.exec(
                MessageSend(
                    MessageChain.create([Text("点歌超时")]),
                    quote=waite_musicmessageId.messageId,
                )
            )

        musicid = musicIdList[int(wantMusicID) - 1]
        # print(musicid)
        times = str(int(time.time()))
        musicinfo = requests.get(
            url=f"{HOST}/song/detail?ids={musicid}&timestamp={times}", cookies=login
        ).json()
        # print(musicinfo)
        musicurl = requests.get(
            url=f"{HOST}/song/url?id={musicid}&br=128000&timestamp={times}",
            cookies=login,
        ).json()

        if not os.path.exists(f"./modules/CloudMusic/temp/{musicid}.mp3"):
            music_url = musicurl["data"][0]["url"]
            if music_url == None:
                WAITING.remove(rs.ctx.id)
                return await rs.exec(
                    MessageSend(
                        MessageChain.create([Text("该歌曲暂无法点歌")]),
                    )
                )
            r = requests.get(music_url)
            music_fcontent = r.content
            print(f"正在缓存歌曲：{music_name}")
            with open(f"./modules/CloudMusic/temp/{musicid}.mp3", "wb") as f:
                f.write(music_fcontent)

        music_name = musicinfo["songs"][0]["name"]
        music_ar = []
        for ar in musicinfo["songs"][0]["ar"]:
            music_ar.append(ar["name"])
        music_ar = "/".join(music_ar)
        music_al = musicinfo["songs"][0]["al"]["picUrl"] + "?param=300x300"
        await rs.exec(
            MessageSend(
                MessageChain.create(
                    [
                        Text(f"\n曲名：{music_name}\n作者：{music_ar}"),
                        Text(
                            "\n超过9:00的歌曲将被裁切前9:00\n歌曲时长越长音质越差\n超过4分钟的歌曲音质将受到较大程度的损伤\n发送语音需要一定时间，请耐心等待"
                        ),
                    ]
                )
            )
        )

        # cache = Path(f'./modules/CloudMusic/temp/out/{musicid}.mp3')
        # cache.write_bytes(await silkcoder.encode(
        #     f'./modules/CloudMusic/temp/{musicid}.mp3', t=540, rate=100000))
        await rs.exec(
            MessageSend(
                MessageChain.create(
                    [
                        Voice.fromLocalFile(
                            Path(f"./modules/CloudMusic/temp/{musicid}.mp3")
                        )
                    ]
                )
            )
        )
        # os.remove(f'{MIRAI_PATH}data/net.mamoe.mirai-api-http/voices/{musicid}')
        return WAITING.remove(rs.ctx.id)


@channel.use(
    ListenerSchema(
        listening_events=[MessageEvent],
        inline_dispatchers=[Literature("查看点歌状态")],
        decorators=[Filter(lambda rs: rs.ctx.id == 1958731779)],
    )
)
async def main(rs: Relationship):
    runlist_len = len(WAITING)
    runlist = "\n".join(map(lambda x: str(x), WAITING))
    if runlist_len > 0:
        await rs.exec(
            MessageSend(
                MessageChain.create(
                    [Text(f"当前共有 {runlist_len} 人正在点歌"), Text(f"\n{runlist}")]
                )
            )
        )
    else:
        await rs.exec(MessageSend(MessageChain.create([Text(f"当前没有正在点歌的人")])))
