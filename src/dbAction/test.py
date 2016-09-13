'''
Created on 2016年9月9日

@author: zhengwei
'''
from MySQLConnect import Update, MySQL

up = Update(insertStr="INSERT INTO test(name,part,pay)", dataIndex=['name', 'part', 'pay'])

strsql = up.getSQLByList(
    [{'name': '测试名称1', 'part': [1, 2, 3], 'pay': '321'}, {'name': '测试名称2', 'part': '测试分组', 'pay': '321'}])

print(strsql)

db = MySQL(host="127.0.0.1", user="root", passwd="root", db="test")

re = db.cursor(strsql)

print(re['cur'])
print(re['response'])


re = db.cursor("select * from test")

print(re['cur'])
print(re['response'])

for data in re['cur']:
    print(data)
    # for column in data:
    #     if type(column) is str:
    #         print(column)

db.clossConn()
