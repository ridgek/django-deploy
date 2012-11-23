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

License
-------

Copyright (C) 2012 Ridge Kennedy

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
