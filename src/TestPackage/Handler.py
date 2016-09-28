'''
Created on 2016年9月8日

@author: zhengwei
'''
import datetime, re, types

__pattern_oracleDatetime = re.compile('^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})Z$')
__pattern_mysqlDatetime = re.compile('^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})$')


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


def __MillisecondTimeStampToYMD_HMS(value):
    dateArray = datetime.datetime.utcfromtimestamp(value / 1000)
    str = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    return str


def __stringnumberTOnumenr(value):
    try:
        return int(value.replace(",", ""))
    except:
        return -1


def __stringdatedefault(value):
    if value is None:
        now = datetime.datetime.now()
        return str(now)[0:19]
    match = __pattern_mysqlDatetime.match(value)
    if match:
        return value
    else:
        now = datetime.datetime.now()
        return str(now)[0:19]


__sqlReplace = {
    "\"": "&#34;"
}


def __sqlBUG(value):
    if value is None:
        return ""
    if type(value) is str:
        for key in __sqlReplace:
            value = value.replace("\"", "&#34;")
        return value
    else:
        return ""


Handler = {
    'OracleDateToMySQLDate': __OracleDateToMySQLDate,
    'NoneDefaultInt': __NoneDefaultInt,
    'MillisecondTimeStampToYMD_HMS': __MillisecondTimeStampToYMD_HMS,
    'stringnumberTOnumenr': __stringnumberTOnumenr,
    'stringdatedefault': __stringdatedefault,
    'sqlBUG': __sqlBUG
}
