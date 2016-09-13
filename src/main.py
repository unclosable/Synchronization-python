'''
Created on 2016年9月9日

@author: zhengwei
'''

from TestPackage.FileReader import FileReaderClass
from dbAction.MySQLConnect import Insert

file = FileReaderClass('/Users/zhengwei/Desktop/test2.json')

datas = file.eachData()
print(len(datas))

insert = Insert("INSERT INTO merchant(id,name,code,province_id,city_id,is_deleted)",
                ['ID', 'MERCHANTNAME', 'MERCHANTCODE', 'PROVINCEID', 'CITYID', 'ISDELETED'])

strsql = insert.getSQLByList(datas=datas)
print(strsql)