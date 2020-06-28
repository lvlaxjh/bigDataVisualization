from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import os
import json
import demjson
# 用于显示主界面

print('---后端---')


def index(request):
    response = render(request, 'index.html')
    return response

# 因为没有商量接口设定暂时设定一个接口


def returnData(request):
    result = {"test": "s"}
    # 获取前端的请求
    require = demjson.decode(request.body)
    print(require)
    return JsonResponse(result)
