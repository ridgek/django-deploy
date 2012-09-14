django-deploy
=================

Template for [Django](http://www.djangoproject.com) projects,
targetting [Debian](http://debian.org) hosts.

Assuming [virtualenv](http://virtualenv.org) environment with
[Circus](http://circus.io) managing
[Chaussette](http://chaussette.readthedocs.org) WSGI servers, running 
[gevent](http://gevent.org/) workers.

Not necessarily limited to Django, should/will work with any WSGI application.


Usage
-----

1.  Replace `project/` and `manage.py` with your project

2.  Edit `circus.ini` to point to your WSGI application ie. `project.wsgi.application`

3.  Add python/pip dependencies to `requirements.txt`

4.  Add dpkg dependencies to `packages.txt`

5.  Build (set up virtualenv, install pip and dpkg requirements)
        
        $ ./build.sh build
 
6.  Run

        $ source venv/bin/activate
        $ circusd circus.ini
    
7.  Clean up

        $ ./build.sh clean

Not Implemented
---------------

*   Provisioning the server
*   Getting the code to the server, use Fabric and Git
*   Support for non-apt distributions, just edit `build.sh` and `packages.txt`
*   Serving static files, use S3 or nginx
