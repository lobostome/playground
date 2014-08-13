from __future__ import with_statement
from fabric.api import task, put, run, local, env, cd, lcd
from time import time
import os

def permissions():
  """Sets permissions for the release"""
  run("chmod -R g+w %s" % (env.releases_dir))
  run("chown -R nginx:nginx %s" % (env.releases_dir))

def create_release_archive():
  """Checkouts and tars the project"""
  if not env.has_key('new_release_name'):
    env.new_release_name = "%.0f" % time()
    env.new_release_gz = "%s%s" % (env.new_release_name, ".tar.gz")
    with lcd(env.tmp_dir):
      local("git clone %s %s" % (env.repo, env.new_release_name))
      local("gnutar -cvzf %s %s" % (env.new_release_gz, env.new_release_name))

def symlink():
  """Updates the symlink to the most recently deployed version"""
  if not env.has_key('current_release'):
    releases()
  run("ln -nfs %s %s" % (env.current_release, env.current_dir))

def releases():
  """Lists the releases"""
  env.releases = sorted(run('ls -x %s' % (env.releases_dir)).split())
  if len(env.releases) >= 1:
    env.current_revision = env.releases[-1]
    env.current_release = "%s/%s" % (env.releases_dir, env.current_revision)
  if len(env.releases) > 1:
    env.previous_revision = env.releases[-2]
    env.previous_release = "%s/%s" % (env.releases_dir,  env.previous_revision)

def post_deploy_hook():
  """Executes various commands after a deploy"""
  run("rm -rf %s/.git" % (env.current_release))

@task
def start():
    """Starts the application server"""
    run("/etc/init.d/nginx start")

@task
def restart():
    """Restart your application"""
    run("/etc/init.d/nginx force-reload")

@task
def stop():
    """Stops the application server"""
    run("/etc/init.d/nginx stop")

@task
def setup():
  '''Prepares for deployment'''
  run("mkdir -p %s" % (env.releases_dir))
  permissions()

@task
def build():
    """Checkouts, tars, and copies the project to the servers"""
    create_release_archive()
    destination_path = "%s/%s" % (env.tmp_dir, env.new_release_gz)
    put(destination_path, destination_path)
    with cd(env.tmp_dir):
      run("tar -xzvf %s" % (env.new_release_gz))
      run("cp -r %s %s/%s" % (env.new_release_name, env.releases_dir, env.new_release_name))

@task
def deploy():
  """Deploys the project"""
  build()
  symlink()
  permissions()
  post_deploy_hook()
  restart()

@task
def clean():
  """Removes old releases"""
  releases()
  if len(env.releases) > env.releases_max:
    directories = env.releases
    directories.reverse()
    del directories[:env.releases_max]
    env.directories = ' '.join([ "%s/%s" % (env.releases_dir, release) for release in directories ])
    run("rm -rf %s" % (env.directories))

@task
def rollback():
  """Performs a rollback to a previous release"""
  releases()
  if len(env.releases) > 1:
    delete_release = env.current_release
    if (env.current_dir):
      run("unlink %s" % (env.current_dir))
    env.current_release = env.previous_release
    symlink()
    run("rm -rf %s" % (delete_release))
