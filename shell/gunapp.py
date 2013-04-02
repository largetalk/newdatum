import os
#from kazoo.client import KazooClient
import zc.zk

zk = zc.zk.ZooKeeper('172.16.97.11:2181')
pid = os.getpid()
flag = False

@zk.properties('/new_test')
def data_update(data):
    global flag
    if flag:
        os.kill(pid, 1)
        #print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
    else:
        flag = True

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    yield 'Blocking on read(), pid is %s \n' % pid   
    if not os.path.exists('/tmp/my-fifo'):
        os.mkfifo('/tmp/my-fifo')
    fd = open('/tmp/my-fifo', 'r').read(1)
    yield 'Read done\n'
