"""
ASGI config for photographApi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photographApi.settings')

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chat.authmiddleware import JwtAuthMiddlewareStack
from chat import routing

application = ProtocolTypeRouter({
    "http":django_asgi_app,
    "https": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        JwtAuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
    ), 
})
