from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import lecture,kakao_user

@csrf_exempt
def keyboard(request):
    pass

@csrf_exempt
def message(request):
    pass
    
@csrf_exempt    
def reg_friend(request):
    value=json.loads(request.body.decode("utf-8"))
    key=value['user_key']
    new_user=kakao_user(user_key=key)
    new_user.save()
    return HttpResponse("")

@csrf_exempt
def del_friend(request,user_key):
    #유저 키 삭제
    try: 
        del_user=kakao_user.objects.get(user_key=user_key)
        del_user.exist_user=0
        del_user.save()
    finally:
        return HttpResponse("")


@csrf_exempt
def room(request,user_key):
    #채팅방 나감
    
    return HttpResponse("")