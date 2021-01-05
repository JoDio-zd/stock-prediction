# 用来提取股票代码
# 将代码存入mysql中
import re
import pymysql.cursors
f = open('stock.txt', mode='r')
res = re.compile(r'"f12":"(\d*?)"')
ans = re.findall(res, f.read())
connection = pymysql.connect(
        host='localhost',
        user='jodio',
        password='123456@Zz',
        db='stock',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
        )
for i in ans:
    with connection.cursor() as cursor:
        sql = 'insert into stock_id values ("%s")' % i
        cursor.execute(sql)
        connection.commit()
f.close()
connection.close()