"""
WSGI config for microsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import socket
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microsite.settings")

from django.core.wsgi import get_wsgi_application

if socket.gethostbyname(socket.gethostname()) == "136.243.86.126":
    import newrelic.agent
    newrelic.agent.initialize('/home/micropyramid.com/newrelic.ini')

application = get_wsgi_application()
