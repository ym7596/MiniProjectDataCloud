import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import font_manager,rc
import platform
imgpath = 'D:\pythonfile\imgs'

def MachineLr(path,day,price):
    path = imgpath #테스트용
    # day = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30
    #             ,31,32,33,34,35,36,37,38,39,40])
    # price = np.array([72300,71300,74400,75800,75600,76300,77400,77400,78200,76900,76800,77000,77600,77800,78000
    #                 ,77100,78100,79400,79900,80500,80200,80300,78800,78300,78600,78700,77400,76900,78300,78000
    #                 ,78900,78900,77900,77300,77500,77000,76300,76300,76500,75600])

    t_input,te_input,t_target,te_target = train_test_split(day,price,random_state=20)
    t_input = t_input.reshape(-1,1)
    te_input = te_input.reshape(-1,1)
    t_p = np.column_stack((t_input ** 2,t_input))
    te_p = np.column_stack((te_input ** 2,te_input))
    lr = LinearRegression()

    lr.fit(t_p,t_target)
    predic = lr.predict([[91**2,91]])
    coe = lr.coef_
    inter= lr.intercept_

    point = np.arange(1,91)
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
    plt.scatter(41,predic,marker='^',color="red")
    plt.xlabel('day')
    plt.ylabel('price')
    #plt.figure(figsize=(3, 2),dpi=200)
    plt.savefig(path + '\\' + 'img.png')
    plt.show(block=False)
    plt.pause(3)
    plt.close()
#MachineLr(imgpath)