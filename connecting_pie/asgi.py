import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connecting_pie.settings")
application = get_asgi_application()
