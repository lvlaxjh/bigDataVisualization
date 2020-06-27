from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import os
import json
# Create your views here.


def index(request):
    response = render(request, 'index.html')
    return response


def returnData(request):
    result = {}
    return JsonResponse(json.dumps(result))
