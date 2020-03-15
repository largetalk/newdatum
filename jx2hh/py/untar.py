#coding:utf8
import os, sys
import tarfile
import hashlib


base = '/Users/largetalk/jx2hh'

def untar(inFile):
    tf = tarfile.open(inFile, mode='r')
    members = tf.getmembers()
    for m in members:
        try:
            try:
                m.name.decode('utf8')
                name = m.name.decode('utf8').encode('raw_unicode_escape').decode('gb18030').encode('utf8')
                #print 'utf8-gb18030:', m.name, name
            except UnicodeDecodeError, ex:
                name = m.name.decode('gb18030').encode('utf8')
                #print 'gb18030:', m.name, name
        except UnicodeDecodeError, ex:
            print 'fatal error name:', m.name
            name = m.name
        if 'script' in name and m.name  != name:
            print 'origin', m.name
            print 'update', name
            print 'check', name.decode('utf8').encode('gb18030'), m.name == name.decode('utf8').encode('gb18030')
        mp = os.path.join(base, name)
        #print mp
        if not os.path.exists(os.path.dirname(mp)):
            os.makedirs(os.path.dirname(mp))
        if m.isdir():
            if not os.path.exists(mp):
                #print 'create Folder', mp
                os.makedirs(mp)
        elif m.isfile():
            if os.path.exists(mp):
                fr = tf.extractfile(m)
                if check_md5(mp, fr):
                    continue
                else:
                    mp = mp + '.1'
                    if os.path.exists(mp):
                        print mp
            fr = tf.extractfile(m)
            with open(mp, 'wb') as fw:
                while True:
                    data = fr.read(4096)
                    if not data:
                        break
                    fw.write(data)
                #for l in fr:
                #    fw.write(l)
        else:
            print 'error tarinfo', m

def check_md5(mp, fr):
    oldmd5 = get_file_md5(mp)
    m = hashlib.md5()   #创建md5对象
    while True:
        data = fr.read(4096)
        if not data:
            break
        m.update(data)
    newmd5 = m.hexdigest()
    fr.seek(0)
    return oldmd5 == newmd5

def get_file_md5(file_name):
    """
    计算文件的md5
    :param file_name:
    :return:
    """
    m = hashlib.md5()   #创建md5对象
    with open(file_name,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  #更新md5对象

    return m.hexdigest()    #返回md5对象

if __name__ == '__main__':
    #untar('/Users/largetalk/jx2hh/script.tar.gz')
    untar('/Users/largetalk/jx2hh/jx2JQ.tar.gz')
