import sys
import os
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printer_supplies.settings')
from waitress import serve
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
serve(application, host='0.0.0.0', port=8080)