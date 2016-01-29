#--coding:utf8--
import sys
import gevent
from gevent import monkey

monkey.patch_all()

import time
import json
import urllib2

REFER_URL = 'http://xueqiu.com/S/%s/GSJJ'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
COOKIE = "s=r9711ebjgl; bid=a035a6b006ec49f7f248a63a965693a9_igrppfx4; webp=1; snbim_minify=true; xq_a_token=fe77b3a0e8f0b7b99a66fd0b0d847ce2cc0146d5; xqat=fe77b3a0e8f0b7b99a66fd0b0d847ce2cc0146d5; xq_r_token=a6cc21a75c206257e9e5d43dc232ae6745201660; xq_is_login=1; u=2079082878; xq_token_expire=Fri%20Jan%2029%202016%2009%3A43%3A32%20GMT%2B0800%20(CST); __utmt=1; __utma=1.1085688491.1447034296.1451877159.1451888375.161; __utmb=1.1.10.1451888375; __utmc=1; __utmz=1.1448263777.36.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_1db88642e346389874251b5a1eded6e3=1451026184; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1451888375"
YI = 100000000

shgps = ['sz000002', 'sh601988', 'sh601318', 'sz000625', 'sh600518', 'sh600030', 'sh600000', 'sh601166']
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

def gtvsct():
    base_url = "http://xueqiu.com/v4/stock/quote.json?code=SH%s&_=%s"
    headers = {'User-Agent': UA, 'Referer': REFER_URL % 'SH600674', "Cookie": COOKIE}

    try:
        gt_url = base_url % (600886, time.time())
        ct_url = base_url % (600674, time.time())

        gt_req = urllib2.Request(gt_url, headers=headers)
        ct_req = urllib2.Request(ct_url, headers=headers)

        gt_resp = urllib2.urlopen(gt_req, timeout=10)
        ct_resp = urllib2.urlopen(ct_req, timeout=10)

        gt_data = gt_resp.read()
        ct_data = ct_resp.read()

        gt_json = json.loads(gt_data)
        ct_json = json.loads(ct_data)

        gt_fmc = eval(gt_json['SH600886']['float_market_capital'])
        ct_fmc = eval(ct_json['SH600674']['float_market_capital'])
        print 'gt: %.6s, ct: %.6s, gt - ct: %.6s ' % (gt_fmc/YI, ct_fmc/YI, (gt_fmc-ct_fmc)/YI),
        if ((gt_fmc-ct_fmc)/YI) >= 180 and ((gt_fmc-ct_fmc)/YI) <= 300:
            print 'suggest gt'
        else:
            print 'suggent ct'
    except Exception, e:
        print str(e)


while(1):
    jobs = [gevent.spawn(print_current_price, id) for id in shgps]
    jobs.append(gevent.spawn(gtvsct))
    gevent.wait(jobs)
    gevent.sleep(5)
    print '############'
