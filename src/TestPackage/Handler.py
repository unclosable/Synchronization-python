'''
Created on 2016年9月8日

@author: zhengwei
'''
import datetime, re

__pattern_oracleDatetime = re.compile('^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})Z$')


def __OracleDateToMySQLDate(value):
    if value == None:
        now = datetime.datetime.now()
        return str(now)[0:19]
    else:
        match = __pattern_oracleDatetime.match(value)
        if match:
            return match.group(1) + " " + match.group(2) + ":00"
        else:
            now = datetime.datetime.now()
            return str(now)[0:19]


def __NoneDefaultInt(value):
    if value == None:
        return -1
    else:
        return value


Handler = {
    'OracleDateToMySQLDate': __OracleDateToMySQLDate,
    'NoneDefaultInt': __NoneDefaultInt
}
