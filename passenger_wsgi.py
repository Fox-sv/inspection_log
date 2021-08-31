
import os, sys
sys.path.insert(0, '/var/www/u1460148/data/www/inspectionlog.xyz/inspection_log')
sys.path.insert(1, '/var/www/u1460148/data/inspectionlogenv/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'inspection_log.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()