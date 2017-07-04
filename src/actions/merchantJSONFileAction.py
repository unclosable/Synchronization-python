from TestPackage.FileReader import FileReaderClass
from dbAction.MySQLConnect import MySQL, Insert, Update, UpdateOrInsert

file = FileReaderClass('/Users/zhengwei/Desktop/test.json')

datas = file.eachData()
print(len(datas))

# 本地测试
# db = MySQL(host="127.0.0.1", user="root", passwd="root", db="eyes")

# 正式数据库
db = MySQL(host="10.230.3.92", port=8088, user="eyes_prog", passwd="3FDEF8AED7DD6E43E3", db="eyes")

# 测试数据库
# db = MySQL(host="10.3.47.82", port=3308, user="eyes", passwd="eyes", db="eyes")

insert = Insert("INSERT INTO merchant(id,name,code,province_id,city_id,is_deleted,once_import)",
                # ['ID', 'text', 'code', 'provinceid', 'cityid', 'isdeleted', 'isonceimport'])
                ['ID', 'MERCHANTNAME', 'MERCHANTCODE', 'PROVINCEID', 'CITYID', 'ISDELETED', 'ISONCEIMPORT'])
update = Update(tableName="merchant",
                set={"MERCHANTNAME": "name",
                     "MERCHANTCODE": "code",
                     "PROVINCEID": "province_id",
                     "CITYID": "city_id",
                     "ISDELETED": "is_deleted",
                     "ISONCEIMPORT": "once_import"},
                where=" id=${ID}")

UpdateOrInsert = UpdateOrInsert(insert, update, query="SELECT * FROM merchant WHERE id=${ID}", db=db)

UpdateOrInsert.pushDatas(datas)

db.clossConn()
