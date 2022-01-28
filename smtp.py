import smtplib
from email.message import EmailMessage

pw = 'elzmalbjtuytwzxs'

class gmail_sender:
    def __init__(self,sender_email,receiver_email,sender_passsword,cc_email='',bcc_email=''):
        self.s_email = sender_email
        self.r_email = receiver_email
        self.pw = sender_passsword
        self.server_name = 'smtp.gmail.com'
        self.server_port = 587

        self.msg = EmailMessage()
        self.msg["From"] = self.s_email
        self.msg["To"] = self.r_email
        if cc_email != '':
            self.cc_email = cc_email
            self.msg["Cc"] = self.cc_email
        if bcc_email != '':
            self.bcc_email = bcc_email
            self.msg["Bcc"] = self.bcc_email
        self.smtp = smtplib.SMTP(self.server_name,self.server_port)
    def msg_set(self,msg_title,msg_body):
        self.msg['Subject'] = msg_title
        self.msg.set_content(msg_body)
    def file_set(self,file):
        with open(file,"rb") as f:
            self.msg.add_attachment(f.read(),maintype ="xlsx",subtype="plain",filename='주식 분석 보고서.xlsx')
    def smtp_con_send(self):
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(self.s_email,self.pw)
        self.smtp.send_message(self.msg)

    def smtp_discon(self):
        self.smtp.close()

def sending(tL:list):
    rList = ''
    for i in tL:
        rList += i
        rList += ';'
    path = './주식 분석 보고서.xlsx'
    for i in range(len(tL)):
        test_e = gmail_sender('symbols25@gmail.com',tL.pop(0),pw)
        test_e.msg_set("Test_Title2","안녕하세요 테스트입니다..")
        test_e.file_set(path)
        test_e.smtp_con_send()
        test_e.smtp_discon()
            