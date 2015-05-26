from fool_deployer import *
from fool_deployer.environments import set_hosts, list_hosts, get_hosts_from_zookeeper
from fabric.api import env, task, run, local, sudo, lcd, put
import posixpath
import os
from functools import partial
from fabric.api import roles, puts, cd
from time import sleep
import getpass
from datetime import datetime
from fool_deployer.deployment import deploy


HOSTS = ['web01.test.sol.fool.com',]


fabpath = os.path.dirname(os.path.abspath(__file__))
env.hosts = HOSTS
env.colors = True
env.user = 'deploy'
env.project_source_path = '/var/src/sol'
env.current = posixpath.join(env.project_source_path, 'current')
env.checkout = env.current
env.get_snapshot = False
env.notify_new_relic = False
env.virtualenv_name = ''
env.virtualenv_root = posixpath.join(env.project_source_path, '.venv')
env.newest_virtualenv = posixpath.join(env.project_source_path, '.venv')
env.run = run
env.project_name = 'content-satellite'
env.supervisor_group = "sol:*"
env.notify_new_relic = False





@task
def test():
    env.environment = 'test'

    set_hosts(HOSTS)

    env.deploy_tasks.insert(0, "build_and_upload_archive")
    env.deploy_tasks.append("static.collectstatic")
    env.deploy_tasks.append("notify_slack")

    env.deploy_tasks.exclude(
        "snapshots.get_snapshot",
        "static.compress",
        "notifications.notify_new_relic",
    )

	

@task
def build_and_upload_archive():
    print '-- build_and_upload_archive START --'

    explode_folder = 'satellite-' + datetime.now().strftime('%Y%m%d_%H%M%S')


    rename_folder = '%s-%s' % (env.project_name, datetime.now().strftime('%Y%m%d_%H%M%S'))

    # create a new source distribution as tarball
    with lcd('..'):
        
        local('python setup.py sdist --formats=gztar > sdist.log', capture=False)

        archive = local('python setup.py --fullname', capture=True).strip()
        archive_name  = '%s.tar.gz' % archive
        
        print 'archive name!!!!!!!!!!!!!!!!!!!', archive_name

        put('dist/%s' % archive_name, '/tmp/%s' % archive_name)
        with cd('/var/src/sol'):
            run('mkdir %s' % explode_folder)
            #run('tar xzf /tmp/%s --wildcards "sol/sol/" --strip-components=1 -C %s' % (archive_name, explode_folder))
            #run('tar xzf /tmp/%s  --strip-components=1 -C %s' % (archive_name, explode_folder))
            run('tar xzf /tmp/%s  --wildcards "Satellite-*/content_satellite" --strip-components=1 -C %s' % (archive_name, explode_folder))
            
            run('mv content_satellite %s' % rename_folder)

            print "renamed folder!!!!!!" , rename_folder

            #with cd('/var/src/sol/%s' % explode_folder):
            #    run('mv satellite/* .')
        run('rm /tmp/%s' % archive_name)

    print '-- build_and_upload_archive END --'



@task
def notify_slack():
    import urllib
    import urllib2
    import json

    url = 'https://fool.slack.com/services/hooks/incoming-webhook?token=Eiy0PpKQacTBVfOVWQhaFJIz'

    payload = {
        'text': "%s deployed %s!" % (getpass.getuser(), env.project_name),
        'channel': '#satellite-of-love',
        'username': 'derploybot',
        'icon_emoji':':sol_2:',
    }

    params = urllib.urlencode({
        'payload': json.dumps(payload),
    })
    urllib2.urlopen(url, params).read()
