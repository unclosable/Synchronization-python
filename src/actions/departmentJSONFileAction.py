from TestPackage.FileReader import FileReaderClass
from TestPackage.Handler import Handler
from dbAction.MySQLConnect import MySQL, Insert, Update, UpdateOrInsert

file = FileReaderClass('/Users/zhengwei/Desktop/test.json')

datas = file.eachData({
    'CREATED_AT': Handler['OracleDateToMySQLDate'],
    'UPDATED_AT': Handler['OracleDateToMySQLDate'],
    'CITY_ID': Handler['NoneDefaultInt'],
    'PARENTSORTINGCENTERID':Handler['sqlBUG']
})

print("共有［%d］条数据" % (len(datas)))

# 本地测试
# db = MySQL(host="127.0.0.1", user="root", passwd="root", db="eyes")

# 正式数据库
# db = MySQL(host="10.230.3.92", port=8088, user="eyes_prog", passwd="3FDEF8AED7DD6E43E3", db="eyes")

# 测试数据库
db = MySQL(host="10.3.47.82", port=3308, user="eyes", passwd="eyes", db="eyes")

insert = Insert(
    "INSERT INTO departments(id,name,dtype,created_at,updated_at,city_id,is_deleted,distribution_code,parent_sortings)",
    ['ID', 'NAME', 'DTYPE', 'CREATED_AT', 'UPDATED_AT', 'CITY_ID', 'ISDELETED', 'DISTRIBUTIONCODE',
     'PARENTSORTINGCENTERID'])

update = Update(tableName="departments",
                set={"NAME": "name",
                     "DTYPE": "dtype",
                     "CREATED_AT": "created_at",
                     "UPDATED_AT": "updated_at",
                     "CITY_ID": "city_id",
                     "ISDELETED": "is_deleted",
                     "DISTRIBUTIONCODE": "distribution_code",
                     "PARENTSORTINGCENTERID": "parent_sortings"},
                where=" id=${ID}")

UpdateOrInsert = UpdateOrInsert(insert, update, query="SELECT * FROM departments WHERE id=${ID}", db=db)

UpdateOrInsert.pushDatas(datas)

db.clossConn()
