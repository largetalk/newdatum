#!/usr/bin/env python
import sys
import urllib
from xml.dom import minidom

if len(sys.argv) < 2:
    print 'Usage : dict word'
    exit(-1)

data = urllib.urlopen('http://dict-co.iciba.com/api/dictionary.php?w='+sys.argv[1])
#data = urllib.urlopen('http://dict.cn/ws.php?utf8=true&q='+sys.argv[1])

try:
    xml = minidom.parse(data)
    
    ps = xml.getElementsByTagName('ps')
    if len(ps) < 0 :ps = ps[0].firstChild.data
    else: ps =''
    acceptions = xml.getElementsByTagName('acceptation')
except xml.parsers.expat.ExpatError:
    ps = ''
    acceptions = []

#pron = xml.getElementsByTagName('pron')[0].firstChild.data
#defi = xml.getElementsByTagName('def')[0].firstChild.data


print sys.argv[1], '[ '+ ps +' ]'

for acceptation in acceptions:
    print acceptation.firstChild.data
