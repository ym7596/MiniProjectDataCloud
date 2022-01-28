import urllib.request
from bs4 import BeautifulSoup
import time
import pandas as pd
import selenium
from selenium import webdriver

##################################################################

def get_items(prod_items):
    prod_data = []
    # 배열이 들어갈 리스트 prod_data
    for prod_item in prod_items:
        
        print('테스트 오류 검사')
        try:
            name = prod_item.select('td')[0].text.strip().replace('*', '')
        except:
            name = ''
        try:
            price = prod_item.select('td')[2].text.strip()
        except:
            price = '0'
        try:
            yes = prod_item.select('td')[3].text.strip()
        except:
            yes = '0'
        try:
            updown = prod_item.select('td')[4].text.strip()
        except:
            updown = '0'
        try:
            siga = prod_item.select('td')[5].text.strip()
        except:
            siga = '0'
        try:
            asset_total = prod_item.select('td')[6].text.strip()
        except:
            asset_total = '0'
        try:
            bprofits = prod_item.select('td')[7].text.strip()
        except:
            bprofits = '0'
        try:
            jprofits = prod_item.select('td')[8].text.strip()
        except:
            jprofits = '0'
        try:
            bprofitsPercents = prod_item.select('td')[9].text.strip()
        except:
            bprofitsPercents = '0'
        try:
            roe = prod_item.select('td')[10].text.strip()
        except:
            roe = '0'
        try:
            why = prod_item.select('td')[1].text.strip().replace("테마 편입 사유", '')
        except:
            why = ''
        prod_data.append([name, price, yes, updown, siga, asset_total, bprofits, jprofits, bprofitsPercents, roe, why])

    
    return prod_data
    

def thema_option(driver):
    time.sleep(1)
    # 체크박스 초기화
    driver.find_element_by_xpath('''//*[@id="contentarea"]/div[3]/form/div/div/div/a[2]''').click()

    org_op_list = ['option1', 'option2', 'option8', 'option3', 'option9']
    check_op_list = ['option4', 'option5', 'option10', 'option11', 'option12', 'option23']

    # 체크박스 체크된 것 풀기 1, 2, 8, 3, 9
    for i in org_op_list:
        driver.find_element_by_id(i).click()
    
    # 옵션 지정: 4-시가총액, 5-영업이익, 10-자산총계, 11-영업이익증가율, 12-주당순이익, 23-roe 
    for i in check_op_list:
        driver.find_element_by_id(i).click()

    # 옵션 적용하기
    driver.find_element_by_xpath('''//*[@id="contentarea"]/div[3]/form/div/div/div/a[1]''').click()
    

def thema_to_list(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 종목명 현재가 등 열명
    title_list = soup.select('table.type_5 > thead > tr > th')

    # 종목 list로 받기
    items = soup.select('table.type_5 > tbody > tr')
    
    title = []
    for i in title_list:
        title.append(i.text)

    title.remove('토론실')
    title.append('테마 편입 사유')
    
    return items, title


# 종목 테마 리스트 뽑기
def get_thema_list(soup):
    link_list = []
    i = 0 
    for link in soup.select('table.type_1 > tbody > tr > td.col_type1 > a'):
        str = link.get('href')
        link_list.append(f'https://finance.naver.com{str}')
        if(i == 4):
            break
        i = i + 1
    return link_list

# 테마 이름, 전일대비증감율, 최근 3일 등락율
def get_theme_info():
    driver = webdriver.Chrome('chromedriver')

    # 크롬으로 네이버 테마별 시세 페이지 접속
    driver.get("https://finance.naver.com/sise/theme.naver")

    # 현재 페이지 소스 얻어오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    thema_title = []
    list1 = []
    list2 = []
    
    i = 0
    for item in soup.select('table.type_1 > tbody > tr > td.col_type1'):
        str = item.get_text()
        thema_title.append(str)
        if(i == 4):
            break
        i = i + 1
        
    i = 0
    for item in soup.select('table.type_1 > tbody > tr > td.number.col_type2 > span'):
        str = item.get_text().replace('\n', '').replace('\t', '').replace('%', '')
        list1.append(str)
        if(i == 4):
            break
        i = i + 1
    
    i = 0
    for item in soup.select('table.type_1 > tbody > tr > td.number.col_type3 > span'):
        str = item.get_text().replace('\n', '').replace('\t', '').replace('%', '')
        list2.append(str)
        if(i == 4):
            break
        i = i + 1
        
    thema_df = pd.DataFrame({'테마명': thema_title, '전일대비': list1, '최근 3일 등락률': list2})
    # print(thema_df)
    driver.close()
    # 일단 df로 반환
    return thema_df
        
    
# obj -> float
def obj_to_float(data):
    emp = []

    # 현재가부터 ROE까지
    for i in range(1, 8):
        str = data.columns[i]
        rq = []
        for j in data[str]:
            try:
                if ',' in j:
                    j = j.replace(',', '')
                    rq.append(float(j))
                else:
                    rq.append(float(j))
            except:
                rq.append(0)
        emp.append(rq)


    # 각 열에 값 대입
    for i in range(1, 8):
        str = data.columns[i]
        data[str] = emp[i-1]
        
    return data
        
def dropduplicate(df):
    df_new = df.dropna(how = 'any')
    df_new = df_new.drop_duplicates("종목명")
    
    return df_new

def crawling(): #메인 호출
    driver = webdriver.Chrome('chromedriver')

    # 크롬으로 네이버 테마별 시세 페이지 접속
    driver.get("https://finance.naver.com/sise/theme.naver")

    # 현재 페이지 소스 얻어오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # 테마 리스트
    thema_list = get_thema_list(soup)
    
    # 빈 데이터 프레임 생성
    df = pd.DataFrame()
    
    # 상위 테마 5개 돌리기
    for url in thema_list:
        driver.get(url)

        # 옵션 선택
        thema_option(driver)

        # 테마 item이랑 타이틀 가져오기
        items, title = thema_to_list(driver)

        # item 가져온 거 리스트화
        prod_data_fin = get_items(items)

        # 마지막 의미 없는 값 제거
        del prod_data_fin[-1]
        del prod_data_fin[-1]

        # 리스트 -> df
        data = pd.DataFrame(prod_data_fin)
        data.columns = title
        data.drop(columns=['전일비', '등락률'], inplace=True)
        df = pd.concat([df, data])

        time.sleep(1.5)

    df.dropna(how='any', inplace=True)
    df = obj_to_float(df)
    df.reset_index(drop=True, inplace=True)
    
    df = dropduplicate(df)
    
    return df

