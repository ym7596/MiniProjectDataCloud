
import urllib.request
import config   
import pandas as pd
from bs4 import BeautifulSoup
import os

def makeURL(sNode, search_text ):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.xml" % sNode
    parameters = "?query=%s" %  urllib.parse.quote( search_text )
    url = base + node + parameters
    return url

def requestURL(url):
    req = urllib.request.Request(url)  
    
    req.add_header("X-Naver-Client-Id", config.client_id)  # open api 키를 header에 추가
    req.add_header("X-Naver-Client-Secret", config.client_secret)  # open api 키를 header에 추가
    try:
        response = urllib.request.urlopen(req) 
        if response.status == 200 : 
            # print("Url Request Success")
            data = response.read().decode('utf-8')
            return data 
    except Exception as e:
        print(e)
        print("Error for URL : %s" %url) 
        return None
    
    
def searchText(text):
    sNode = 'news'
    search_text = text

    targetUrl = makeURL(sNode, search_text)
    data = requestURL(targetUrl)
    
    bs = BeautifulSoup(data, "lxml")
    list = bs.find_all('item')

    return list


def removeTag(n):
    n = n.replace('<b>','').replace('</b>','').replace('&lt;','<').replace('&gt;','>').replace('&quot;', '')
    return n


def searchResult(list):
    title = []
    link = []
    pubDate = []

    for item in list:
        temp_title = (item.find('title')).get_text()
        temp_link = (item.find('originallink')).get_text()
        temp_pubDate = (item.find('pubdate')).get_text()
        title.append(removeTag(temp_title))
        link.append(removeTag(temp_link))

    # 각각 리스트로 반환 = 인덱스 번호순으로 대응 title[0] - link[0]
    return title, link

# 사용 예시
# def main():
#     list = searchText('삼성전자')
#     title, link = searchResult(list)
#     return title, link

# title, link = main()
