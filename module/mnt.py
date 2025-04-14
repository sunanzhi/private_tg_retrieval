from ast import Tuple
import string
from telethon import functions, types
import os
from typing import Tuple, Dict
from app.client import get_client

# movie and tv module code

# 从环境变量获取配置
MOVIE_AND_TV_FOLDER_TITLE = os.getenv('MOVIE_AND_TV_FOLDER_TITLE')
# 获取影视对话列表id
async def get_movie_and_tv_dialog_id() -> Tuple[Dict[int, int], Dict[int, int]]:
    client = await get_client()
    channle_ids: Dict[int, int] = {}
    chat_ids: Dict[int, int] = {}
    # 获取所有文件夹过滤器
    result = await client(functions.messages.GetDialogFiltersRequest())
    if not isinstance(result, types.messages.DialogFilters):
        raise Exception("get dialog filters failed!")
    # 使用 result.filters 来获取过滤器列表
    for folder in result.filters:
        # 只处理自定义文件夹
        if isinstance(folder, types.DialogFilter):  
            # 仅指定文件夹名称
            if folder.title.text != MOVIE_AND_TV_FOLDER_TITLE:
                continue
            if folder.include_peers:
                for peer in folder.include_peers:
                    # 仅处理群组和频道
                    if isinstance(peer, types.InputPeerChat):
                        chat_ids[peer.chat_id] = peer.chat_id
                    elif isinstance(peer, types.InputPeerChannel):
                        # 添加 -100 前缀
                        channel_id = int(f"-100{peer.channel_id}")
                        channle_ids[channel_id] = channel_id

    return chat_ids, channle_ids

# 搜索指定关键字的消息
async def search_dialogs_messages(chat_ids: Dict[int, int], channle_ids: Dict[int, int], keyword: string):
    if keyword is None or keyword == '':
        return []
    client = await get_client()
    messages = []
    # 获取所有对话（群组、频道、私聊）
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if isinstance(dialog.entity, types.Channel):
            id = channle_ids.get(dialog.id)
        elif isinstance(dialog.entity, types.Chat):
            id = chat_ids.get(dialog.id)
        else:
            continue

        if id is not None:
            async for message in client.iter_messages(
                dialog.entity, 
                search=keyword,  # 支持模糊匹配
                limit=100        # 控制单次检索量
            ):
                messages.append(message)
                # print(f"来源：{dialog.name} | 时间：{message.date} | 内容：{message.text}")

    return messages