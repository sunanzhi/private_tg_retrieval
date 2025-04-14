from fastapi import Request
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount
from typing import Optional
from app.app import app

class BaseSseHandler:
    def __init__(self, prefix: str, fastmcp: FastMCP):
        self.prefix = prefix
        self.sse = SseServerTransport(f"/{prefix}/messages/")
        self.fastmcp = fastmcp
        self._setup_routes()

    def _setup_routes(self):
        # 挂载消息处理路由
        app.router.routes.append(
            Mount(f"/{self.prefix}/messages", app=self.sse.handle_post_message)
        )

        # 添加文档路由
        @app.get(f"/{self.prefix}/messages", tags=[f"{self.prefix}-mcp"], include_in_schema=True)
        def messages_docs():
            """
            Messages endpoint for SSE communication

            This endpoint is used for posting messages to SSE clients.
            Note: This route is for documentation purposes only.
            The actual implementation is handled by the SSE transport.
            """
            pass

        # 添加 SSE 处理路由
        @app.get(f"/{self.prefix}/sse", tags=[f"{self.prefix}-mcp"])
        async def handle_sse(request: Request):
            async with self.sse.connect_sse(
                request.scope, request.receive, request._send
            ) as (read_stream, write_stream):
                await self.fastmcp._mcp_server.run(
                    read_stream,
                    write_stream,
                    self.fastmcp._mcp_server.create_initialization_options(),
                )