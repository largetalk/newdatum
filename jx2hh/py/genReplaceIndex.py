#coding:utf8
import os, sys
import io


#################
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
            dic[k] = v
    return dic

def replaceIndex(inFile, dic):
    outFile = os.path.join(os.path.dirname(inFile), 'tcvn_replace.txt')
    fw = io.open(outFile, 'w', encoding='utf8')
    with io.open(inFile, 'r', encoding='utf8') as fr:
        for line in fr:
            fw.write(line)
            if line.startswith('filename'):
                continue
            fidx = line.find(':')
            sidx = line.find(':', fidx+1)
            tcvn = line[sidx+1:].strip()
            zh = dic.get(tcvn, '')
            fw.write(u'zh: %s\n' % zh)
    fw.close()

if __name__ == '__main__':
    tcvn_file = '/Users/largetalk/git/jx2local/script/fetch_tcvn.txt'
    dic_file = '/Users/largetalk/git/jx2local/tcvn2zh.txt'
    dic = loadDic(dic_file)
    replaceIndex(tcvn_file, dic)
