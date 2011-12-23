django-deploy
=================

Template for deploying [Django](http://www.djangoproject.com) projects
to [Debian Wheezy](http://debian.org) hosts,
using [Fabric](http://fabfile.org)
and [Git](http://git-scm.com).

The template assumes a deployment of [Gunicorn](http://gunicorn.org)
running behind [Nginx](http://wiki.nginx.org).

No database deployment is currently implemented.


Requirements
------------

#### Local ####

* python >= 2.6

* virtualenv

* setuptools

* fabric >= 1.3.2

#### Remote ####

* Debian Wheezy or newer

* SSH access


Project Layout
--------------

A basic directory structure is assumed.

    django_deploy/
        nginx/
            nginx.conf       -- Nginx config file
        gunicorn/
            gunicorn-default -- for /etc/default/gunicorn
            djangotest.py    -- Gunicorn config file
        env/                 -- Python virtualenv 
        djangotest/          -- Django project
        fabfile.py
        requirements.txt     -- Pip requirements file

