import sys
import os
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printer_supplies.settings')

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(os.getcwd(), 'static'))
application.add_files(os.path.join(os.getcwd(), 'media'), prefix='media/')

if __name__ == '__main__':
    from waitress import serve
    port = int(os.environ.get('PORT', 8080))
    serve(application, host='0.0.0.0', port=port)
