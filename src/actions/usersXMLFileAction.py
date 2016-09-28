from TestPackage.XMLFileReader import FileReaderClass
from TestPackage.Handler import Handler
from dbAction.MySQLConnect import MySQL, Insert, Update, UpdateOrInsert

file = FileReaderClass('/Users/zhengwei/Desktop/xmlTest2.xml')

datas = file.readDatas(keys=['EMPLOYEEID', 'EMPLOYEENAME', 'STATIONID', 'CREATETIME', 'UPDATETIME', 'ISDELETED'],
                       handler={
                           'EMPLOYEENAME': Handler['sqlBUG'],
                           'EMPLOYEEID': Handler['stringnumberTOnumenr'],
                           'STATIONID': Handler['stringnumberTOnumenr'],
                           'CREATETIME':Handler['stringdatedefault'],
                           'UPDATETIME':Handler['stringdatedefault']
                       })

# 本地测试
# db = MySQL(host="127.0.0.1", user="root", passwd="root", db="eyes")

# 正式数据库
# db = MySQL(host="10.230.3.92", port=8088, user="eyes_prog", passwd="3FDEF8AED7DD6E43E3", db="eyes")

# 测试数据库
db = MySQL(host="10.3.47.82", port=3308, user="eyes", passwd="eyes", db="eyes")

insert = Insert("INSERT INTO users(id,name,department_id,created_at,updated_at,is_deleted)",
                ['EMPLOYEEID', 'EMPLOYEENAME', 'STATIONID', 'CREATETIME', 'UPDATETIME', 'ISDELETED'])

# 空表导入
dataLen = len(datas)
start = 0
end = 1000
while dataLen > 0:
    if end < dataLen:
        sql = insert.getSQLByList(datas[start:end])
        # print(sql)
        try:
            db.cursor(sql)
        except Exception as e:
            print(e)
            # print(sql)
        start = end
        end += 1000
    else:
        sql = insert.getSQLByList(datas[start:dataLen])
        # print(sql)
        try:
            db.cursor(sql)
        except Exception as e:
            print(e)
            # print(sql)
        dataLen = -1

# update = Update(tableName="users",
#                 set={"EMPLOYEENAME": "name",
#                      "STATIONID": "department_id",
#                      "CREATETIME": "created_at",
#                      "UPDATETIME": "updated_at",
#                      "ISDELETED": "is_deleted"},
#                 where=" id=${EMPLOYEEID}")
#
# UpdateOrInsert = UpdateOrInsert(insert, update, query="SELECT * FROM users WHERE id=${EMPLOYEEID}", db=db)
#
# UpdateOrInsert.pushDatas(datas)
