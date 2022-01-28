import sys
import time
import asyncio



from sqlalchemy import false

import finance_crawling
import delzero
import data_analize
import index_crawling
import Top6DB
import writeexcell
import smtp
import Linear
import lastC
import news_crawling
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5 import uic
class Mail_Thread(QThread):
    sm = smtp
    
    def __init__(self, parent):
        super().__init__(parent)
        
    
class M_Thread(QThread):
    lc = lastC
    NC = news_crawling
    lr = Linear
    sm = smtp
    def __init__(self,parent):
        super().__init__(parent)
        
    def LCrol(self,txt:str):
        
        tmp =  self.lc.LastCrolling(txt)
        return tmp
        
    def SMTP_Start(self):
        pass
    def col(self,txt):
        print('들어옴2')
        return self.NC.main(txt)

    def Machine(self,path,tmp1,tmp2):
        self.lr.MachineLr(path,tmp1,tmp2)
        #nc = news_crawling
    def stop(self):
        self.quit()
        self.wait(2000)
    def EmailSend(self,elist):
        self.sm.sending(elist)    

class GUI_Function(QtWidgets.QDialog):
    model = QStandardItemModel()
    lc = lastC
    SM = smtp
    lr = Linear
    NC = news_crawling
    WriteX = writeexcell
    fn = finance_crawling
    da = data_analize
    dz = delzero
    ic = index_crawling
    T6 =Top6DB
    emailList = []
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./TestGUI.ui',self)
        self.ui.show()
        #self.brw.append('<a href="https://www.naver.com">테스트</a>')
        self.imageadd('default.png')
        self.pushButton.clicked.connect(self.buttonFunction)
        self.addBtn.clicked.connect(self.addButtonFunction)
    def addButtonFunction(self):
        self.emailList.append(self.textEdit.toPlainText())
        self.MailBr(self.textEdit.toPlainText())
        self.textEdit.clear()
        print(self.emailList)
    def TextBr(self,textList,htmlList):
        #self.brw =QtWidgets.QTextBrowser(self)
        self.brw.setAcceptRichText(True)
        self.brw.setOpenExternalLinks(True)

        for i in range(len(textList)):
            self.brw.append("<a href='"+str(htmlList[i])+"'>"+str(textList[i])+'</a>"')
    def MailBr(self,Address):
        self.emailB.setAcceptRichText(True)
        self.emailB.append(Address) 
    def SetLabel(self,name):
        self.BestNameLabel.setText(str(name))
    def imageadd(self,path):
        self.pixmapvar = QPixmap()
        self.pixmapvar.load('.\imgs\\'+path)
        #self.pixmapvar.load('.\imgs\\img.png')
        self.pixmapvar = self.pixmapvar.scaledToWidth(600)
        self.lbPic.setPixmap(self.pixmapvar)
        #self.showList()
    
    def showList(self,txt):
        
        self.model.appendRow(QStandardItem(txt))
        self.ui.listView.setModel(self.model)
        self.ui.listView.scrollToBottom()
    def buttonFunction(self):
        self.IsbtnClicked()
        self.showList('버튼 연결')
        #time.sleep(100)
        #self.x.start()
        
        self.main()
        
        #time.sleep(100)
        self.imageadd('img.png')
        self.IsbtnClickedAfter()
    def IsbtnClicked(self):
        self.pushButton.setDisabled(True)
    def IsbtnClickedAfter(self):
        self.pushButton.setEnabled(True)
    # 
    def main(self):


        DFTest = self.fn.crawling()
        DzResult = self.dz.delzero(DFTest)
        DA_Result = self.da.drawdata(DzResult)
        #종목이름(최우수),상위6개 데이터프레임

        #DB 쓰기
        self.T6.temp(DA_Result[1])



        testname = str(DA_Result[0])
        self.SetLabel(testname)
        self.showList('뉴스 검색 시작')
        x = M_Thread(self)
        n_title,n_link=x.col(testname)
        time.sleep(2)
        x.stop()
        self.showList('뉴스 검색 완료')
        
        

        jongmok_name = n_title
        j_link = n_link
        self.TextBr(n_title,n_link)
        time.sleep(2)
        #self.showList(str(n_title))
        #self.showList(str(n_link))
        #머신러닝 모듈 임포트
        self.showList('우수 종목 크롤링 시작')
        tmpp=x.LCrol(testname)
        time.sleep(2)
        x.stop()
        self.showList('우수 종목 크롤링 끝')
        
        time.sleep(2)
        
        self.showList('회귀 분석 시작')
        x.Machine('./imgs',tmpp[0],tmpp[1])
        time.sleep(2)
        x.stop()
        self.showList('회귀 분석 완료')
        
        a,b,c = self.ic.temp()
        #코스피 코스닥 코스피200

        Theme_List = self.fn.get_theme_info()
        self.WriteX.savepng(a,b,c,testname,Theme_List)
        time.sleep(3)
        
        x.EmailSend(self.emailList)
        self.showList('끝')



if __name__ == '__main__':
    IsStart = False
    app = QtWidgets.QApplication(sys.argv)
    mm= GUI_Function()

    mm.showList('시작합니다.')
   
   
    sys.exit(app.exec())
    #app.exec()
    #메인 함수 시작 (크롤링 등)

    
    