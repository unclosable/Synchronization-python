'''
Created on 2016年9月9日

@author: zhengwei
'''
import pymysql


class MySQL(object):
    __conn = None

    def __init__(self, host, user, passwd, db, charset="utf8", port=3306):
        self.__conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)

    def cursor(self, sql):
        cur = self.__conn.cursor()
        try:
            response = cur.execute(sql)
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
        reSql = self.__insertStr + " VALUES "
        for data in datas:
            dataStr = "("
            for index in self.__dataIndex:
                dataStr += "\"" + str(data[index]) + "\","
            reSql += dataStr[:-1] + "),\n"
        return reSql[:-2]

    def getSQLByOne(self, data):
        reSql = self.__insertStr + " VALUES "
        dataStr = "("
        for index in self.__dataIndex:
            dataStr += "\"" + str(data[index]) + "\","
        reSql += dataStr[:-1] + ")"
        return reSql


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
        for match in iter:
            if match.group(1) in data:
                whereStr = whereStr.replace(match.group(), str(data[match.group(1)]))
        return whereStr

    def getUpdateSQLByOne(self, data):
        reSQL = "UPDATE " + self.__tableName + " SET "
        for setKey in self.__set:
            reSQL += self.__set[setKey] + "=\"" + str(data[setKey]) + "\","
        reSQL = reSQL[:-1] + " WHERE " + self.__getWhere(data)
        return reSQL


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
        for match in iter:
            if match.group(1) in data:
                whereStr = whereStr.replace(match.group(), str(data[match.group(1)]))
        return whereStr

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
