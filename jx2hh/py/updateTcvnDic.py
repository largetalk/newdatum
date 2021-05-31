#coding:utf8
import os
import io
from translate import Translator


MS_TRANSLATOR=Translator(from_lang="vi",to_lang="chinese")

#########################
#origin tcvn index description
#filename: /Users/largetalk/git/jx2Local/script/体服指引(正式服要删除).lua
#line5: 13: <color=green>Hướng dẫn:<color>
#line12: 4: Gia nhập môn phái
#line16: 4: Nâng cao đẳng cấp chuyển sinh nhân vật

################
#tcvn2zh dic description
#tcvn: hồng hoang Ặ vô khởi Ặ vô diệt!
#红玫瑰，开始，结束，结束!
#tcvn: Hợp thành Tẩy Tâm Thạch cấp 2 = 4*1 cấp Tẩy Tâm Thạch + Băng Tinh Thạch
#二级洗心膏= 4*1级洗心膏+水晶粉
#tcvn: Người chơi
#玩家

def transSentence(sentence, translator=MS_TRANSLATOR):
    translation = translator.translate(sentence)
    if translation is None or len(translation) < 1:
        return None
    return translation

def loadDic(inFile):
    dic = {}
    with io.open(inFile, 'r', encoding='utf8') as fr:
        while True:
            tcvnLine = fr.readline()
            chLine = fr.readline()
            if tcvnLine == '' or chLine == '' or not tcvnLine.startswith("tcvn: "):
                break
            k = tcvnLine[6:].strip()
            v = chLine.strip()
            if v:
                dic[k] = v
    return dic


WRITE_EMPTY = False

def updateDic(tcvnFile, dicFile):
    dic = loadDic(dicFile)
    fw = io.open(dicFile, 'a+', encoding='utf8')
    MS_TRANS_FLAG = True
    with io.open(tcvnFile, 'r', encoding='utf8') as fr:
        for line in fr:
            if line.startswith('filename'):
                continue
            fidx = line.find(':')
            sidx = line.find(':', fidx+1)
            tcvn = line[sidx+1:].strip()
            if tcvn in dic:
                continue
            
            trans = None
            if MS_TRANS_FLAG:
                trans = transSentence(tcvn)
                if trans is None or trans.startswith('MYMEMORY WARNING'):
                    MS_TRANS_FLAG = False
                    trans = None

            dic[tcvn] = trans if trans is not None else ''
            if trans is not None or WRITE_EMPTY:
                fw.write(u'tcvn: ')
                fw.write(tcvn)
                fw.write(u'\n')
                if trans is not None:
                    fw.write(trans)
                fw.write(u'\n')
    fw.close()

if __name__ == '__main__':
    tcvn_file = '/Users/largetalk/git/jx2local/script/fetch_tcvn.txt'
    dic_file = '/Users/largetalk/git/jx2local/tcvn2zh.txt'
    updateDic(tcvn_file, dic_file)
    
