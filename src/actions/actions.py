from httpAction.HttpConnect import HttpConnect
from dbAction.MySQLConnect import MySQL, Insert

__ctionSettings = {
    'province': {
        'host': 'pms-service.rfddc.com',
        'uri': '/province',
        'dataBase': {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'passwd': 'root',
            'db': 'eyes'
        },
        'insertStr': 'INSERT INTO provinces(id,name) ',
        'dataIndex': ['id', 'text']
    }
}

# 同步校验省
def __province_synchronization():
    provinceSetting = __ctionSettings['province']
    conc = HttpConnect(provinceSetting['host'])
    response = conc.getresponse(provinceSetting['uri'])
    datas = response['data']
    dataBaseInfo = provinceSetting['dataBase']
    mysql = MySQL(host=dataBaseInfo['host'], user=dataBaseInfo['user'], passwd=dataBaseInfo['passwd'],
                  db=dataBaseInfo['db'])
    insert = Insert(insertStr=provinceSetting['insertStr'], dataIndex=provinceSetting['dataIndex'])
    for data in datas:
        checkSql = "select id,name from provinces where id = " + str(data['id'])
        result = mysql.cursor(checkSql)
        if result['response'] == 0:
            mysql.cursor(insert.getSQLByOne(data))
        else:
            if result['cur'].fetchall()[0][1] != data['text']:
                print(result['cur'].fetchall()[0][1])


if __name__ == "__main__":
    __province_synchronization()
