"""
WSGI config for food_viser project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_viser.settings")

if settings.DEBUG:
    application = StaticFilesHandler(get_wsgi_application())
else:
    application = get_wsgi_application()
    
#waitress-serve --listen=127.0.0.1 myapp.wsgi:application
