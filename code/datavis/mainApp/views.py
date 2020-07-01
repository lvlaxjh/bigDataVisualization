from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
import demjson
# 用于显示主界面
# shangxing: 9000
# xiaxing: 9000
# yujian: 9000
# task: 5000
# 用于在启动前将数据全部读入内存------------------------------------------------------------------------------------------------
pwd = os.getcwd()
allData = {}  # 存储全部数据
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
allData["shangxing"] = {}
allData["xiaxing"] = {}
siteName = []  # 存储地点名称
for file in fileList:
    fileName = file.name.split('/')[-1][:-4]
    fileName1 = fileName.split('_')[0]  # beijing
    fileName2 = fileName.split('_')[1]  # xiaxing
    lineNum = 0  # 记录文件行数
    allData[fileName2][fileName1] = {}
    for line in file:
        oneLine = line.replace('\n', '').split(',')
        if lineNum == 0:
            siteName = oneLine
        else:
            oneDict = allData[fileName2][fileName1][oneLine[0]] = {}
            for i in range(len(oneLine)):
                if i != 0:
                    oneDict[siteName[i]] = oneLine[i]
        lineNum += 1
# print(allData)
for i in fileList:
    i.close()
# 存储链路内容------------------------------------------------------------------------------------------------
yujianFile = open(pwd+'/mainApp'+'/data'+'/yujian.txt')
siteName = []  # 存储地点名称
allData['yujian'] = {}
lineNum = 0  # 记录文件行数
for line in yujianFile:
    oneLine = line.replace('\n', '').split(',')
    if lineNum == 0:
        siteName = oneLine
    else:
        oneDict = allData['yujian'][oneLine[0]] = {}
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
allData['renwu'] = {}
lineNum = 0  # 记录文件行数
for line in renwuFile:
    oneLine = line.replace('\n', '').split(',')
    if lineNum == 0:
        siteName = oneLine
    else:
        if oneLine[0] not in allData['renwu'].keys():
            oneDict = allData['renwu'][oneLine[0]] = {}  # 时间
        oneDict[oneLine[1]] = []
        for i in oneLine[2:]:
            oneDict[oneLine[1]].append(i)
        # for i in oneLine[]
    lineNum += 1
renwuFile.close()
# -------------------------------------------------------------------------------------------------


def index(request):
    response = render(request, 'index.html')
    return response


def region(request):
    response = render(request, 'region.html')
    return response


def shangxing(request):
    response = render(request, 'shangxing.html')
    return response


def task(request):
    response = render(request, 'task.html')
    return response


def xiaxing(request):
    response = render(request, 'xiaxing.html')
    return response


def testt(request):
    response = render(request, 'test.html')
    return response


@csrf_exempt
def returnData(request):
    result = {
        "shangxing": {
            "time": "",
            "cdc": {
                "beijing": {},
                "dongguan": {},
                "nanjing": {},
            }
        },
        "xiaxing": {
            "time": "",
            "cdc": {
                "beijing": {},
                "dongguan": {},
                "nanjing": {},
            }
        },
        "yujian": {
            "time": "",
            "cdc": {
                "beijing": {},
                "dongguan": {},
                "nanjing": {},
            }
        },
        "renwu": {
            "time": "",
            "id": {}},
    }

    # 获取前端的请求
    # try:
    if request.method == "POST":
        # print(request.body)
        # require = demjson.decode(request.body)
        # -------------------------------------------------------------------------------------------
        # reKey = require['key']
        # reTime = require['time']
        reKey = request.POST.get('key')
        reTime = request.POST.get('time')
        if reTime == "0":
            reTime = "50"
        else:
            reTime = str(int(reTime)+5)
        if reKey == "all" or reKey == "renwu":
            if int(reTime) > 5000:
                reTime = '50'
        elif reKey == "shangxing" or reKey == "xiaxing" or reKey == "yujian":
            if int(reTime) > 9000:
                reTime = '50'
        siteList = ['beijing', 'dongguan', 'nanjing']
        # -------------------------------------------------------------------------------------------
        if reKey == "all":
            result['shangxing']['time'] = reTime
            for i in siteList:
                result['shangxing']['cdc'][i] = allData['shangxing'][i][result['shangxing']['time']]
            result['xiaxing']['time'] = reTime
            for i in siteList:
                result['xiaxing']['cdc'][i] = allData['xiaxing'][i][result['xiaxing']['time']]
            result['yujian']['time'] = reTime
            for i in siteList:
                result['yujian']['cdc'][i] = allData['yujian'][result['yujian']['time']][i]
            result['renwu']['time'] = reTime
            result['renwu']['id'] = allData['renwu'][result['renwu']['time']]
        # -------------------------------------------------------------------------------------------

        if reKey == "shangxing":
            result['shangxing']['time'] = reTime
            for i in siteList:
                result['shangxing']['cdc'][i] = allData['shangxing'][i][result['shangxing']['time']]
            # -------------------------------------------------------------------------------------------
        if reKey == "xiaxing":
            result['xiaxing']['time'] = reTime
            for i in siteList:
                result['xiaxing']['cdc'][i] = allData['xiaxing'][i][result['xiaxing']['time']]
            # -------------------------------------------------------------------------------------------

        if reKey == "yujian":
            result['yujian']['time'] = reTime
            for i in siteList:
                result['yujian']['cdc'][i] = allData['yujian'][result['yujian']['time']][i]
            # -------------------------------------------------------------------------------------------
        if reKey == "renwu":
            result['renwu']['time'] = reTime
            result['renwu']['id'] = allData['renwu'][result['renwu']['time']]
            # -------------------------------------------------------------------------------------------
    return JsonResponse(result)
