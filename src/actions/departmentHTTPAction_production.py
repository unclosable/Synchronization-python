from httpAction.HttpConnect import HttpConnect
from dbAction.MySQLConnect import MySQL, Insert, Update, UpdateOrInsert
from TestPackage.Handler import Handler
import datetime


def action():
    conn = HttpConnect("pms-service.rfddc.com")

    departmentQueryStr = "/expresscompany/"

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:10]
    SixDaysAgo = (datetime.datetime.now() - datetime.timedelta(days=6))
    SixDaysAgo = SixDaysAgo.strftime("%Y-%m-%d %H:%M:%S")[:10]

    departmentQueryStr += SixDaysAgo + "/" + now
    response = conn.getresponse(departmentQueryStr)

    def eachData(datas, handler):
        if handler != None:
            for data in datas:
                for handFuncKey in handler:
                    if handFuncKey in data.keys():
                        data[handFuncKey] = handler[handFuncKey](data[handFuncKey])
        return datas

    if response is not None and response['code'] == '200' and len(response['data']) > 0:
        datas = response['data']

        datas = eachData(datas, handler={
            'creattime': Handler['MillisecondTimeStampToYMD_HMS'],
            'updatetime': Handler['MillisecondTimeStampToYMD_HMS'],
            'parentsortingcenterid': Handler['sqlBUG']
        })

        print(now + "处理正式部门数据" + str(datas))

        # 本地测试
        # db = MySQL(host="127.0.0.1", user="root", passwd="root", db="eyes")

        # 正式数据库
        db = MySQL(host="10.230.3.92", port=8088, user="eyes_prog", passwd="3FDEF8AED7DD6E43E3", db="eyes")

        insert = Insert(
            "INSERT INTO departments(id,name,dtype,created_at,updated_at,city_id,is_deleted,distribution_code,parent_sortings)",
            ['id', 'text', 'dtype', 'creattime', 'updatetime', 'cityid', 'isdeleted', 'distributioncode',
             'parentsortingcenterid'])

        update = Update(tableName="departments",
                        set={"text": "name",
                             "dtype": "dtype",
                             "creattime": "created_at",
                             "updatetime": "updated_at",
                             "distributioncode": "distribution_code",
                             "cityid": "city_id",
                             "isdeleted": "is_deleted",
                             "parentsortingcenterid": "parent_sortings"},
                        where=" id=${id}")

        updateOrInsert = UpdateOrInsert(insert, update, query="SELECT * FROM departments WHERE id=${id}", db=db)

        updateOrInsert.pushDatas(datas)

        db.clossConn()


if __name__ == "__main__":
    action()
