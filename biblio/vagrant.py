# myproject/asgi.py
"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import yourapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings.production')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            yourapp.routing.websocket_urlpatterns
        )
    ),
})
