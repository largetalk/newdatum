#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import *
from fabric.colors import green,red
from fabric.tasks import Task
import os
import functools


@task
def usage():
    print 'fab -f %s -H host -u user command[:root=sailfish]' % (os.path.basename(__file__)[:-1],)

# globals
#env.user = 'abc'
home_dir = '/home/%s' % env.user 
root_dir = 'uts'

class G(object): #Global ENV
    is_load = False
    root = None
    project_root = None
    project_env_root = None
    virtualenv_name = None
    virtualenv_pkg_list = None
    virtualenv_root = None
    node_modules_root = None

    online_root = None
    history_dir = None
    package_dir = None
    resource_dir = None
    config_dir = None
    upload_dir = None
    log_dir = None

    bundle_name = 'utsEnv.pybundle'

def set_env(root):
    if G.is_load:
        return
    G.root = root if root else root_dir
    G.project_root = os.path.join(home_dir, G.root) #项目根目录
    G.project_env_root = os.path.join(G.project_root, 'env')
    
    G.virtualenv_name = 'py_venv'
    G.virtualenv_pkg_list = 'requirements.txt'
    G.virtualenv_root = os.path.join(G.project_env_root, G.virtualenv_name) #virtual env 目录
    G.history_dir = os.path.join(G.project_env_root, 'history')
    G.package_dir = os.path.join(G.project_env_root, 'package')
    G.upload_dir = os.path.join(G.project_env_root, 'upload')
    G.log_dir = os.path.join(G.project_env_root, 'logs')

    G.node_modules_root = os.path.join(G.project_env_root, 'node_modules') #node module 目录
    
    G.online_root = os.path.join(G.project_root, 'online')
    G.code_dir = os.path.join(G.online_root, 'current')
    G.resource_dir = os.path.join(G.online_root, 'www')
    G.config_dir = os.path.join(G.online_root, 'config')
    G.is_load = True


# tasks

@task
def setup(root=None):
    '''
    setup a new env, install package, create folder
    '''
    set_env(root)
    setup_pyenv()
    setup_install_pkg()
    setup_online()

#@task
def setup_pyenv(root=None):
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """
    set_env(root)
    sudo('apt-get update')
    sudo('apt-get install -y supervisor')
    sudo('apt-get install -y python-dev')
    sudo('apt-get install -y libevent-dev')
    sudo('apt-get install -y python-setuptools')
    sudo('apt-get install -y git-core')
    sudo('apt-get install -y p7zip-full')
    sudo('apt-get install -y libxml2-dev libxslt-dev')
    sudo('apt-get install -y nginx')

    #install nodejs
    with settings(warn_only=True):
        if not run('command -v nodejs'):
            sudo('apt-get install -y python-software-properties python g++ make')
            sudo('add-apt-repository ppa:chris-lea/node.js')
            sudo('apt-get update')
            sudo('apt-get install -y nodejs')

    sudo('easy_install pip')
    sudo('pip install virtualenv')
    run('[ -d %s ] || mkdir -p %s' % (G.project_env_root, G.project_env_root))
    with cd(G.project_env_root):
        run("[ -d %s ] || virtualenv --distribute --python=python2.7 %s"%(G.virtualenv_name, G.virtualenv_name))

    run('mkdir -p %s' % G.history_dir)
    run('mkdir -p %s' % G.package_dir)
    run('mkdir -p %s' % G.upload_dir)
    run('mkdir -p %s' % G.log_dir)

#@task
def setup_install_pkg(root=None):
    '''
    install python pkg
    '''
    set_env(root)
    put(G.virtualenv_pkg_list, G.project_env_root)
    if os.path.exists(G.bundle_name):
        put(G.bundle_name, G.project_env_root)
        run('%s/bin/pip install %s' % (G.virtualenv_root, os.path.join(G.project_env_root, G.bundle_name)))
    else:
        run('%s/bin/pip install -r %s --download-cache=pip_cache' % (G.virtualenv_root, os.path.join(G.project_env_root, G.virtualenv_pkg_list)))

    with cd(G.project_env_root):
        run("npm install grunt-cli")
        run("npm install grunt --save-dev")

#@task
def setup_online(root=None):
    set_env(root)
    run('mkdir -p %s' % G.online_root)
    run('mkdir -p %s' % G.resource_dir)
    run('mkdir -p %s' % G.config_dir)
    run('mkdir -p %s' % os.path.join(G.config_dir, 'supervisor'))
    run('mkdir -p %s' % os.path.join(G.config_dir, 'nginx'))
    run('mkdir -p %s' % os.path.join(G.config_dir, 'mongodb'))
    run('mkdir -p %s' % os.path.join(G.config_dir, 'settings'))

    with cd(G.resource_dir):
        run('rm -f static && ln -s %s static' % os.path.join(G.code_dir, 'srv/uts/collectstatic/static'))
        run('rm -f client && ln -s %s client' % os.path.join(G.code_dir, 'client'))
        run('rm -f custom && ln -s %s custom' % os.path.join(G.code_dir, 'custom'))
        run('rm -f ata && ln -s %s ata' % os.path.join(G.code_dir, 'uts_ata'))
        run('rm -f casic && ln -s %s casic' % os.path.join(G.code_dir, 'uts_casic'))
        run('rm -f cmbc && ln -s %s cmbc' % os.path.join(G.code_dir, 'uts_cmbc'))
        run('rm -f ericsson && ln -s %s ericsson' % os.path.join(G.code_dir, 'uts_ericsson'))
        run('rm -f huawei && ln -s %s huawei' % os.path.join(G.code_dir, 'uts_huawei'))
        run('rm -f public && ln -s %s public' % os.path.join(G.code_dir, 'uts_public'))

@task
def tar(version=None):
    "create a source package to local filesystem"
    if version is None:
        head_version = local("ver=`git log | head -n 1 | awk '{print $2}' | cut -c -7`; echo $ver;", capture=True )
        local("rm -rf /var/tmp/%(version)s && git archive --format=tar --prefix=%(version)s/%(version)s/ %(version)s | (cd /var/tmp/ && tar xf -) && echo %(version)s > /var/tmp/%(version)s/%(version)s/version.txt && 7z a %(version)s.7z /var/tmp/%(version)s/* && rm -rf /var/tmp/%(version)s" % {'version':head_version})
        print (green("file package success! %s.7z" %(head_version,)))
    else:
        local("rm -rf /var/tmp/%(version)s && git archive --format=tar --prefix=%(version)s/%(version)s/ %(version)s | (cd /var/tmp/ && tar xf -) && echo %(version)s > /var/tmp/%(version)s/%(version)s/version.txt && 7z a %(version)s.7z /var/tmp/%(version)s/* && rm -rf /var/tmp/%(version)s" % {'version':version})
        print (green("file package success! %s.7z" %(version,)))

@task
def bundle():
    '''
    create a pip bundle for package install
    '''
    if not os.path.exists(G.bundle_name):
        print green('beging create pip bundle %s' % G.bundle_name)
        local("pip bundle %s -r requirements.txt --download-cache=pip_cache" % G.bundle_name)

@task
def deploy(tar, root=None):
    '''
    deploy a tar to server
    '''
    set_env(root)
    stop()
    deploy_update(tar)
    print green("deploy successed!")

@task
def stop(root=None):
    set_env(root)
    sudo('supervisorctl stop all')

@task
def rebuild(root=None):
    '''
    rebuild js and local settings link, recollcet django static
    '''
    set_env(root)
    buildjs()

    with cd(G.online_root):
        with cd('current/srv/uts'):
            run('rm -rf logs && ln -s %s logs' % G.log_dir)
            run('rm -f upload && ln -s %s upload' % G.upload_dir)
            with settings(warn_only=True):
                run('''
                rm -f uts_site/localsettings.py && 
                [ -f %s/settings/localsettings.py ] && 
                ln -s %s/settings/localsettings.py uts_site/localsettings.py
                ''' % (G.config_dir, G.config_dir))

    with cd(os.path.join(G.online_root, 'current/srv/uts')):
        run('%s/bin/python manage.py collectstatic --no-post-process --noinput > /dev/null' % G.virtualenv_root)
    print green("django static build completed!")

#@task
def buildjs(root=None):
    set_env(root)
    print red('make sure your server.address and codemap.js is right and in right place, if not, modify it and call buildjs again')
    with cd(G.online_root):
        with cd('current'):
            SERVER_ADDRESS = run('read line < ../config/settings/server.address; echo $line;', shell=True)
            run('''sed -i 's/\(data_service_host :\)\(.*\)/\\1\"%s\"/g' client/app/coffee/config.coffee''' % SERVER_ADDRESS.replace('/', '\/'))
            run('''sed -i 's/\(debug :\)\(.*\)/\\1 false/g' client/app/coffee/config.coffee''')

            run('rm -f node_modules && ln -s %s node_modules' % G.node_modules_root)
            run('npm install --save-dev')
            run('./node_modules/grunt-cli/bin/grunt default:client/')
            with settings(warn_only=True):
                run('[ -r ../config/settings/codemap.js ] && cp -f ../config/settings/codemap.js client/app/public/js/')
                result = run('[ -f ../config/settings/codemap.js ]')
                if result.failed:
                    print ("codemap.js " + red("Not Exists and Not Replace!!!"))
                else:
                    print ("codemap.js " + green("Replace") + " with config/settings/codemap.js")

def deploy_update(tar):
    #TODO
    put(tar, G.package_dir)
    run("7z x -o%s %s > /dev/null" % (G.online_root, os.path.join(G.package_dir, tar)))
    print green("Unpackage completed!")
    with cd(G.online_root):
        import time
        now = time.strftime('%Y%m%d%H%M%S')
        run('''if [ -d current ]
               then
               mv current %s
               fi''' % os.path.join(G.history_dir, now))

        run('mv %s current' %  tar[:-3])

    rebuild()


@task
def start(root=None):
    set_env(root)
    with cd('/etc/supervisor/conf.d/'):
        sudo('rm -f uts.conf && ln -s %s/supervisor/uts.conf uts.conf' % G.config_dir)
    sudo('supervisorctl update')
    sudo('supervisorctl start all')

    with cd('/etc/nginx/sites-enabled/'):
        sudo('rm -f uts_nginx.conf && ln -s %s/nginx/uts_nginx.conf uts_nginx.conf' % G.config_dir)
    sudo('nginx -s reload')

@task
def restart(root=None):
    set_env(root)
    stop()
    start()
