from httpAction.HttpConnect import HttpConnect
from dbAction.MySQLConnect import MySQL, Insert, Update, UpdateOrInsert
from TestPackage.Handler import Handler
import datetime


def action():
    conn = HttpConnect("pms-service.wltest.com")

    departmentQueryStr = "/merchant/"

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

        # datas = eachData(datas, handler={
        #     'creattime': Handler['MillisecondTimeStampToYMD_HMS'],
        #     'updatetime': Handler['MillisecondTimeStampToYMD_HMS']
        # })

        # 本地测试
        # db = MySQL(host="127.0.0.1", user="root", passwd="root", db="eyes")

        # 正式数据库
        # db = MySQL(host="10.230.3.92", port=8088, user="eyes_prog", passwd="3FDEF8AED7DD6E43E3", db="eyes")

        # 测试数据库
        db = MySQL(host="10.3.47.82", port=3308, user="eyes", passwd="eyes", db="eyes")

        insert = Insert("INSERT INTO merchant(id,name,code,province_id,city_id,is_deleted)",
                        ['id', 'text', 'code', 'provinceid', 'cityid', 'isdeleted'])

        update = Update(tableName="merchant",
                        set={"text": "name",
                             "code": "code",
                             "provinceid": "province_id",
                             "cityid": "city_id",
                             "isdeleted": "is_deleted"},
                        where=" id=${id}")

        updateOrInsert = UpdateOrInsert(insert, update, query="SELECT * FROM merchant WHERE id=${id}", db=db)

        updateOrInsert.pushDatas(datas)


if __name__ == "__main__":
    action()
