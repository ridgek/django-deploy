import os
import sys
import site

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), 'firehaz')
SITE_PACKAGES = os.path.join(os.path.dirname(PROJECT_ROOT), 'env/lib/python2.7/site-packages')
site.addsitedir(os.path.abspath(SITE_PACKAGES))

paths = (os.path.abspath(os.path.dirname(__file__)), os.path.abspath(PROJECT_ROOT))
for path in paths:
	if path not in sys.path:
    		sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'example_site.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
