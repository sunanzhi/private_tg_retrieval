from fastapi import Request
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount
from tools.mnt import mnt_mcp
from app.app import app

# Create SSE transport instance for handling server-sent events
mnt_sse = SseServerTransport("/mnt/messages/")

# Mount the /messages path to handle SSE message posting
app.router.routes.append(Mount("/mnt/messages", app=mnt_sse.handle_post_message))

# Add documentation for the /messages endpoint
@app.get("/mnt/messages", tags=["TG-MCP"], include_in_schema=True)
def messages_docs():
    """
    Messages endpoint for SSE communication

    This endpoint is used for posting messages to SSE clients.
    Note: This route is for documentation purposes only.
    The actual implementation is handled by the SSE transport.
    """
    pass  # This is just for documentation, the actual handler is mounted above


@app.get("/mnt/sse", tags=["TG-MCP"])
async def handle_sse(request: Request):
    """
    SSE endpoint that connects to the MCP server

    This endpoint establishes a Server-Sent Events connection with the client
    and forwards communication to the Model Context Protocol server.
    """
    # Use sse.connect_sse to establish an SSE connection with the MCP server
    async with mnt_sse.connect_sse(request.scope, request.receive, request._send) as (
        read_stream,
        write_stream,
    ):
        # Run the MCP server with the established streams
        await mnt_mcp._mcp_server.run(
            read_stream,
            write_stream,
            mnt_mcp._mcp_server.create_initialization_options(),
        )
