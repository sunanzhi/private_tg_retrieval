from tools.weather import weather_mcp
from sse.base import BaseSseHandler

# 创建 Weather SSE 处理器实例
weather_handler = BaseSseHandler("weather", weather_mcp)