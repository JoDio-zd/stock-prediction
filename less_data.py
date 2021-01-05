'''
对现有的logistic回归的一个小改造，
所考虑的问题是系数的变化
这是一个系数与时间有关的回归问题
'''
import pymysql.cursors
import numpy as np
import random

def logistic():
    connection = database()
    stock_id = get_id(connection)
    stock_id = random.sample(stock_id, 10)
    info = []
    theta = 1
    alpha = 0.01
    for i in stock_id:
        info.append(get_info_by_id(i['id'], connection))
    date_all = []
    delta_p = []
    y_ans = []
    for sample in info:
        date_ = []
        money = []
        if len(sample) > 1:
            for i in sample:
                date_.append(date_to_t(i['date_']))
                money.append(i['money'])
            date_ = np.array(date_)
            date_all.append(date_)
            for i in range(len(money) - 1):
                if i < len(money) - 2:
                    money[i] = float(money[i + 1]) - float(money[i])
                else:
                    y_ans.append(0 if float(money[i + 1]) - float(money[i]) < 0 else 1)
                    money[i] = float(money[i]) - float(money[i + 1])
                    money[i + 1] = 0
            money = np.array(money)    
            delta_p.append(money)
        else:
            continue
    y_ans = np.array(y_ans)
    del info
    while True:
        z = []
        zs_ = []
        for i in range(len(delta_p)):
            z_temp, zs_temp = zs(date_all[i], delta_p[i], theta)
            z.append(z_temp)
            zs_.append(zs_temp)
        z = np.array(z)
        zs_ = np.array(zs_)
        y_pred = sigmoid(z)
        theta1 = theta - alpha * 1 / (len(z)) * (y_pred - y_ans).dot(zs_)
        z = []
        for i in range(len(delta_p)):
            z_temp = zs(date_all[i], delta_p[i], theta1)[0]
            z.append(z_temp)
        z = np.array(z)
        y_pred1 = sigmoid(z)
        a = lost_function(y_ans, y_pred)
        b = lost_function(y_ans, y_pred1)
        theta = theta1
        if abs(a - b) < 0.1:
            if theta < 0:
                print('拟合失败')
                return 0
            n = 0
            for i in range(len(y_pred1)):
                if y_pred1[i] > 0.6:
                    y_pred1[i] = 1
                elif y_pred1[i] < 0.4:
                    y_pred1[i] = 0
            for i in range(len(y_pred1)):
                if y_pred1[i] == y_ans[i]:
                    n += 1
            print('正确率为：', n / (i + 1))
            print('theta=', theta)
            break

    connection.close()

def lost_function(y_test, y_pred):
    '''
    定义损失函数
    '''
    j = (1 / len(y_pred)) * np.sum(y_test * np.log(y_pred) + (1-y_test) * np.log(1 - y_pred))
    return j

def sigmoid(z):
    '''
    逻辑回归的激活函数
    '''
    y_pred = 1 / (1 + np.exp(-z))
    return y_pred

def zs(t, delta_p, theta = 1):
    '''
    此函数用来计算z
    之后代入sigmoid函数即可
    '''
    z = 0
    zs = 0
    z += np.sum(delta_p * f(t, theta))
    zs += np.sum(delta_p * theta * 1 / t * f(t, theta))
    # zs += np.sum(delta_p * t * f(t, theta))
    return z, zs

def date_to_t(date_):
    '''
    将日期转换成为我们所想要的t
    即转换成可计算的数值类
    '''
    date = date_.split('-')
    for i in range(len(date)):
        date[i] = int(date[i])
    t = date[0] -2010 + (date[1] - 1) / 12 + (date[2] - 1) / 31
    return t

def database():
    '''
    搭建数据库的连接
    '''
    connection = pymysql.connect(
        host='localhost',
        user='jodio',
        password='123456@Zz',
        db='stock',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
        )
    return connection

def get_id(connection):
    '''
    得到股票代码
    '''
    cs = connection.cursor()
    sql = 'select distinct id from stock'
    cs.execute(sql)
    stock_id = cs.fetchall()
    return stock_id

def get_info_by_id(stock_id, connection):
    '''
    这个函数的目的是通过股票的id
    来对同一只股票的数据进行提取
    '''
    cs = connection.cursor()
    sql = 'select date_, money from stock where id = %s' % stock_id
    cs.execute(sql)
    info = cs.fetchall()
    return info

def f(t, theta=1):
    '''
    所需要系数的形式
    我们就用反比例函数来试验好了
    '''
    ans = 1 / ((12 - t) ** theta)
    # ans = theta ** t
    return ans

if __name__ == '__main__':
    logistic()