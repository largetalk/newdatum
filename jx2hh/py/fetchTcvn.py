#coding:utf8
import os, sys
import subprocess
import io
import re


YN_PATTERN = re.compile(ur'[\u1e00-\u1eff]+')

def walk_lua(base_dir):
    base_dir = os.path.abspath(base_dir)
    fw = io.open(os.path.join(base_dir, 'fetch_tcvn.txt'), 'w', encoding='utf8')
    for root, dirs, files  in os.walk(base_dir):
        for filename in files:
            if filename.endswith('.lua'):
                luaFn = os.path.join(root, filename)
                print luaFn
                transFile(luaFn, fw)
    fw.close()
                

def transFile(inFile, fw):
    fw.write(u'filename: ')
    fw.write(inFile.decode('utf8'))
    fw.write(u'\n')
    with io.open(inFile, 'r', encoding='utf8') as fin:
        lcount = 0
        for line in fin:
            lcount += 1
            qIdx = line.find('"')
            cIdx = line.find('--')
            if qIdx == -1 or (cIdx != -1 and qIdx > cIdx):
                continue

            head = line
            if cIdx != -1:
                head = line[:cIdx]
            sentList = extractTCVN(head)
            sIdx = 0
            for sentence, isTcvn in sentList:
                if isTcvn:
                    fw.write(u"line%s: %s: %s\n" % (lcount, sIdx, sentence))
                sIdx += len(sentence)

def extractTCVN(line):
    if YN_PATTERN.search(line) is None:
        return [(line, False)]

    spl = line.split('"')
    ret = []
    for i in range(len(spl)):
        l = spl[i]
        if i%2 == 0:
            ret.append((l, False))
            continue
        ret.append((u'"', False))
        if len(l) < 1 or YN_PATTERN.search(l) is None:
            ret.append((l, False))
        else:
            iidx = l.find('/')
            if iidx != -1:
                ret.append((l[:iidx], True))
                ret.append((l[iidx:], False))
            else:
                ret.append((l, True))
        ret.append((u'"', False))
    return ret




if __name__ == '__main__':
    root = '/Users/largetalk/git/jx2Local/script/'
    walk_lua(root)
