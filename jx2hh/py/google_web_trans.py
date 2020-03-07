#coding:utf8
import os
import requests
import urllib
from bs4 import BeautifulSoup

URL = 'https://translate.google.cn/#view=home&op=translate&sl=vi&tl=zh-CN&text={}'

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.text
    except:
        print("Get HTML Text Failed!")
        return 0

def translate(sentence):
    print type(sentence)
    url = URL.format(urllib.quote(sentence))
    print url
    html = getHTMLText(url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        print soup

    try:
        result = soup.find_all("span", {"class":"tlid-translation"})[0].text
        print result
    except:
        print("Translation Failed!")
        result = ""

    return result


if __name__ == '__main__':
    line = '''Ta muốn nhận hạt giống hoa hồng và Hạt Thần bí'''
    translate(line)
