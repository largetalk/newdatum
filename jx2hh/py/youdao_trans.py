# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import hashlib
import time
import time
import json

reload(sys)
sys.setdefaultencoding('utf-8')

YOUDAO_URL = 'https://openapi.youdao.com/api'
#wangzhiqing721
#APP_KEY = '27db2702aec50a50'
#APP_SECRET = 'EKtC1BI9lhUnyLcchuPC8Y6QgVtwX8nw'
#
#largetalkxyk
APP_KEY = '0ca13802af9c88a4'
APP_SECRET = 'aoYY69JBRduEMGrWIuidN3yChaDxm89v'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    q_utf8 = q.decode("utf-8")
    size = len(q_utf8)
    return q_utf8 if size <= 20 else q_utf8[0:10] + str(size) + q_utf8[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def translate(q):
    #q = u'''Ta muốn nhận hạt giống hoa hồng và Hạt Thần bí'''

    data = {}
    data['from'] = 'vi'
    data['to'] = 'zh-CHS'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        pass
        #millis = int(round(time.time() * 1000))
        #filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        #fo = open(filePath, 'wb')
        #fo.write(response.content)
        #fo.close()
    else:
        j = json.loads(response.content)
        if j['errorCode'] != '0':
            print(j)
            return None
        return j['translation'][0]


if __name__ == '__main__':
    q = u'''Ta muốn nhận hạt giống hoa hồng và Hạt Thần bí'''
    translate(q)
