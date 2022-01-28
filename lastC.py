import urllib.request
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
from selenium import webdriver
import requests

def LastCrolling(name:str):
    path = 'chromedriver.exe'
    driver = webdriver.Chrome(path)
    time.sleep(2)
    driver.get("https://finance.naver.com/sise/sise_group_detail.naver?type=theme&no=509")
    time.sleep(2)

    inputElement = driver.find_element_by_id("stock_items") 
    time.sleep(2)

    ffst = ''
    sstr = ''
    for i in name:
        if ffst == '':
            ffst = i
        else:
            sstr += i  
         
    inputElement.send_keys(ffst)
    time.sleep(1)
    inputElement.send_keys(sstr)
    time.sleep(1)

    #뒤에 공백이 입력되서 공백없애기
    name1=name.replace(" ","")
    time.sleep(1)

    #종목코드로 변환해서 검색하는부분
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #code = soup.find('span', class_="code").get_text() 
    page=1
    url = []
    code = 1
    # 값들 받아와서
    l = soup.findAll('div', {"class": "_au_full"})
    for i in l:
        #ex <title>lg<title>
        t = i.text.split() #t[0] = 종목코드, t[1] = 종목이름
        if( t[1] == name1.upper()): # 입력값과 같으면
            inputElement.clear()   # 원래 입력 제거
            #종목코드로보냄
            inputElement.send_keys(t[0]) #종목코드 입력
            inputElement.submit() #제출
            code=t[0] #종목코드 저장
            

    #종목코드를 이용하여 원하는 종목의 일별시세에 접속하여 url에 저장
    for i in range(1, 30):
        page = i
        url.append(f'https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}')

    #빈 데이터프레임 생성    
    df = pd.DataFrame() 

    for i in range(0, 29):
        req = requests.get(url[i], headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Max Os X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.9683.103 Safari/537.36'})
        temp = pd.read_html(req.text, encoding='utf-8')[0]
        df = pd.concat([df, temp])


    df.drop(df[df['날짜'].isna()].index, inplace=True)
    df=df.drop(['전일비','시가','고가','저가','거래량'],axis=1)
    df.reset_index(drop=True, inplace=True)
    b = df.loc[:,['종가']]
    a = df.loc[:,['날짜']]
    #b = df['종가']
    print(df.dtypes)
    b = b.astype('int32')
    a = a.astype('str')
    b = list(reversed(np.array(df['종가'].tolist())))
    a = list(reversed(np.array(df['날짜'].tolist())))
    listo = []
    listo.append(a)
    listo.append(b)
    print(a)
    print(b)
    driver.close()
    return listo
#LastCrolling('삼성전자')

        