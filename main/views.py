from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import lecture,kakao_user,recent_search
from django.contrib.auth.decorators import login_required
from .tasks import periodic_task


@csrf_exempt
def keyboard(request):
    response_json={}
    response_json["type"]="buttons"
    response_json["buttons"]=["시작하기"]
    return HttpResponse(json.dumps(response_json,ensure_ascii=False), content_type=u"application/json; charset=utf-8")

@csrf_exempt
def message(request):
    value=json.loads(request.body.decode("utf-8"))
    
    key=value['user_key']
    text=value['type']
    content=value["content"]
    response_json={}
    user=kakao_user.objects.get(user_key=key)
    
    if content=="시작하기":
        
        if user.recent_search_set.all().count()==0:
            
            response_json={
                "message":{
                    "text": "강의 이름을 입력해 주세요"
                },
                "keyboard":{
                    "type": "text"
                }
            }
            
        else:
            
            r_s_list=[x.lecture_name for x in user.recent_search_set.all()]
            
            response_json={
                "message":{
                    "text": "최근 검색한 강의 중 선택하거나<br>강의 검색을 눌러주세요"
                },
                "keyboard":{
                    "type": "buttons",
                    "buttons":["강의 검색"]+r_s_list
                }
            }
            
    elif content=="강의 검색":
    
        response_json={
            "message":{
                "text": "강의 이름을 입력해 주세요"
            },
            "keyboard":{
                "type": "text"
            }
        }
    
    else:
        if ":" in content:
            
            temp=content.split(":")
            lecture_list=lecture.objects.filter(lecture_name=temp[0],professor_name=temp[1],course_number=temp[2])
            
        else:
            
            lecture_list=lecture.objects.filter(lecture_name__icontains=content)
        
        
        if lecture_list.count()>1:
            
            lecture_list=[lecture.lecture_name+":"+lecture.professor_name+":"+lecture.course_number for lecture in lecture_list]
            
            response_json={
                "message":{
                    "text": "여러개의 강의가 있습니다 선택하세요"
                },
                "keyboard":{
                    "type": "buttons",
                    "buttons": lecture_list
                }
            }
            
        else:
            
            if user.recent_search_set.all().count()>5:
                
                user.recent_search_set.all()[0].delete()
                recent_search(kakao_user=user,lecture_name=temp[0],professor_name=temp[1],course_number=temp[2]).save()
                
            else:
                
                recent_search(kakao_user=user,lecture_name=temp[0],professor_name=temp[1],course_number=temp[2]).save()
            #검색 후 보여주기
            
        
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
        del_user.delete()
    finally:
        return HttpResponse("")


@csrf_exempt
def room(request,user_key):
    #채팅방 나감
    
    return HttpResponse("")

@login_required
def task_form(request):
    if request.user.is_superuser:
        
        
        # try:
        if request.GET.get('method')=='start':
            periodic_task()
            
        elif request.GET.get('method')=='stop':
            periodic_task.pause_task()
            word="pause 성공"
            
        elif request.GET.get('method')=='resume':
            periodic_task.resume_task()
            word="resume 성공"
            
        elif request.GET.get('method')=='interval':
            
            periodic_task.modify_task(time=int(request.GET.get('interval')))
            word="interval 조절 성공"
        else:
            word=""
            
        status=periodic_task.get_status()
        # except(e):
        #     print("fail")
        #     word=e
            
        
        return render(request,'control.html',{'message' : word, 'status' : status})