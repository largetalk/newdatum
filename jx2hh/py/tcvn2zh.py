#coding:utf8
import os, sys
import subprocess
import io
import re
from translate import Translator
from googletrans import Translator as GTranslator
import youdao_trans as YDTranslator


MS_TRANSLATOR=Translator(from_lang="vi",to_lang="chinese")
YN_PATTERN = re.compile(ur'[\u1e00-\u1eff]+')

GOO_TRANSLATOR = GTranslator(service_urls=[
    'translate.google.cn',
    #'translate.google.com',
])

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
    for root, dirs, files  in os.walk(base_dir):
        for filename in files:
            if filename.endswith('.lua'):
                luaFn = os.path.join(root, filename)
                print luaFn
                u8Fn = iconv(luaFn)
                transFile(u8Fn)
                

def transFile(inFile, outFile=None):
    if outFile is None:
        outFile = inFile + '.ts'
    if os.path.exists(outFile):
        return
    fw = io.open(outFile, 'w', encoding='utf8')
    with io.open(inFile, 'r', encoding='utf8') as fin:
        for line in fin:
            if line.strip().startswith('--') or line.find('"') == -1:
                fw.write(line)
                continue
            sentList = extractTCVN(line)
            for sentence, isTcvn in sentList:
                if not isTcvn:
                    fw.write(sentence)
                    continue
                trans = transSentence(sentence)
                if trans is None or trans == sentence:
                    print(u"trans error:%s" % sentence)
                    fw.write(sentence)
                else:
                    fw.write(trans)
    fw.close()

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


def transSentence(sentence, translator=GOO_TRANSLATOR):
    #### 
    #youdao translate
    return YDTranslator.translate(sentence)
    ####
    #google translate
    #try:
    #    trans = translator.translate(sentence, src='vi', dest='zh-CN')
    #    if trans.text is not None and len(trans.text.strip()) > 1:
    #        return trans.text
    #    return None
    #except KeyboardInterrupt, ex:
    #    raise ex
    #except BaseException, ex:
    #    print(ex)
    #    return None
    ####
    #microsoft translate
    #translation = translator.translate(sentence)
    #if translation is None or len(translation) < 1:
    #    return None
    #return translation


if __name__ == '__main__':
    fp = '/Users/largetalk/Downloads/jx2JQ/gs/script/qixi07/baihua_npc.lua'
    #ufp = iconv(fp)
    ufp = '/Users/largetalk/Downloads/jx2JQ/gs/script/qixi07/baihua_npc.lua.u8'
    line = u'''		"Ta muốn nhận hạt giống hoa hồng và Hạt Thần bí/get_seed",'''
    l58 = u'''^I^ITalk(1,"","Trên người bạn không có hạt giống thần kỳ và hoa thần kỳ!");'''
    #sl = extractTCVN(l58)
    #transFile(ufp)
    root = '/Users/largetalk/Downloads/jx2JQ/gs/script/'
    walk_lua(root)
