# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from game.routing import websocket_urlpatterns

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })
import os
import asyncio
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from game.routing import websocket_urlpatterns
from game.redis.cleanup import cleanup_stale_users  # Import your cleanup function

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# Get the HTTP application
django_application = get_asgi_application()

# Function to start the periodic cleanup task
async def start_cleanup_task():
    asyncio.create_task(cleanup_stale_users()) #schedules the cleanup_stale_users function as a background task that runs alongside the main application.

# Wrapping the HTTP and WebSocket apps with cleanup logic
async def application_with_cleanup(scope, receive, send):
    # Ensure the cleanup task starts only once
    if scope["type"] == "http" and not hasattr(application_with_cleanup, "_cleanup_started"):
        application_with_cleanup._cleanup_started = True
        await start_cleanup_task()

    if scope["type"] == "http":
        await django_application(scope, receive, send)
    elif scope["type"] == "websocket":
        websocket_application = AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
        await websocket_application(scope, receive, send)

# Create the protocol router
application = ProtocolTypeRouter({
    "http": application_with_cleanup,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
