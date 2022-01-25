from xml.etree.ElementInclude import include
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import font_manager,rc
import platform
imgpath = './imgs'

def MachineLr(path,day,price):
    path = imgpath #테스트용
    # day = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30
    #             ,31,32,33,34,35,36,37,38,39,40])
    # price = np.array([72300,71300,74400,75800,75600,76300,77400,77400,78200,76900,76800,77000,77600,77800,78000
    #                 ,77100,78100,79400,79900,80500,80200,80300,78800,78300,78600,78700,77400,76900,78300,78000
    #                 ,78900,78900,77900,77300,77500,77000,76300,76300,76500,75600])
    #price = np.array([80400.0, 81200.0, 80800.0, 79900.0, 79400.0, 79700.0, 79800.0, 79500.0, 80600.0, 79800.0, 79000.0, 79000.0, 78500.0, 79700.0, 79300.0, 78800.0, 78500.0, 79200.0, 79000.0, 78500.0, 79300.0, 81400.0, 82900.0, 82100.0, 81500.0, 81500.0, 80200.0, 78500.0, 77000.0, 74400.0, 74200.0, 73900.0, 73100.0, 72700.0, 73300.0, 75600.0, 75700.0, 74600.0, 74300.0, 74600.0, 76700.0, 76800.0, 76000.0, 76600.0, 77300.0, 76100.0, 76300.0, 75300.0, 75300.0, 76300.0, 76600.0, 77000.0, 76100.0, 77200.0, 77400.0, 77300.0, 77700.0, 76300.0, 74100.0, 74100.0, 73200.0, 72200.0, 71300.0, 71600.0, 71500.0, 69000.0, 68800.0, 69400.0, 70100.0, 70200.0, 70600.0, 70300.0, 70200.0, 70400.0, 70200.0, 71100.0, 70100.0, 70700.0, 69800.0, 69900.0, 71500.0, 70400.0, 70600.0, 70200.0, 70600.0, 70500.0, 70200.0, 69900.0, 70600.0, 71400.0, 71300.0, 70700.0, 70200.0, 71200.0, 74900.0, 75300.0, 74800.0, 73700.0, 72300.0, 72300.0, 71300.0, 74400.0, 75800.0, 75600.0, 76300.0, 77400.0, 77400.0, 78200.0, 76900.0, 76800.0, 77000.0, 77600.0, 77800.0, 78000.0, 77100.0, 78100.0, 79400.0, 79900.0, 80500.0, 80200.0, 80300.0, 78800.0, 78300.0, 78600.0, 78700.0, 77400.0, 76900.0, 78300.0, 78000.0, 78900.0, 78900.0, 77900.0, 77300.0, 77500.0, 77000.0, 76300.0, 76500.0, 75600.0, 75100.0, 74000.0])
    
    a= len(price)
    numlist = [i for i in range(a)]
    numlist = np.array(numlist)
    price = np.array(price)
    day = np.array(day)
    #day = numlist
    print(numlist)
    print(price)
    t_input,te_input,t_target,te_target = train_test_split(numlist,price,random_state=20)
    t_input = t_input.reshape(-1,1)
    te_input = te_input.reshape(-1,1)
    t_p = np.column_stack((t_input ** 2,t_input))
    te_p = np.column_stack((te_input ** 2,te_input))



   
    lr = LinearRegression()

    lr.fit(t_p,t_target)
    predic = lr.predict([[(a+2)**2,a+2]])
    coe = lr.coef_
    inter= lr.intercept_

    point = np.arange(1,a+2)
    plt.style.use(['dark_background'])
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
    
    
    plt.figure(figsize=(6,4),dpi=100,edgecolor='green',linewidth=2)
    plt.scatter(t_input,t_target,color='limegreen')
    plt.plot(point,coe[0]*point**2+coe[1]*point+inter)

    plt.title("이평선 기준 일별 주가 예측")
    plt.scatter(a+2,predic,marker='^',color="red")
    plt.xlabel('day')
    plt.ylabel('price')
    #plt.figure(figsize=(3, 2),dpi=200)
    plt.savefig(path + '\\' + 'img.png')
    plt.show(block=False)
    plt.pause(3)
    plt.close()
#MachineLr(imgpath)