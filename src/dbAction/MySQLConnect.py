'''
Created on 2016年9月9日

@author: zhengwei
'''
import pymysql


class safeSQL:
    sql = None
    tupleData = None

    def __init__(self, sql, data):
        self.sql = sql
        self.tupleData = data

    def isList(self):
        if len(self.tupleData) > 0 and type(self.tupleData[0]) == tuple:
            return True
        else:
            return False


class MySQL(object):
    __conn = None

    def __init__(self, host, user, passwd, db, charset="utf8", port=3306):
        self.__conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)

    def cursor(self, sql):
        if type(sql) == str:
            return self.__cursor_sql(sql)
        if isinstance(sql, safeSQL):
            if sql.isList():
                return self.__cursor_tupleList(sql.sql, sql.tupleData)
            else:
                return self.__cursor_tuple(sql.sql, sql.tupleData)

    def __cursor_sql(self, sql):
        cur = self.__conn.cursor()
        try:
            response = cur.execute(sql)
            self.__conn.commit()
            return {'response': response, 'cur': cur}
        finally:
            cur.close()

    def __cursor_tuple(self, sql, tuple):
        cur = self.__conn.cursor()
        try:
            response = cur.execute(sql, tuple)
            self.__conn.commit()
            return {'response': response, 'cur': cur}
        finally:
            cur.close()

    def __cursor_tupleList(self, sql, tuple):
        cur = self.__conn.cursor()
        try:
            response = cur.executemany(sql, tuple)
            self.__conn.commit()
            return {'response': response, 'cur': cur}
        finally:
            cur.close()

    def clossConn(self):
        self.__conn.close()


class Insert(object):
    __insertStr = None
    __dataIndex = None

    def __init__(self, insertStr, dataIndex):
        self.__dataIndex = dataIndex
        self.__insertStr = insertStr

    def getSQLByList(self, datas):
        reSql = self.__insertStr + " VALUES ("
        for i in range(len(self.__dataIndex)):
            reSql += "%s,"
        reSql = reSql[:-1] + ")"
        re_datas = []
        for data in datas:
            values = []
            for index in self.__dataIndex:
                values.append(str(data[index]))
            re_datas.append(tuple(values))
        return safeSQL(reSql, tuple(re_datas))

    def getSQLByOne(self, data):
        reSql = self.__insertStr + " VALUES ("
        for i in range(len(self.__dataIndex)):
            reSql += "%s,"
        reSql = reSql[:-1] + ")"
        values = []
        for index in self.__dataIndex:
            values.append(str(data[index]))
        return safeSQL(reSql, tuple(values))


import re


class Update(object):
    __tableName = None
    __set = None
    __where = None

    __whereRegex = re.compile('\${(.+?)}')

    def __init__(self, tableName, set, where):
        self.__tableName = tableName
        self.__set = set
        self.__where = where

    def __getWhere(self, data):
        whereStr = self.__where
        iter = self.__whereRegex.finditer(whereStr)
        dataIndex = []
        for match in iter:
            if match.group(1) in data:
                whereStr = whereStr.replace(match.group(), "%s")
                dataIndex.append(str(data[match.group(1)]))
        return safeSQL(whereStr, tuple(dataIndex))

    def getUpdateSQLByOne(self, data):
        reSQL = "UPDATE " + self.__tableName + " SET "
        dataIndex = []
        for setKey in self.__set:
            if setKey in data:
                dataIndex.append(str(data[setKey]))
                reSQL += self.__set[setKey] + "= %s ,"
        whereSafesql = self.__getWhere(data)
        reSQL = reSQL[:-1] + " WHERE " + whereSafesql.sql
        print(reSQL)
        return safeSQL(reSQL, tuple(dataIndex) + whereSafesql.tupleData)


class UpdateOrInsert(object):
    __insert = None
    __update = None
    __query = None
    __db = None

    __whereRegex = re.compile('\${(.+?)}')

    def __init__(self, inser, update, query, db):
        self.__insert = inser
        self.__update = update
        self.__query = query
        self.__db = db

    def __getWhere(self, data):
        whereStr = self.__query
        iter = self.__whereRegex.finditer(whereStr)
        dataIndex = []
        for match in iter:
            if match.group(1) in data:
                dataIndex.append(str(data[match.group(1)]))
                whereStr = whereStr.replace(match.group(), "%s")
        return safeSQL(whereStr, tuple(dataIndex))

    def pushDatas(self, datas):
        for data in datas:
            queryStr = self.__getWhere(data)
            cur = self.__db.cursor(queryStr)
            if cur['response'] == 0:
                sql = self.__insert.getSQLByOne(data)
                self.__db.cursor(sql)
            else:
                sql = self.__update.getUpdateSQLByOne(data)
                self.__db.cursor(sql)
