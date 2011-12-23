import os
import sys

from fabric.api import env, run, cd, sudo, get, settings, local
from fabric.contrib import files
from fabric.colors import red

env.hosts = ['example.com']

# User to use on remote host
# Edit gunicorn config file to reflect this change
env.user = 'example_user'

# Django project name (same as directory name)
env.project = 'djangotest'

# Path to the root of the installation (where to clone to)
# Edit gunicorn and nginx config files to reflect this change
env.root = '/home/example_user/django-deploy'

# Path to the project root
env.project_root = os.path.abspath(os.path.join(env.root, env.project))
# Path to the virtualenv root 
env.env_root = os.path.abspath(os.path.join(env.root, 'env'))
# Path to the pip requirements file
env.requirements = os.path.abspath(os.path.join(env.root, 'requirements.txt'))

# Git repository to use
env.git_repo = 'git://github.com/ridgek/django-deploy.git'
env.git_branch = 'master'

# Location of gunicorn config file
env.gunicorn_config = os.path.abspath(os.path.join(env.root, 'gunicorn', 'djangotest.py'))
# Location of gunicorn default file (for /etc/default/gunicorn)
env.gunicorn_default = os.path.abspath(os.path.join(env.root, 'gunicorn', 'gunicorn-default'))
# Location of nginx config file
env.nginx_config = os.path.abspath(os.path.join(env.root, 'nginx', 'nginx.conf'))


env.apt_packages = [
	'git',
	'python-setuptools',
	'python-virtualenv',
	'build-essential',
	
	'gunicorn',
	'nginx-full',

	'libsqlite3-0',
]

def deploy_local():
	"""Set up local virtualenv"""
	local('mkdir -p %s' % os.path.split(env.env_root)[1])
	local('virtualenv --no-site-packages %s' % os.path.split(env.env_root)[1])
	local('. %s/bin/activate; pip install -E %s -r %s' % 
		(os.path.split(env.env_root)[1],
		os.path.split(env.env_root)[1],
		os.path.split(env.requirements)[1]))

def deploy():
	"""Deploy to host(s)."""
	run('mkdir -p %(root)s' % env)
	update_packages()
	configure_virtualenv()
	configure_gunicorn()
	configure_nginx()
	syncdb()
	collect_static()
	restart()

def configure_git():
	"""Configure git repository.
	
	Defines user.name and user.email incase a merge happens.
	
	"""
	with cd(env.root):
		if not files.exists(os.path.abspath(os.path.join(env.root, '.git'))):
			run('git clone %(git_repo)s .' % env)
			run('git config user.name "No One"')
			run('git config user.email none@none')
		pull()

def configure_virtualenv():
	"""Configure virtualenv."""
	run('mkdir -p %(env_root)s' % env)
	run('virtualenv --no-site-packages %(env_root)s' % env)
	update_requirements()

def configure_gunicorn():
	"""Configure gunicorn.
	
	Move /etc/gunicorn.d to /etc/gunicorn to prevent RuntimeErrors,
	see https://github.com/lamby/pkg-gunicorn/issues/8 for details.
	
	"""
	with settings(warn_only=True):
		sudo('rm /etc/default/gunicorn')
		sudo('ln -s %(gunicorn_default)s /etc/default/gunicorn' % env)
		sudo('mkdir -p /etc/gunicorn')
		sudo('mv /etc/gunicorn.d/* /etc/gunicorn/')
		sudo('rm -r /etc/gunicorn.d')
		sudo('ln -s /etc/gunicorn /etc/gunicorn.d')
		sudo('rm /etc/gunicorn.d/%(project)s' % env)
		sudo('ln -s %(gunicorn_config)s /etc/gunicorn.d/%(project)s' % env)
		
def configure_nginx():
	"""Configure nginx."""
	with settings(warn_only=True):
		sudo('cd /etc/nginx; rm -r nginx.conf sites-available/ sites-enabled/')
		sudo('ln -s %(nginx_config)s /etc/nginx/nginx.conf' % env)

def generate_key():
	"""Generate a RSA key, and get the public key.
	
	Copys the public key into the directory of this file.
	
	"""
	run('ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa')
	get('~/.ssh/id_rsa.pub', '%(host)s.pub' % env)

def pull():
	"""Pull branch HEAD from git repo.
	
	Performs a `reset --hard` before the pull to prevent merges.
	
	"""
	with cd(env.root):
		run('git reset --hard')
		run('git pull origin %(git_branch)s' % env)
		
def reset(hash):
	"""Reset to specified revision from git repo."""
	with cd(env.root):
		run('git reset --hard %s' % hash)

def update_packages():
	"""Update apt packages."""
	if not env.apt_packages == None:
		with settings(warn_only=True):
			sudo('apt-get update -q')
		sudo('apt-get install -q -y %s' % ' '.join(env.apt_packages))

def update_requirements():
	"""Update virtualenv packages using requirements.txt."""
	run('. %(env_root)s/bin/activate; pip install -E %(env_root)s -r %(requirements)s' % env)
	
def collect_static():
	"""Collect app static files into project static folder."""
	if files.exists('%(env_root)s/bin/python' % env):
		with cd(env.project_root):
			run('%(env_root)s/bin/python manage.py collectstatic -v0 --noinput' % env)
	else:
		print(red('collect_static failed: env does not exist'))
		
def syncdb():
	"""Run django syncdb."""
	if files.exists('%(env_root)s/bin/python' % env):
		with cd(env.project_root):
			run('%(env_root)s/bin/python manage.py syncdb' % env)
	else:
		print(red('syncdb failed: env does not exist'))
	
def reload():
	"""Reload gunicorn and nginx."""
	sudo('/etc/init.d/gunicorn reload')
	sudo('/etc/init.d/nginx reload')

def restart():
	"""Restart gunicorn and nginx."""
	sudo('/etc/init.d/gunicorn restart')
	sudo('/etc/init.d/nginx restart')

