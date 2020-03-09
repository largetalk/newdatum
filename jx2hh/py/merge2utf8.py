#coding:utf8
import os, sys
import subprocess
import io
import re


YN_PATTERN = re.compile(ur'[\u1e00-\u1eff]+')

CN_PATTERN = re.compile(r'[\u4e00-\u9fa5]+')


def iconv(inFile, from_code='tcvn', outFile=None):
    if outFile is None:
        outFile = inFile + '.tmp'
        #dn = os.path.dirname(inFile)
        #bn = os.path.basename(inFile)
        #outFile = os.path.join(dn, bn+'.u8')
        #print(outFile)
    if os.path.exists(outFile):
        return outFile
    with open(outFile, 'wb') as fout:
        ret = subprocess.call(['iconv', '-f', from_code, '-t', 'utf-8', inFile], stdout=fout)
        print('iconv %s return %s' % (inFile, ret))

    return outFile

def walk_lua(base_dir):
    base_dir = os.path.abspath(base_dir)
    for root, dirs, files  in os.walk(base_dir):
        for filename in files:
            if filename.endswith('.lua'):
                luaFn = os.path.join(root, filename)
                #print luaFn
                tmpFn = iconv(luaFn)
                mergeFile(luaFn, tmpFn)
                

def mergeFile(luaFn, tmpFn, outFile=None):
    if outFile is None:
        outFile = luaFn + '.u8'
    #if os.path.exists(outFile):
    #    return
    fw = io.open(outFile, 'w', encoding='utf8')
    with io.open(luaFn, 'rb') as luafr:
        with io.open(tmpFn, 'r', encoding='utf8') as tmpfr:
            lCount = 0
            while True:
                lCount += 1
                luaLine = luafr.readline()
                tmpLine = tmpfr.readline()
                if luaLine == '':
                    break

                if luaLine.strip().startswith('Include('): #process include script has chinese
                    try:
                        includeStr = luaLine.decode('gb18030')
                        fw.write(includeStr)
                        continue
                    except UnicodeError, ex:
                        print 'include error', luaLine

                if "\\script\\" in luaLine: #process as xxx yunanwen \\script\\chinese\\  yunanwen
                    try:
                        fw.write(luaLine.decode('gb18030'))
                        continue
                    except UnicodeError, ex:
                        pass
                    sluaidx = luaLine.find("\\script\\")
                    eludidx = luaLine.find('"', sluaidx)
                    stmpidx = tmpLine.find("\\script\\")
                    etmpidx = tmpLine.find('"', stmpidx)
                    try:
                        inStr = luaLine[sluaidx:eludidx].decode('gb18030')
                        fw.write(tmpLine[:stmpidx])
                        fw.write(inStr)
                        fw.write(tmpLine[etmpidx:])
                    except UnicodeError, ex:
                        print 'script error', luaLine
                        fw.write(luaLine)

                    continue


                if "\\sound\\" in luaLine or ".wav" in luaLine or ".mp3" in luaLine:
                    try:
                        includeStr = luaLine.decode('gb18030')
                        fw.write(includeStr)
                        continue
                    except UnicodeError, ex:
                        print 'sound error', luaLine

                #    print '####inline script', luaLine
                #    try:
                #        includeStr = luaLine.decode('gb18030')
                #        fw.write(includeStr)
                #        continue
                #    except UnicodeError, ex:
                #        print 'inline error', luaLine

                idx = luaLine.find('--')
                if idx == -1:
                    fw.write(tmpLine)
                    continue
                tmpIdx = tmpLine.find('--')
                head = tmpLine[:tmpIdx]
                tail = luaLine[idx:]
                try:
                    tail = tail.decode('gb18030')
                except UnicodeError, ex:
                    #print luaFn, 'line:', lCount
                    #print luaLine
                    #print ex
                    tail = tmpLine[tmpIdx:]

                fw.write(head)
                fw.write(tail)
    fw.close()





if __name__ == '__main__':
    root = '/Users/largetalk/git/jx2local/script/'
    walk_lua(root)
