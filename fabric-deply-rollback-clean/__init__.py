from fabric.api import env
import deploy

env.user = "root"
env.port = 22
env.hosts = [
  'host1',
  'host2'
]
env.base_dir = "/var/www"
env.releases_dir = "%s/releases" % (env.base_dir)
env.tmp_dir = "/tmp"
env.releases_max = 5
env.current_dir = "%s/current" % (env.base_dir)
env.repo = "https://github.com/some-profile/some-repo.git"
