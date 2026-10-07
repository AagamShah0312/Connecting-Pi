import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connecting_pie.settings")
application = get_wsgi_application()
