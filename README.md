django-deploy
=================

Template for deploying [Django](http://www.djangoproject.com)
projects using [Fabric](http://fabfile.org).


Requirements
------------

#### Local

* python => 2.6

* setuptools

* fabric => 1.3.2

#### Remote 

* apt

* sshd

* python => 2.6 (edit site-dir in `example_site.wsgi`)

* virtualenv

* pip


Configuration
-------------

Configuration of deployment is done by changing values in `fabfile.py`


Project Layout
--------------

A basic directory structure is assumed

    django_deploy/         -- This should be the root of a git repository
        apache/
            apache2.conf   -- Apache2 config file
        env/               -- Python virtualenv 
        example_site/      -- Django project
        example_site.wsgi  -- mod_wsgi configuration
        fabfile.py


Usage
-----

`fab TARGET COMMAND...`

#### Targets

* `production` - Target production host(s)

* `staging` - Target staging host(s)

#### Commands

* `deploy` - Deploy the host (apt-get, virtualenv, git clone)

* `pull` - git pull

* `reset:HASH` - git reset (`reset:4jg6` is equivalent to `git reset 4jq6`)

* `update_requirements` - Use PIP to update the virtualenv requirements

* `restart` - Restart apache2 (`apapche2ctl restart`)

* `collect_static` - Collect Django static files (`manage.py collectstatic`)

* `clean` - Clean (undeploy) the host
