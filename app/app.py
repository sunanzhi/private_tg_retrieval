from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.client import init_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_client()
    yield

# Create FastAPI application with metadata
app = FastAPI(
    title="tg retrieval server(with MCP)",
    description="A TG of Server-Sent Events with Model Context Protocol integration",
    version="0.1.0",
    lifespan=lifespan
)