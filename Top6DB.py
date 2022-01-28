import pymysql
from datetime import datetime
def temp(df):
	

	a="Today"
	a+=datetime.today().strftime('%Y-%m-%d')
	a= a.replace("-","_")

	conn = pymysql.connect(host='127.0.0.1', user='root', password='password',charset='utf8')
	curs = conn.cursor(pymysql.cursors.DictCursor)
	mk_database='create database if not exists 상위6개종목'
	curs.execute(mk_database)

	conn1 = pymysql.connect(host='127.0.0.1', user='root', password='password',db='상위6개종목',charset='utf8')
	curs1 = conn1.cursor(pymysql.cursors.DictCursor)
	mk_table = 'create table if not exists '+a+' (종목명 varchar(500),현재가 DECIMAL(20,3),시가총액 DECIMAL(30,3),자산총계 DECIMAL(30,3),영업이익 DECIMAL(30,3),주당순이익 DECIMAL(30,3),영업이익증가율 DECIMAL(20,3),ROE DECIMAL(20,3),테마편입사유 varchar(500)) '
	curs1.execute(mk_table)

	sql = "insert into "+a+" (종목명,현재가,시가총액,자산총계,영업이익,주당순이익,영업이익증가율,ROE,테마편입사유) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) "

	for idx in range(len(df)):
		curs1.execute(sql, tuple(df.values[idx]))
	conn1.commit()
	conn1.close() 

