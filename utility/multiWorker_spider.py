#--coding:utf8--
import gevent
from gevent import monkey
#monkey.patch_all()

import os,sys
import time
import subprocess
import signal
from httplib import IncompleteRead
from gevent.pool import Pool
import gevent.socket as socket
from gevent.event import Event
from goose import Goose
from goose.configuration import Configuration
from goose.text import StopWordsChinese
import chardet
import random

goose_config = Configuration()
goose_config.enable_image_fetching = False
goose_config.browser_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/534.52.7 (KHTML, like Gecko) Version/5.1.2 Safari/534.52.7"
#goose_config.parser_class = 'soup'
goose_config.stopwords_class = StopWordsChinese

g = Goose(config=goose_config)

url_file = '/data/algorithm/urlcontent'

address = ('192.168.32.5', 10888)

class Worker(object):
    '''
    子进程运行的代码,通过起一个协程来和主进程通信
    包括接受任务分配请求，退出信号(零字节包)，及反馈任务执行进度
    然后主协程等待停止信号并中止进程(stop_event用于协程间同步)。
    '''
    def __init__(self, address):
        self.address = address
        self.stop_event = Event()

        self.wp = open('fetched_%s.txt' % os.getpid(), 'w')
        self.uf_url_p = open('unfetched_%s.txt' % os.getpid(), 'w')

        gevent.spawn(self.communicate)
        self.stop_event.wait()
        print 'worker(%s):will stop' % os.getpid()

    def exec_task(self, url):
        try:
            article = g.extract(url=url)
            title = article.title
            content = article.cleaned_text

            if content != None and len(content) > 0:
                self.wp.write( url )
                #self.wp.write( ' ' )
                #self.wp.write( title.replace(' ', '').replace('\n', '').encode('utf8') )
                self.wp.write( ' ' )
                self.wp.write( content.replace('\n', '').encode('utf8') )
                self.wp.write( '\n' )
            else:
                self.uf_url_p.write( url )
                self.uf_url_p.write( '\n' )
        except (TypeError, IncompleteRead, AttributeError), e:
            return

    def communicate(self):
        print 'worker(%s):started' % os.getpid()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(self.address)
        fp = client.makefile()
        while True:
            line = fp.readline()
            if not line:
                self.stop()
                self.stop_event.set()
                break
            '单独起一个协程去执行任务，防止通信协程阻塞'
            print 'sub process %s accept %s' % ( os.getpid(), line)
            gevent.spawn(self.exec_task, line.strip())
            gevent.sleep(0)

    def stop(self):
        self.wp.close()
        self.uf_url_p.close()

class Master():
    '''
    主进程运行代码,启动单独协程监听一个端口以供子进程连接和通信用，
    通过subprocess.Popen启动CPU个数个子进程,注册SIGTERM信号以便在
    KILL自己时通知子进程退出，主协程等待停止事件并退出主
    '''
    def __init__(self, address):
        self.address = address
        self.workers = []
        self.stop_event = Event()

        gevent.spawn(self.communicate)
        gevent.sleep(0) #让communicate协程有机会执行，否则子进程会先启动

        self.process = [subprocess.Popen(('python',sys.argv[0],'worker')) for i in xrange(12)] #启动multiprocessing.cpucount-1个子进程

        gevent.signal(signal.SIGTERM, self.stop) #拦截kill信号

        gevent.spawn(self.start) #分发任务

        self.stop_event.wait() 

    def communicate(self):
        print 'master(%s):started' % os.getpid()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(address)
        server.listen(1024)
        while True:
            worker, addr = server.accept()
            print 'master(%s):new worker' % os.getpid()
            self.workers.append(worker)

    def stop(self):
        print 'master stop'
        for worker in self.workers:
            worker.close()
        for p in self.process:
            p.wait()
        self.stop_event.set()

    def start(self):
        while not self.workers:
            gevent.sleep(1)
            continue

        with open(url_file, 'rb') as fp:
            line_count = 0
            t = time.time()
            for line in fp:
                url = line.split()[0]
                worker = random.choice(self.workers)
                worker.send(url + '\n')

                line_count += 1
                if line_count % 1000 == 0:
                    print 'process %s line used %s seconds' % (line_count, time.time() - t)
                    gevent.sleep(10)


if len(sys.argv) == 1:
    Master(address)
else:
    Worker(address)
