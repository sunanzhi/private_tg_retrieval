from ast import Tuple
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession
import os
import socks
from typing import Tuple, Dict
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 从环境变量获取配置
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
MOVIE_AND_TV_FOLDER_TITLE = os.getenv('MOVIE_AND_TV_FOLDER_TITLE')
TG_SESSION_NAME = os.getenv('TG_SESSION_NAME')
PROXY_STATUS = os.getenv('PROXY_STATUS')
PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = int(os.getenv('PROXY_PORT'))


# 全局客户端实例
client = None
# 初始化客户端连接
async def init_client():
    global client
    if os.path.exists(TG_SESSION_NAME):
        with open(TG_SESSION_NAME, 'r') as f:
            session_str = f.read()
    
    if session_str:
        if PROXY_STATUS == 'True':
            client = TelegramClient(StringSession(session_str), API_ID, API_HASH, proxy=(socks.SOCKS5, PROXY_HOST, PROXY_PORT, True))
        else:
            client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
    else:
        if PROXY_STATUS == 'True':
            client = TelegramClient(StringSession(), API_ID, API_HASH, proxy=(socks.SOCKS5, PROXY_HOST, PROXY_PORT, True))
        else:
            client = TelegramClient(StringSession(), API_ID, API_HASH)
        async with client:
            session_str = client.session.save()
            with open(TG_SESSION_NAME, 'w') as f:
                f.write(session_str)
    
    await client.connect()
    if not await client.is_user_authorized():
        raise Exception("用户未授权，请先登录")
    return client

# 获取影视对话列表id
async def get_movie_and_tv_dialog_id() -> Tuple[Dict[int, int], Dict[int, int]]:
    channle_ids: Dict[int, int] = {}
    chat_ids: Dict[int, int] = {}
    # 获取所有文件夹过滤器
    result = await client(functions.messages.GetDialogFiltersRequest())
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
async def search_dialogs_messages(chat_ids: Dict[int, int], channle_ids: Dict[int, int], keyword):
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
            
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(init_client())