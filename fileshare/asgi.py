import os

from django.core.asgi import get_asgi_application

from .middleware import DatabaseMiddleware # DatabaseMiddleware from middleware.py



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fileshare.settings')

application = get_asgi_application()
# connect application with DatabaseMiddleware
application = DatabaseMiddleware(application)
