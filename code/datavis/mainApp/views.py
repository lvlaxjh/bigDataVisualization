from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import os
import json

# 用于显示主界面


def index(request):
    response = render(request, 'index.html')
    return response

# 因为没有商量接口设定暂时设定一个接口


def returnData(request):
    result = {}
    return JsonResponse(json.dumps(result))