from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import os
import json
import demjson
# 用于显示主界面

# 用于在启动前将数据全部读入内存------------------------------------------------------------------------------------------------
pwd = os.getcwd()
print('---后端---')
print('---读取数据---')
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
lianluFile = open(pwd+'/mainApp'+'/data'+'/lianlu.txt')
siteName = []  # 存储地点名称
allData['lianlu'] = {}
lineNum = 0  # 记录文件行数
for line in lianluFile:
    oneLine = line.replace('\n', '').split(',')
    if lineNum == 0:
        siteName = oneLine
    else:
        oneDict = allData['lianlu'][oneLine[0]] = {}
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
lianluFile.close()

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
# print(allData)
renwuFile.close()
# print([1, 2, 3][1:2])
file = open('/Users/lvlaxjh/code/code/bigDataVisualization/bigDataVisualization/code/datavis/mainApp/allData.json', 'w')
file.write(json.dumps(allData))
file.close()
# -------------------------------------------------------------------------------------------------


def index(request):
    response = render(request, 'index.html')
    return response

# 因为没有商量接口设定暂时设定一个接口


def returnData(request):
    result = {"test": "s"}
    # 获取前端的请求
    try:
        if request.method == "POST":
            require = demjson.decode(request.body)
        # -------------------------------------------------------------------------------------------
        reKey = require['key']
        reTime = require['time']
        

        # -------------------------------------------------------------------------------------------
    except Exception as e:
        print(e)
        result = {"error": e}
    return JsonResponse(result)
