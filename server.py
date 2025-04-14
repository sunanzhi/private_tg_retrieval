from dotenv import load_dotenv
import uvicorn
import os
import logging
# 加载 .env 文件
load_dotenv()

DEBUG = os.getenv('DEBUG')
if DEBUG == 'True':
    logging.basicConfig(level=logging.DEBUG)

PORT = int(os.getenv('PORT'))

if __name__ == "__main__":
    uvicorn.run("app.sse:app", host="0.0.0.0", port=PORT, reload=False)