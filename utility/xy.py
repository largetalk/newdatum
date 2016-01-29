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
    if id.startswith('00') or id.startswith('15') or id.startswith('16'):
        id = 'sz' + id
    elif id.startswith('60') or id.startswith('510'):
        id = 'sh' + id
    url = url_head + id
    content = urlopen(url).read()
    data = content.split(",")
    name = data[0].split('"')[1]
    name = name.decode('gbk')
    price = data[3]
    t = data[31]

    return price
    
    #print('id: %s, %s, c: %r, t: %s' % (id, name, price, t))


ct = float(print_current_price('600674'))
xy = float(print_current_price('601166'))
print 'ct:', ct, ' xy:', xy, ' cost:', (ct-9.49)*1700 - (xy-15.92)*1000 
