import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import seaborn as sns
from matplotlib import font_manager,rc
import platform
import matplotlib


def calc_score(calc):

    for name in score_df.종목명:
        a = int(score_df.loc[score_df.종목명 == name, 'score'])
        b = int(calc.loc[calc.종목명 == name, 'score'])
        a = a + b
        
        score_df.loc[score_df.종목명 == name, 'score'] = a
    
def per(testdata):

    per = np.array(testdata['현재가']/testdata['주당순이익'])
    calc = pd.DataFrame({
        '종목명': testdata['종목명'],
        'per': per,
        '현재가':testdata['현재가'],
        '주당순이익':testdata['주당순이익']
        })
    
    calc = calc.sort_values(by='per',ascending = False)
    calc = calc.reset_index()
    
    temp = calc.copy()
    temp = temp.sort_values(by='per')
    temp = temp.reset_index()
    temp = temp[:6]

    plt.figure(figsize=(4,2.5),dpi=100)
    plt.title("적정주가 분석 - PER")
    sns.scatterplot(temp['현재가'], temp['주당순이익'], hue = temp['종목명'])

    x = [i for i in range(int(temp['현재가'].min()), int(temp['현재가'].max()))]
    y = [(1/10)*i for i in range(int(temp['현재가'].min()), int(temp['현재가'].max()))]
    plt.plot(x,y,'r--',lw = 1)
    
    plt.savefig('./imgs/per.png')
    #plt.show()
    plt.close()
    score = []
    s = -1
    for i in range(len(calc)):
        if calc['per'][i] > 10:
            s = -1
            score.append(s)
        else:
            s = s+1
            score.append(s)
    calc["score"] = pd.Series(score)
    
    calc_score(calc)

def eps(testdata):
    eps = np.array(testdata['주당순이익'])
    calc = pd.DataFrame({
        '종목명': testdata['종목명'],
        'eps': eps*10 - testdata['현재가']
        })
    
    calc = calc.sort_values(by='eps')
    calc = calc.reset_index()
    
    temp = calc.copy()
    temp = temp.sort_values(by='eps', ascending = False)
    temp = temp.reset_index()
    temp = temp[:6]
    
    plt.figure(figsize=(4,2.5),dpi=100)
    plt.title("적정주가 분석 - EPS")
    plt.bar(temp['종목명'], temp['eps'], width=0.8)
    plt.savefig('./imgs/eps.png')
    #plt.show()
    
    plt.close()
    score = []
    s = -1
    for i in range(len(calc)):
        s = s+1
        score.append(s)
    
    calc["score"] = pd.Series(score)
    
    calc_score(calc)
    
def graph01(testdata):
    #PBR
    eps = np.array(testdata['주당순이익'])
    price = np.array(testdata['현재가'])
    roe = np.array(testdata['ROE'])
    
    calc = pd.DataFrame({
        '종목명': testdata['종목명'],
        'PER': price/eps,
        'PBR': price/eps * roe/100,
        'ROE':testdata['ROE']
        })
    
    calc = calc.sort_values(by='PBR', ascending = False)
    calc = calc.reset_index()
    
    temp = calc.copy()
    temp = temp.sort_values(by='PBR')
    temp = temp.reset_index()
    temp = temp[:6]
    
    plt.figure(figsize=(4,2.5),dpi=100)
    plt.title("적정주가 분석 - PBR")
    sns.scatterplot(temp['PER'], temp['ROE'], hue = temp['종목명'])
    plt.savefig('./imgs/pbr.png')
    #plt.show()
    plt.close()
    score = []
    s = -1
    for i in range(len(calc)):
        if calc['PBR'][i] > 1:
            s = -1
            score.append(s)
        else:
            s = s+1
            score.append(s)
            
        
    calc["score"] = pd.Series(score)
    
    calc_score(calc)

def graph02(testdata):
    #EPS * ROE
    eps = np.array(testdata['주당순이익'])
    roe = np.array(testdata['ROE'])
    
    calc = pd.DataFrame({
        '종목명': testdata['종목명'],
        'eps*roe': eps*roe - testdata['현재가'],
        '주당순이익': testdata['주당순이익'],
        'ROE': testdata['ROE']
        })
    
    calc = calc.sort_values(by='eps*roe')
    calc = calc.reset_index()
    
    temp = calc.copy()
    temp = temp.sort_values(by='eps*roe', ascending = False)
    temp = temp.reset_index()
    temp = temp[:6]
    
    plt.figure(figsize=(4,2.5),dpi=100)
    plt.title("적정주가 분석 - EPS * ROE")
    sns.scatterplot(temp['주당순이익'], temp['ROE'], hue = temp['종목명'])
    plt.savefig('./imgs/epsroe.png')
    #plt.show()
    plt.close()
    score = []
    s = -1
    for i in range(len(calc)):
        s = s+1
        score.append(s)
    
    calc["score"] = pd.Series(score)
    
    calc_score(calc)

def total(score_df):
    
    score_df = score_df.sort_values(by='score',ascending = False)
    score_df = score_df.reset_index()
    
    plt.figure(figsize=(4,2.5),dpi=100)
    plt.title("분석 결과")
    plt.bar(score_df['종목명'][:6], score_df['score'][:6], width=0.8)
    plt.ylabel("총점")
    plt.savefig('./imgs/total.png')
    #plt.show()
    plt.close()
    return score_df[:6]

def drawdata(data): ##메인 
    font_path = ''
    if platform.system() == 'Windows':
        font_path = 'C:/Windows/Fonts/malgun.ttf'
        font_name = font_manager.FontProperties(fname = font_path).get_name()
        rc('font',family = font_name)
    elif platform.system() == 'Darwin':
        font_path = '/Users/$USER/Library/Fonts/AppleGothic.ttf'
        rc('font',family = 'AppleGothic')
    else:
        print('Check your OS System')
    # font_location = "c:/Windows/fonts/malgun.ttf"
    # font_name = font_manager.FontProperties(fname=font_location).get_name()
    # matplotlib.rc('font', family=font_name)
    # matplotlib.rcParams['axes.unicode_minus'] = False
    # print('오류검사2')
    # get_ipython().run_line_magic('matplotlib', 'inline')
    # print('오류검사2')
    global score_df
    score = [0 for i in range(len(data))]
    score_df = pd.DataFrame({
            '종목명': data['종목명'],
            'score': score
            })
    
    if not(os.path.isdir("./imgs")):
        os.mkdir("imgs")
    per(data)
    eps(data)
    graph01(data)
    graph02(data)
    
    a = total(score_df)
    listt = []
    for i in range(6):
        listt.append(a['종목명'][i])
        

    b = data[data["종목명"].isin(listt)].copy()
    sorterIndex = dict(zip(listt, range(len(listt))))
    b['sorter'] = b['종목명'].map(sorterIndex)
    b.sort_values('sorter',inplace=True)
    b.drop('sorter', 1, inplace = True)
    
    b = b.reset_index()
    b.drop('index', 1, inplace = True)
    
    a = b['종목명'][0]
    
    return a, b

