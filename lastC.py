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

    #종목 검색창에 파라다이스를 입력하고 클릭 
    ffst = ''
    sstr = ''
    for i in name:
        if ffst == '':
            ffst = i
        else:
            sstr += i
    inputElement.send_keys(ffst)
    inputElement.send_keys(sstr)
    time.sleep(2)
    #xpath = """//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/button"""
    xpath = """//*[@id="atcmp"]/div/div/ul/li[1]/a"""
    driver.find_element_by_xpath(xpath).click()

    time.sleep(1)

    #종목코드 추출
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    code = soup.find('span', class_="code").get_text() 
    page=1
    url = []

    for i in range(1, 30):
        page = i
        url.append(f'https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}')
        
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