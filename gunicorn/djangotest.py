# gunicorn config file
# /etc/gunicorn.d/djangotest.py

import multiprocessing
import sys

version = '%i.%i' % sys.version_info[:2]
worker_count = (multiprocessing.cpu_count()*2+1)

CONFIG = {
    'mode': 'django',
    'environment': {
        'PYTHONPATH': '/home/example_user/django-deploy/env/lib/python%s/site-packages' % version
    },
    #'working_dir': '',
    'user': 'example_user',
    'group': 'example_user',
    'args': (
        '--bind=127.0.0.1:8000',
        '--workers=%i' % worker_count,
        #'--worker-class=egg:gunicorn#sync',
        '--timeout=30',
        '/home/example_user/django-deploy/djangotest/settings.py',
    ),
}
