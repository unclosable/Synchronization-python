import xml.etree.cElementTree as ET

if __name__ == "__main__":
    tree = ET.parse("/Users/zhengwei/Desktop/xmlTest.xml")

    root = tree.getroot()

    print(root.tag)

    for DATA_RECORD in root.findall('DATA_RECORD'):
        print(DATA_RECORD.find("EMPLOYEEID").text)


class FileReaderClass(object):
    filePath = ''
    datas = []

    def __init__(self, filePath):
        self.filePath = filePath

    def readDatas(self, keys=[], handler={}):
        tree = ET.parse(self.filePath)
        root = tree.getroot()
        reDatas = []
        for DATA_RECORD in root.findall('DATA_RECORD'):
            data = {}
            for key in keys:
                child = DATA_RECORD.find(key)
                if child is not None:
                    data[key] = child.text
                    if key in handler:
                        data[key] = handler[key](data[key])
                else:
                    data[key] = 'null'
            reDatas.append(data)
        return reDatas
