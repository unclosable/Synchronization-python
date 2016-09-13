'''
Created on 2016年9月8日

@author: zhengwei
'''
import codecs
import json


class FileReaderClass(object):
    filePath = ''
    datas = []

    def __init__(self, filePath):
        self.filePath = filePath
        self.__readDatas()

        # 读取JSON

    def __readDatas(self):
        file = codecs.open(self.filePath, "r", "utf-8")
        fileString = file.read(size=-1);
        if fileString.startswith(u'\ufeff'):  # BOM
            fileString = fileString.encode('UTF-8')[3:].decode('UTF-8')
        JSONArray = json.loads(fileString, encoding="UTF-8")
        self.datas = JSONArray

    def eachData(self, handler=None):
        if handler != None:
            for data in self.datas:
                for handFuncKey in handler:
                    if handFuncKey in data.keys():
                        data[handFuncKey] = handler[handFuncKey](data[handFuncKey])
                # print(data)
        return self.datas
