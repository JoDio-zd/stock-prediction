# 股市分析
import requests
import re
f = open('stock.txt', mode='a')
# 东方财富网分析得到api
# 分析其接口后可以发现其拥有更加方便的爬取操作
# 通过调整pn可以改变初始页，改变pz可以改变总数据值
res =  requests.get('http://31.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1_11&pn=1&pz=4000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=160')
res.encoding = 'utf-8'
print(res.text, file = f)
print(type(res.text))
res.close()
f.close()