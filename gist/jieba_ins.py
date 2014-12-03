#encoding:utf-8

import jieba

seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print "Full Mode:", "/ ".join(seg_list)  # 全模式

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print "Default Mode:", "/ ".join(seg_list)  # 精确模式

seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print ", ".join(seg_list)

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print ", ".join(seg_list)

data = open("mfbck.txt", 'rb').read()

seg_list = jieba.cut(data, cut_all=False, HMM=True)
print "Default Mode/HMM:", "/ ".join(seg_list) # 精确模式 & HMM

print '#################################'

import jieba.analyse

tags = jieba.analyse.extract_tags(data, topK=10, withWeight=True)

print "tags: "
for t in tags:
    print t[0], t[1]

print '#################################'

tags = jieba.analyse.textrank(data, withWeight=True)

print "text rank: "
for t in tags:
    print t[0], t[1]

print '#################################'

import jieba.posseg as pseg

words = pseg.cut(data)

for w in words:
    print w.word, w.flag
