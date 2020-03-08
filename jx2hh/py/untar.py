import os, sys
import tarfile


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
        #print '###', name
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
                continue
            fr = tf.extractfile(m)
            with open(mp, 'wb') as fw:
                for l in fr:
                    fw.write(l)
        else:
            print 'error tarinfo', m

if __name__ == '__main__':
    #untar('/Users/largetalk/jx2hh/script.tar.gz')
    untar('/Users/largetalk/jx2hh/jx2JQ.tar.gz')
