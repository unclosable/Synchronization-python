'''
Created on 2016年9月9日

@author: zhengwei
'''
from MySQLConnect import Update, MySQL, Insert, UpdateOrInsert

db = MySQL(host="127.0.0.1", user="root", passwd="root", db="test")

# ===insert测试===
insert = Insert(insertStr="INSERT INTO test(id,name,part,pay)", dataIndex=['id', 'name', 'part', 'pay'])
#
# strsql = insert.getSQLByList(
#     [{'name': '测试"名<$$$>\'称1', 'part': [1, 2, 3], 'pay': '321'}, {'name': '测试名称2', 'part': '测试分组', 'pay': '321'}])
#
# testOne = insert.getSQLByOne({'name': '测试"名<$$$>\'称1', 'part': [1, 2, 3], 'pay': '321'})
#
# re = db.cursor(strsql)
#
# print(re['cur'])
# print(re['response'])
#
# re = db.cursor(testOne)
#
# print(re['cur'])
# print(re['response'])

# ===update test===

update = Update(tableName='test',
                set={"name": "name",
                     "part": "part",
                     "pay": "pay"},
                where=" id=${id}")

# updateTest = update.getUpdateSQLByOne({'id': 131, 'name': '测1试"名<$$$>\'称1', 'part': [1, 2, 3], 'pay': '321'})
#
# print(updateTest)
# re = db.cursor(updateTest)
#
# print(re['cur'])
# print(re['response'])

updateORinsert = UpdateOrInsert(insert, update, "select * from test where id = ${id}", db)

updateORinsert.pushDatas([{'id': 131, 'name': '测1试111"名<$$$>\'称1', 'part': [1, 2, 3], 'pay': '321'},{'id': 141, 'name': '测1试111"名<$$$>\'称1', 'part': [1, 2, 3], 'pay': '321'}])

re = db.cursor("select * from test")

print(re['cur'])
print(re['response'])

for data in re['cur']:
    print(data)
# for column in data:
#     if type(column) is str:
#         print(column)

db.clossConn()
