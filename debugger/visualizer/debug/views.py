from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

import json

def index(request):
  return HttpResponse(render(request, 'debug/index.html'))

def getinfo(request):
  try:
    return HttpResponse(json.dumps({'matrix': cache.get('mtx')}))
  except:
    return HttpResponse("")

@csrf_exempt
def setinfo(request):
  mtx = json.loads(request.POST["matrix"])
  try:
    cache.set('mtx', mtx)
  except:
    cache.add('mtx', mtx)

  return HttpResponse("ok")
