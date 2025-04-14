from telethon import TelegramClient
from telethon.sessions import StringSession
import os
import socks
from app.common import base_path

# get env
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
MOVIE_AND_TV_FOLDER_TITLE = os.getenv('MOVIE_AND_TV_FOLDER_TITLE')
TG_SESSION_NAME = os.getenv('TG_SESSION_NAME')
PROXY_STATUS = os.getenv('PROXY_STATUS')
PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = int(os.getenv('PROXY_PORT'))

# global tg client
client = None
session_path = os.path.join(base_path, 'session')
session_file = os.path.join(session_path, TG_SESSION_NAME)
# init tg client connection
async def init_client():
    global client
    session_str = None
    if os.path.exists(session_file):
        with open(session_file, 'r') as f:
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
            print(session_str)
            with open(session_file, 'w') as f:
                f.write(session_str)
    
    await client.connect()
    if not await client.is_user_authorized():
        raise Exception("user not authorized!")
    return client

async def get_client():
    global client
    if client is None:
        client = await init_client()
    return client

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(init_client())