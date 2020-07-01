from django.test import TestCase, Client
from . import models
import json
import os
import random


class DataPutTest(TestCase):
    c = Client()
    allData = {}

    def getRandom(self):
        '''
        取得随机时间
        '''
        num = 0
        while(True):
            num = random.randint(50, 4000)
            if num % 5 == 0:
                break
        return num

    def setUp(self):
        pwd = os.getcwd()
        print('---后端---')
        # 存储上下行内容------------------------------------------------------------------------------------------------
        xiaxingFile1 = open(pwd+'/mainApp'+'/data'+'/beijing_xiaxing.txt')
        xiaxingFile2 = open(pwd+'/mainApp'+'/data'+'/dongguan_xiaxing.txt')
        xiaxingFile3 = open(pwd+'/mainApp'+'/data'+'/nanjing_xiaxing.txt')
        shangxingFile1 = open(pwd+'/mainApp'+'/data'+'/beijing_shangxing.txt')
        shangxingFile2 = open(pwd+'/mainApp'+'/data'+'/dongguan_shangxing.txt')
        shangxingFile3 = open(pwd+'/mainApp'+'/data'+'/nanjing_shangxing.txt')
        fileList = []  # 上下行文件列表
        fileList.append(xiaxingFile1)
        fileList.append(xiaxingFile2)
        fileList.append(xiaxingFile3)
        fileList.append(shangxingFile1)
        fileList.append(shangxingFile2)
        fileList.append(shangxingFile3)
        self.allData["shangxing"] = {}
        self.allData["xiaxing"] = {}
        siteName = []  # 存储地点名称
        for file in fileList:
            fileName = file.name.split('/')[-1][:-4]
            fileName1 = fileName.split('_')[0]  # beijing
            fileName2 = fileName.split('_')[1]  # xiaxing
            lineNum = 0  # 记录文件行数
            self.allData[fileName2][fileName1] = {}
            for line in file:
                oneLine = line.replace('\n', '').split(',')
                if lineNum == 0:
                    siteName = oneLine
                else:
                    oneDict = self.allData[fileName2][fileName1][oneLine[0]] = {
                    }
                    for i in range(len(oneLine)):
                        if i != 0:
                            oneDict[siteName[i]] = oneLine[i]
                lineNum += 1
        # print(self.allData)
        for i in fileList:
            i.close()
        # 存储链路内容------------------------------------------------------------------------------------------------
        yujianFile = open(pwd+'/mainApp'+'/data'+'/yujian.txt')
        siteName = []  # 存储地点名称
        self.allData['yujian'] = {}
        lineNum = 0  # 记录文件行数
        for line in yujianFile:
            oneLine = line.replace('\n', '').split(',')
            if lineNum == 0:
                siteName = oneLine
            else:
                oneDict = self.allData['yujian'][oneLine[0]] = {}
                oneDict['beijing'] = {}
                oneDict['dongguan'] = {}
                oneDict['nanjing'] = {}
                oneDict['beijing']['dongguan'] = oneLine[1]
                oneDict['beijing']['nanjing'] = oneLine[2]
                oneDict['dongguan']['beijing'] = oneLine[3]
                oneDict['dongguan']['nanjing'] = oneLine[4]
                oneDict['nanjing']['beijing'] = oneLine[5]
                oneDict['nanjing']['dongguan'] = oneLine[6]
            lineNum += 1
        yujianFile.close()

        # 存储任务内容------------------------------------------------------------------------------------------------
        renwuFile = open(pwd+'/mainApp'+'/data'+'/task.txt')
        siteName = []  # 存储地点名称
        self.allData['renwu'] = {}
        lineNum = 0  # 记录文件行数
        for line in renwuFile:
            oneLine = line.replace('\n', '').split(',')
            if lineNum == 0:
                siteName = oneLine
            else:
                if oneLine[0] not in self.allData['renwu'].keys():
                    oneDict = self.allData['renwu'][oneLine[0]] = {}  # 时间
                oneDict[oneLine[1]] = []
                for i in oneLine[2:]:
                    oneDict[oneLine[1]].append(i)
                # for i in oneLine[]
            lineNum += 1
        renwuFile.close()
        # -------------------------------------------------------------------------------------------------

    def test_returnData_firstSend(self):
        print("all - 第一次请求时间测试")
        content = {
            "key": "all",
            "time": "0",
        }
        response = self.c.post('/returnData', content).json()
        self.assertEqual(response['shangxing']['time'], '50')
        self.assertEqual(response['xiaxing']['time'], '50')
        self.assertEqual(response['yujian']['time'], '50')
        self.assertEqual(response['renwu']['time'], '50')
        #
        self.assertEqual(response['shangxing']['cdc']['beijing'],)

    def test_returnData_otherSend(self):
        print("all - 其他请求时间测试")
        oneTime = self.getRandom()
        content = {
            "key": "all",
            "time": str(oneTime),
        }
        response = self.c.post('/returnData', content).json()
        self.assertEqual(response['shangxing']['time'], str(oneTime+5))
        self.assertEqual(response['xiaxing']['time'], str(oneTime+5))
        self.assertEqual(response['yujian']['time'], str(oneTime+5))
        self.assertEqual(response['renwu']['time'], str(oneTime+5))

    def test_returnData_shangxing_firstSend(self):
        print("shangxing - 第一次请求时间测试")
        content = {
            "key": "shangxing",
            "time": "0",
        }
        response = self.c.post('/returnData', content).json()
        self.assertEqual(response['shangxing']['time'], '50')

    def test_returnData_shangxing_firstSend(self):
        print("shangxing - 其他请求时间测试")
        oneTime = self.getRandom()
        content = {
            "key": "shangxing",
            "time": str(oneTime),
        }
        response = self.c.post('/returnData', content).json()
        self.assertEqual(response['shangxing']['time'], str(oneTime+5))

    def test_returnData_xiaxing_firstSend(self):
        print("下行端口第一次请求时间测试")
        content = {
            "key": "xiaxing",
            "time": "0",
        }
        response = self.c.post('/returnData', content).json()
        self.assertEqual(response['xiaxing']['time'], '50')
