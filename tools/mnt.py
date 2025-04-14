from fastapi import HTTPException
from mcp.server.fastmcp import FastMCP
from module.mnt import get_movie_and_tv_dialog_id, search_dialogs_messages

# movie and tv module mcp tool

# Initialize FastMCP server
mnt_mcp = FastMCP("tg-retrieval")

@mnt_mcp.tool()
async def search(keyword: str):
    """Search for movie and TV resources with specified keywords."""
    try:
        chat_ids, channel_ids = await get_movie_and_tv_dialog_id()
        messages = await search_dialogs_messages(chat_ids, channel_ids, keyword)
        
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
    # Initialize and run the server
    mnt_mcp.run(transport="sse")