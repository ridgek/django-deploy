import os

from fabric.api import env, run, cd, sudo, require, settings
from fabric.contrib import files

# Name of the django-project
# Example: "example_site"
env.project = ""

# User to use on remote hosts
# This user should have write permission for root directory
# Example: "example_user"
env.user = ""

# Root for deployment
# Example: "/home/example_user/django-deploy"
env.root = ""

# Django Project root
# Example: "/home/example_user/django-deploy/example_site"
env.project_root = os.path.join(env.root, env.project)

# Python virtualenv root
# Example: "/home/example_user/django-deploy/env"
env.env_root = os.path.join(env.root, "env")

# pip requirements file location
# Example: "/home/example_user/django-deploy/env"
env.requirements = os.path.join(env.root, "requirements.txt")

# Apache config root
# Example: "/home/example_user/django-deploy/apache"
env.apache_config_root = os.path.join(env.root, "apache")

# Git repository URI
# Example: "git://github.com/example_user/example_site.git"
env.repo = ""

# Git repository branch
# Example: "master"
env.branch = "master"

# Packages to apt-get install
# Example: ("vrms", "apache2", "python-dev")
env.packages = ("git", "python-dev", "python-setuptools",
        "apache2", "libapache2-mod-wsgi",
        "libsqlite3-0", "python-virtualenv",)

def deploy():
    """
    Deploy onto host(s)
    Hosts can be virgin or already deployed
    """
    #Install packages
    if env.packages not None:
        sudo("apt-get update -q")
        sudo("apt-get install -q -y --no-upgrade %s" % " ".join(env.packages))
        
    #Create root directory
    run("mkdir -p %(root)s" % env)

    #Clone into root directory (if .git does not exist)
    with cd(env.root):
        if not files.exists(os.path.join(env.root, ".git")):
            run("git clone %(repo)s ." % env)
            #Set git user (for messy merges)
            run("git config user.name 'DeployServer'; git config user.email 'admin@firehaz.co.nz'")
        pull()

    #Create virtualenv (if it does not already exist)
    run("mkdir -p %(env_root)s" % env)
    run("virtualenv %(env_root)s" % env)
    
    #Populate virtualenv
    update_requirements()

    #Configure apache
    with cd("/etc/apache2"):
        sudo("rm -rf apache2.conf conf.d/ httpd.conf magic mods-* sites-* ports.conf")
        sudo("ln -s %(apache_config_root)s/apache2.conf ./apache2.conf" % env)
        sudo("mkdir -m777 -p /var/www/.python-eggs")
        restart()

def pull():
    """
    Pull branch HEAD from git repo
    """
    with cd(env.root):
        run("git reset --hard")
        run("git pull origin %(branch)s" % env)
        
def reset(hash):
    """
    Reset to specified revision from git repo
    Usage:
        reset:ha5h
    """
    with cd(env.root):
        pull()
        run("git reset --hard %s" % hash)

def update_requirements():
    """
    Update python packages using requirements.txt
    """
    run("pip install -E %(env_root)s -r %(requirements)s" % env)
    
def collect_static():
    """
    Collect app static files into project static folder
    """
    with cd(env.project_root):
        run("%(env_root)s/bin/python manage.py collectstatic -v0 --noinput" % env)
        
def restart():
    """
    Restart apache
    """
    sudo("apache2ctl restart")
    
def clean():
    """
    Destroy everything
    """
    sudo("rm -rf $(root)s" % env)
    sudo("apache2ctl stop")
    
