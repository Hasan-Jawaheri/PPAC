from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

import json

def index(request):
  return HttpResponse(render(request, 'debug/index.html'))

def getinfo(request):
  try:
    return HttpResponse(json.dumps({'matrix': cache.get('mtx'), 'pose': cache.get('pose')}))
  except:
    return HttpResponse("")

@csrf_exempt
def setinfo(request):
  try:
    mtx = json.loads(request.POST["matrix"])
    try:
      cache.set('mtx', mtx)
    except:
      cache.add('mtx', mtx)
  except: pass

  try:
    pose = json.loads(request.POST["pose"])
    try:
      cache.set('pose', pose)
    except:
      cache.add('pose', pose)
  except: pass

  return HttpResponse("ok")
