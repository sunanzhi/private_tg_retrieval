from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from contextlib import asynccontextmanager
from tg import init_client, get_movie_and_tv_dialog_id, search_dialogs_messages
import os
import logging

DEBUG = os.getenv('DEBUG')
if DEBUG == 'True':
    logging.basicConfig(level=logging.DEBUG)
# 加载 .env 文件
load_dotenv()

PORT = int(os.getenv('PORT'))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    await init_client()
    yield
    # 关闭时执行
    # 如果需要清理资源可以在这里添加

app = FastAPI(lifespan=lifespan)

class SearchRequest(BaseModel):
    keyword: str

@app.get("/")
async def root():
    return {"message": "Telegram search already started"}

@app.post("/search")
async def search(request: SearchRequest):
    try:
        chat_ids, channel_ids = await get_movie_and_tv_dialog_id()
        messages = await search_dialogs_messages(chat_ids, channel_ids, request.keyword)
        
        # 将消息转换为可序列化的格式
        results = []
        for msg in messages:
            results.append({
                "source": msg.chat.title if msg.chat else "未知",
                "date": msg.date.isoformat(),
                "text": msg.text,
                "message_id": msg.id
            })
        
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("http_server:app", host="0.0.0.0", port=PORT, reload=True)