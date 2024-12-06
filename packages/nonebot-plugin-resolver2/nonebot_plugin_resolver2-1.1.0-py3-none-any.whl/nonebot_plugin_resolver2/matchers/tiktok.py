import re, httpx

from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Event, Message

from .filter import resolve_filter
from .utils import get_video_seg
from ..core.ytdlp import *
from ..config import *

tiktok = on_regex(
    r"(www.tiktok.com|vt.tiktok.com|vm.tiktok.com)", priority=1
)

@tiktok.handle()
@resolve_filter
async def _(event: Event) -> None:
    """
        tiktok解析
    :param event:
    :return:
    """
    # 消息
    url: str = str(event.message).strip()

    url_reg = r"(http:|https:)\/\/www.tiktok.com\/[A-Za-z\d._?%&+\-=\/#@]*"
    url_short_reg = r"(http:|https:)\/\/vt.tiktok.com\/[A-Za-z\d._?%&+\-=\/#]*"
    url_short_reg2 = r"(http:|https:)\/\/vm.tiktok.com\/[A-Za-z\d._?%&+\-=\/#]*"

    if "vt.tiktok" in url:
        temp_url = re.search(url_short_reg, url)[0]
        temp_resp = httpx.get(temp_url, follow_redirects=True, proxies=PROXY)
        url = temp_resp.url
    elif "vm.tiktok" in url:
        temp_url = re.search(url_short_reg2, url)[0]
        temp_resp = httpx.get(temp_url, headers={ "User-Agent": "facebookexternalhit/1.1" }, follow_redirects=True,
                              proxies=PROXY)
        url = str(temp_resp.url)
    else:
        url = re.search(url_reg, url)[0]
    try:
        info = await get_video_info(url)
        await tiktok.send(Message(f"{NICKNAME}解析 | TikTok - {info['title']}"))
    except Exception as e:
        await tiktok.send(Message(f"{NICKNAME}解析 | TikTok - 标题获取出错: {e}"))
    try:
        video_name = await ytdlp_download_video(url = url)
        await tiktok.send(await get_video_seg(video_name))
    except Exception as e:
        await tiktok.send(f"下载失败 | {e}")


