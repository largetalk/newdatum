#--coding:utf8--
import sys
import gevent
from gevent import monkey

monkey.patch_all()

shgps = ['sh601179', 'sh600219', 'sz000725', 'sz000728', 'sh601318', 'sh600362', 'sz000623']
url_head = 'http://hq.sinajs.cn/list='

if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib2 import urlopen

def print_current_price(id):
    url = url_head + id
    content = urlopen(url).read()
    data = content.split(",")
    name = data[0].split('"')[1]
    name = name.decode('gbk')
    price = data[3]
    t = data[31]
    
    print('id: %s, %s, c: %r, t: %s' % (id, name, price, t))

while(1):
    jobs = [gevent.spawn(print_current_price, id) for id in shgps]
    gevent.wait(jobs)
    gevent.sleep(5)
    print '############'
