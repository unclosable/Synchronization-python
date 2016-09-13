'''
Created on 2016年9月9日

@author: zhengwei
'''
import http.client
import json


class HttpConnect:
    __conn = None
    __header = None

    def __init__(self, host, port=None, header: object = {}):
        self.__conn = http.client.HTTPConnection(host, port=port)
        self.__header = header

    def getresponse(self, uri, methodtype="get"):
        self.__conn.request(method=methodtype, url=uri)
        response = self.__conn.getresponse()
        response = json.loads(response.read().decode(encoding='utf-8'), encoding="utf-8")
        return response
