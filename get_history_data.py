import requests
import re
import pymysql.cursors
import pymysql
from threading import Thread
from fake_useragent import UserAgent

ua = UserAgent()
headers = { 'User-Agent':ua.random}

def hello_stock():
    cs = connection.cursor()
    sql1 = 'select * from stock_id'
    cs.execute(sql1)
    id_ = cs.fetchall()
    for idname in id_[1844:]: # id_从66开始，到4000结束
        url = 'http://quotes.money.163.com/trade/lsjysj_' + idname['id'] + '.html?'
        for year in range(2020, 2009, -1): # 2000-2021
            url1 = url + 'year=%d' % year
            for season in range(4, 0, -1):
                url2 = url1 + '&season=%d' % season
    # url = 'http://quotes.money.163.com/trade/lsjysj_600896.html?year=2018&season=4'

                req = requests.get(url2, headers = headers)
                req.encoding = 'utf8'
                res = re.compile(r'<td>(\d{4}-\d{2}-\d{2})</td>')
                date_ = re.findall(res, req.text)
                res = re.compile(r"<td class='\w*'>(-?\d*\.\d*)</td>")
                money = re.findall(res, req.text)
                if date_ == []:
                    break
                cs1 = connection.cursor()
                for i in range(len(date_)):
                    sql2 = 'insert into stock values ("{}", "{}", "{}")'.format(idname['id'], date_[i], money[i * 6 + 3])
                    cs1.execute(sql2)
                    connection.commit()

if __name__ == '__main__':

    connection = pymysql.connect(
            host='localhost',
            user='jodio',
            password='123456@Zz',
            db='stock',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
            )         
    hello_stock()
    
    connection.close()