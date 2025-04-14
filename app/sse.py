from starlette.routing import Mount
from app.app import app
from sse.mnt import mnt_handler
from sse.weather import weather_handler

# Mount the /messages path to handle SSE message posting
app.router.routes.append(Mount("/mnt/messages", app=mnt_handler.sse.handle_post_message))
app.router.routes.append(Mount("/weather/messages", app=weather_handler.sse.handle_post_message))


# import config routes
import config.routes