import gevent
from gevent import monkey;monkey.patch_all()
from gevent.pool import Pool
import urllib2, urllib, sys
import json
import random
import cookielib

pool_num = 5 
request_time = 10
log_file = open('spider.log', 'a')

host = "http://172.16.21.39:8999"
extern_header = {'content-type': 'application/json', 'Authorization': 'Basic YWRhcHRpdmU6YWRhcHRpdmU=', 'User-Agent': 'Mozilla/5.0 (Ubuntu; X11; Linux i686; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'}
subject_form = None
def gen_taker():
    url = host + '/external/takers/1/'
    rn = str(random.randint(1000, 999999999))
    candidate_id = "spider_"+rn
    data = [{ "candidate_id": candidate_id, "identify_id" : "spider_" + rn, "name": "spider", "gender": "M"}]
    data_json = json.dumps(data)
    req = urllib2.Request(url, data_json, extern_header)
    req.get_method= lambda: 'POST'
    response_stream = urllib2.urlopen(req, timeout=5)
    if response_stream.code == 200:
        return candidate_id
    else:
        return gen_taker()

def get_subject_form():
    def get_r_s_f(sf):
        s = sf[random.randint(0,len(sf)-1)]
        f = s['forms'][random.randint(0,len(s['forms'])-1)]
        return s['id'], f['id']
    if subject_form:
        return get_r_s_f(subject_form)
    global subject_form
    url = host+'/external/formlist/1/'
    req=urllib2.Request(url, headers=extern_header)
    resp = urllib2.urlopen(req)
    data = resp.read()
    subject_form = json.loads(data)
    return get_r_s_f(subject_form)

def gen_schedule():
    url = host+'/external/jobs/1/'
    candidate_id = gen_taker()
    subject, form = get_subject_form()
    data = {'spiderjob':[{"candidate_id": candidate_id, "permission_id": candidate_id, "password": 'www', "subject_id": subject, "form_id": form, "begin_time":"2011-01-01:0:0", "expire_time":"2013-01-01:0:0"}]}
    #print data
    data_json = json.dumps(data)
    req = urllib2.Request(url, data_json, extern_header)
    req.get_method= lambda: 'POST'
    response_stream = urllib2.urlopen(req, timeout=5)
    if response_stream.code == 200:
        return candidate_id, 'www'
    else:
        return None, None

def login(user, passwd):
    post_url = host + '/exam/login/'
    get_url = host + "/exam/?project_id=1"
    code_url = host + "/exam/validate_code/"

    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    req = urllib2.Request(code_url)
    conn = opener.open(req)
    codes = '0000'
    fl=conn.headers["set-cookie"].find("validate_code=") 
    if fl != -1:
        codes = conn.headers['set-cookie'][fl+14: fl+18]
    post_data=(("admission",user), ("password", passwd), ("validate_code", codes), ("project_id", 1))
    req = urllib2.Request(post_url, urllib.urlencode(post_data))
    conn = opener.open(req)
    opener.close()
    if conn.code == 200:
        return cookies
    else:
        return None

def login_confirm(cokie):
    confirm_url = host + '/exam/login_confirm/'
    opener = urllib2.build_opener(cokie)
    req = urllib2.Request(confirm_url, urllib.urlencode(()))
    conn = opener.open(req)
    opener.close()

def begin_exam(cokie):
    begin_url = host + '/exam/begin/'
    opener = urllib2.build_opener(cokie)
    req = urllib2.Request(begin_url)
    conn = opener.open(req)
    opener.close()

def next_exam(cokie, end=False):
    url = host + '/exam/page/'
    opener = urllib2.build_opener(cokie)
    if end:
        data = (("navigate", "end"),)
    else:
        data = (("navigate","next"),("response_1", "C"))
    req = urllib2.Request(url, urllib.urlencode(data))
    conn = opener.open(req)
    opener.close()

def exam_one_time():
    try:
        admission, passwd = gen_schedule()
        if admission is None:
            print >> log_file,  "can't generate test schedule"
            return
        cokie = login(admission, passwd)
        if cokie is None:
            print >> log_file, "can't login"
            return
        login_confirm(cokie)
        begin_exam(cokie)
        for x in xrange(20):
            next_exam(cokie)
        next_exam(cokie, True) 
        print 'SUCCESS request with', admission
    except BaseException, e:
        print >> log_file, "%s"%e
        print 'FAILED'

def main():
    pool = Pool(pool_num)
    for i in xrange(request_time):
        pool.spawn(exam_one_time)
    pool.join()

if __name__ == '__main__':
    main()
