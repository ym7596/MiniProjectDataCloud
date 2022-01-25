import sys
import time

import smtp
import Linear
import lastC
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5 import uic



class testApp(QtWidgets.QDialog):
    model = QStandardItemModel()
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi('./TestGUI.ui',self)
        self.ui.show()
        self.pushButton.clicked.connect(self.buttonFunction)
    
    def imageadd(self):
        self.pixmapvar = QPixmap()
        self.pixmapvar.load('.\imgs\\img.png')
        self.pixmapvar = self.pixmapvar.scaledToWidth(600)
        self.lbPic.setPixmap(self.pixmapvar)
        #self.showList()
    def showList(self,txt):
        
        self.model.appendRow(QStandardItem(txt))
        self.ui.listView.setModel(self.model)
    def buttonFunction(self):
        self.IsbtnClicked()
        self.showList('버튼 연결')
        #time.sleep(100)
        main()
        #time.sleep(100)
        self.imageadd()
        self.IsbtnClickedAfter()
    def IsbtnClicked(self):
        self.pushButton.setDisabled(True)
    def IsbtnClickedAfter(self):
        self.pushButton.setEnabled(True)
def main():
    
    jongmok_name = '삼성전자'
    IsStart = True
    
    #머신러닝 모듈 임포트
    tmpp = LCrol(jongmok_name) #해당 종목의 날짜와 종가 numpy array 리스트 
    #Macine.MachineLr('D:\pythonfile\imgs')
    time.sleep(2)
    mc = Linear
    mc.MachineLr('./imgs',tmpp[0],tmpp[1])
    time.sleep(3)
    
   
    mm.showList('끝')

def LCrol(txt:str):
    lc = lastC
    tmp =  lc.LastCrolling(txt)
    return tmp


if __name__ == '__main__':
    IsStart = False
    app = QtWidgets.QApplication(sys.argv)
    mm= testApp()

    mm.showList('시작합니다.')
   
    mm.showList('머신러닝 모듈 완료...')
    smt=smtp
    #smtp모듈 임포트
    mm.showList('SMTP 모듈 완료...')
    sys.exit(app.exec())
    
    #메인 함수 시작 (크롤링 등)

    
    