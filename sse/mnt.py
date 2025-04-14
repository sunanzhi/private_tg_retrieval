from tools.mnt import mnt_mcp
from sse.base import BaseSseHandler

# Create SSE transport instance for handling server-sent events
mnt_handler = BaseSseHandler("mnt", mnt_mcp)
