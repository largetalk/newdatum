#coding:utf8
import os, sys
import io
import subprocess
import tarfile
from datetime import datetime


#################
#tcvn replace index description
#filename: /Users/largetalk/git/jx2Local/script/体服指引(正式服要删除).lua
#line5: 13: <color=green>Hướng dẫn:<color>
#zh: 红色的小于color = green >指引:红色;rolelabel color >
#line12: 4: Gia nhập môn phái
#zh: 加入部落

REPLACE = True
REPLACE_ALL = True
EXEC_ICONV = True
TAR_FILE = True


def actualFileName(fn, old_base, base):
    if fn.startswith('filename:'):
        fn = fn[10:]
    if not fn.startswith(old_base):
        print 'error fn', fn
        sys.exit(-1)
        return fn
    name = fn[len(old_base):]
    if name.startswith("/"):
        name = name[1:]
    return os.path.join(base, name)

def updateFile(fw, data):
    if fw is None:
        return
    for l in data:
        fw.write(l)
    fw.truncate()
    fw.close()
    #sys.exit()


def replace(indexFile, old_base, base):
    filename = None
    fw = None
    data = None
    old_lc = 0
    gap = 0
    not_replaced = 0
    replaced = 0
    with io.open(indexFile, 'r', encoding='utf8') as fr:
        while True:
            line = fr.readline()
            if line == '':
                updateFile(fw, data)
                break
            if line.startswith('filename'):
                updateFile(fw, data)
                filename = actualFileName(line.strip(), old_base, base)
                fw = None
                old_lc = 0
                continue
            if fw is None:
                fw = io.open(filename,'rb+')
                #fw = io.open(filename,'rb+',encoding="utf-8")
                data = fw.readlines()
                fw.seek(0)
            if line.startswith('line'):
                fidx = line.find(":")
                lc = int(line[4:fidx])
                sidx = line.find(':', fidx+1)
                pos = int(line[fidx+2:sidx])
                if lc == old_lc:
                    #print 'gap', gap
                    pos += gap
                else:
                    gap = 0
                tcvn = line[sidx+2:].rstrip()
                zhline = fr.readline()
                zh = zhline[4:].strip()
                if zh == '':
                    if REPLACE_ALL:
                        zh = u'中文中文'
                    else:
                        not_replaced += 1
                        continue
                curLine = data[lc-1].decode('utf8')

                if curLine[pos:pos+len(tcvn)] != tcvn:
                    print 'fetch tcvn error', filename, lc, pos, line
                    print curLine
                    print tcvn, len(tcvn)
                    print data[lc-1][pos:pos+len(tcvn)], len(data[lc-1][pos:pos+len(tcvn)])
                    break
                    #if curLine[pos:len(zh)] == zh: #for reprocess
                    #    print 'already replace', filename, line
                    #    gap += len(zh) - len(tcvn)
                    #else:
                    #    print 'fetch tcvn error', filename, lc, pos, line, curLine
                    #    #print tcvn, len(tcvn)
                    #    #print data[lc-1][pos:pos+len(tcvn)], len(data[lc-1][pos:pos+len(tcvn)])
                    #    break
                else:
                    replaced += 1
                    #data[lc-1] = curLine.replace(tcvn, zh, 1).encode('utf8')
                    data[lc-1] = u''.join([ curLine[:pos], zh, curLine[pos+len(tcvn): ] ]).encode('utf8')
                    old_lc = lc
                    gap += len(zh) - len(tcvn)
                    #print zh, type(zh), len(zh), tcvn, type(tcvn), len(tcvn)
                    #print data[lc-1]
    print 'replaced', replaced, 'not_replaced', not_replaced

def main(indexFile, old_base, base):
    if REPLACE:
        replace(indexFile, old_base, base)
    if EXEC_ICONV:
        walk_lua(base)
    if TAR_FILE:
        tardir(base)

def tardir(base_dir):
    base_dir = os.path.abspath(base_dir)
    dirname = os.path.dirname(base_dir)
    t = datetime.now().strftime("%m%d%H")
    tf = tarfile.open(name=os.path.join(dirname, 'script_%s.tar.gz' % t), mode='w:gz')

    for root, dirs, files  in os.walk(base_dir):
        for filename in files:
            luaFn = os.path.join(root, filename)
            arcFn = luaFn.replace(dirname, '').decode('utf8').encode('gb18030')
            tf.add(name=luaFn, arcname=arcFn, recursive=False)
    tf.close()


def iconvAndmv(inFile, from_code='utf8', outFile=None):
    if outFile is None:
        outFile = inFile + '.gb'
    if not os.path.exists(outFile):
        with open(outFile, 'wb') as fout:
            ret = subprocess.call(['iconv', '-f', from_code, '-t', 'gb18030', inFile], stdout=fout)
            print('iconv %s return %s' % (inFile, ret))

    ret = subprocess.call(['mv', outFile, inFile])
    print('mv %s %s return %s' % (outFile, inFile, ret))
    return inFile


def walk_lua(base_dir):
    base_dir = os.path.abspath(base_dir)
    for root, dirs, files  in os.walk(base_dir):
        for filename in files:
            if filename.endswith('.lua'):
                luaFn = os.path.join(root, filename)
                u8Fn = iconvAndmv(luaFn)

if __name__ == '__main__':
    replace_file = '/Users/largetalk/git/jx2local/script/tcvn_replace.txt'
    old_base = '/Users/largetalk/git/jx2local/script'
    base = '/Users/largetalk/git/jx2local/script'
    main(replace_file, old_base, base)
