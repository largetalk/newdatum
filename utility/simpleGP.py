#!/usr/bin/env python
import sys

import time
import json
import urllib2



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

    print price
    
    #print('id: %s, %s, c: %r, t: %s' % (id, name, price, t))


if len(sys.argv) <= 1:
    print 'input code'
    exit(-1)
else:
    print_current_price(sys.argv[1])
