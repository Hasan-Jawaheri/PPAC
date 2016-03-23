from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

import json

def index(request):
  return HttpResponse(render('/debug/index.html'))

def getinfo(request):
  try:
    return HttpResponse(json.dumps({'matrix': cache.get('mtx')}))
  except:
    return HttpResponse("")

@csrf_exempt
def setinfo(request):
  mtx = json.loads(request.POST["matrix"])
  try:
    print ("setting")
    cache.set('mtx', mtx)
  except:
    print ("adding")
    cache.add('mtx', mtx)

  return HttpResponse("ok")
