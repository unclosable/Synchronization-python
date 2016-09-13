from TestPackage.FileReader import FileReaderClass
from dbAction.MySQLConnect import MySQL, Insert

file = FileReaderClass('/Users/zhengwei/Desktop/test2.json')

datas = file.eachData()
print(len(datas))

insert = Insert("INSERT INTO merchant(id,name,code,province_id,city_id,is_deleted)",
                ['ID', 'MERCHANTNAME', 'MERCHANTCODE', 'PROVINCEID', 'CITYID', 'ISDELETED'])

strsql = insert.getSQLByList(datas=datas)
print(strsql)

# 本地测试
db = MySQL(host="127.0.0.1", user="root", passwd="root", db="eyes")

# 正式数据库
# db = MySQL(host="10.230.3.92", port=8088, user="eyes_prog", passwd="3FDEF8AED7DD6E43E3", db="eyes")

# 测试数据库
# db = MySQL(host="10.3.47.82", port=3308, user="eyes", passwd="eyes", db="eyes")

re = db.cursor(strsql)
