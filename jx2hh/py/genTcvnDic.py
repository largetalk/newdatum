#coding:utf8
import os, sys
import subprocess
import io
import re
from collections import defaultdict
from translate import Translator
#from googletrans import Translator as GTranslator
import youdao_trans as YDTranslator


MS_TRANSLATOR=Translator(from_lang="vi",to_lang="chinese")
YN_PATTERN = re.compile(ur'[\u1e00-\u1eff]+')

DELIMTER = u' || '

#GOO_TRANSLATOR = GTranslator(service_urls=[
#    'translate.google.cn',
#    #'translate.google.com',
#])

def iconv(inFile, from_code='tcvn', outFile=None):
    if outFile is None:
        outFile = inFile + '.u8'
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
    fw = io.open(os.path.join(base_dir, 'tcvn_dic.txt'), 'w', encoding='utf8')
    tcvn2zh_dic = defaultdict(lambda: set())
    for root, dirs, files  in os.walk(base_dir):
        for filename in files:
            if filename.endswith('.lua.u8'):
                u8Fn = os.path.join(root, filename)
                tsFn = u8Fn + ".ts"
                if not os.path.exists(tsFn):
                    continue

                #fw.write(u'filename: ')
                #fw.write(u8Fn.decode('utf8'))
                #fw.write(u'\n')
                transFile(u8Fn, tsFn, fw, tcvn2zh_dic)
    fw.close()
                
    fsw = io.open(os.path.join(base_dir, 'tcvn_set.txt'), 'w', encoding='utf8')
    for k, sets in tcvn2zh_dic.items():
        #if len(sets) == 1:
        #    continue
        fsw.write(u'tcvn: ')
        fsw.write(k)
        fsw.write(u'\n')
        #fsw.write(DELIMTER)
        for w in sets:
            fsw.write(w)
            fsw.write(u'\n')
    fsw.close()

notFirst = 0
def transFile(u8Fn, tsFn, fw, transSet):
    global notFirst
    with io.open(u8Fn, 'r', encoding='utf8') as u8fr:
        with io.open(tsFn, 'r', encoding='utf8') as tsfr:
            lCount = 0
            while True:
                lCount += 1
                u8Line = u8fr.readline()
                tsLine = tsfr.readline()
                if u8Line == '':
                    break

                if u8Line.strip().startswith('Include(') or u8Line.strip().startswith('--') or u8Line.find('"') == -1:
                    continue

                sentList = extractTCVN(u8Line)
                firstSen = True
                for sentence, isTcvn in sentList:
                    if not isTcvn or '\\script\\' in sentence or '.wav' in sentence or '.mp3' in sentence:
                        continue
                    if firstSen:
                        fidx = u8Line.find(sentence)
                        eidx = findSmallIdx(tsLine, fidx + 1)
                        
                        #fw.write(u'line%s: %s %s ' % (lCount, fidx, eidx))
                        writeTrans(fw, sentence, tsLine[fidx:eidx], transSet)
                        firstSen = False
                    else:
                        trans = None
                        notFirst += 1
                        #print notFirst
                        #trans = transSentence(sentence)
                        if trans is not None and not trans.starswith('MYMEMORY WARNING'):
                            writeTrans(fw, sentence, trans, transSet)

def writeTrans(fw, sentence, trans, transSet):
    fw.write(sentence)
    fw.write(DELIMTER)
    fw.write(trans)
    fw.write(u'\n')
    transSet[sentence].add(trans)

def findSmallIdx(tsLine, fidx):
    a = tsLine.find(u'/', fidx)
    b = tsLine.find(u'"', fidx)
    if a == -1:
        return b
    if b == -1:
        return a
    if a < b:
        return a
    else:
        return b

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


def transSentence(sentence, translator=MS_TRANSLATOR):
    translation = translator.translate(sentence)
    if translation is None or len(translation) < 1:
        return None
    return translation


if __name__ == '__main__':
    root = '/home/arthur/material/jx2/script'
    #root = '/Users/largetalk/jx2hh/jx2JQ_youdao_trans/gs/script'
    walk_lua(root)
