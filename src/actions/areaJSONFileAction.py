from TestPackage.FileReader import FileReaderClass
from TestPackage.Handler import Handler
from dbAction.MySQLConnect import MySQL, Insert, Update, UpdateOrInsert

file = FileReaderClass('/Users/zhengwei/Desktop/test2.json')

datas = file.eachData({
    'CREATED_AT': Handler['OracleDateToMySQLDate'],
    'UPDATED_AT': Handler['OracleDateToMySQLDate'],
    'CITY_ID': Handler['NoneDefaultInt']
})

print("共有［%d］条数据" % (len(datas)))

# 本地测试
# db = MySQL(host="127.0.0.1", user="root", passwd="root", db="eyes")

# 正式数据库
db = MySQL(host="10.230.3.92", port=8088, user="eyes_prog", passwd="3FDEF8AED7DD6E43E3", db="eyes")

# 测试数据库
# db = MySQL(host="10.3.47.82", port=3308, user="eyes", passwd="eyes", db="eyes")

insert = Insert("INSERT INTO area(id,name,city_id)",
                ['AREAID', 'AREANAME', 'CITYID'])

update = Update(tableName="area",
                set={"AREANAME": "name",
                     "CITYID": "city_id"},
                where=" id=${AREAID}")

UpdateOrInsert = UpdateOrInsert(insert, update, query="SELECT * FROM departments WHERE id=${AREAID}", db=db)

UpdateOrInsert.pushDatas(datas)

db.clossConn()