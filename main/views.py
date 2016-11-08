from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import lecture,kakao_user,recent_search,major_list
from django.contrib.auth.decorators import login_required
from .tasks import periodic_task
from .parser import *
from datetime import timedelta

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
            
            r_s_list=["@"+x.lecture.lecture_name for x in user.recent_search_set.all()]

            response_json={
                "message":{
                    "text": "최근 검색한 강의 중 선택하거나\n강의 검색을 눌러주세요"
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
    
    #---강의 이름이 들어왔을 경우
    else:
        
        #---맨 앞 @가 붙은 경우에는 최근 검색 결과에서 검색한 경우
        if "@" is content[0]:

            search_content=content[1:]
            lecture_list=recent_search.objects.filter(lecture__lecture_name=search_content,kakao_user__user_key=key)
            lecture_list=lecture_list[0].lecture
            
            if lecture_list.brand_new()==False:
                a=parsing_class()
                a.parsing_major_name(lecture_list.major.major_name)
                lecture_list=lecture.objects.get(course_number=lecture_list.course_number)


            #--학과 검색시간 갱신
            a=major_list.objects.get(major_name=lecture_list.major.major_name)
            a.recent_datetime=timezone.localtime(timezone.now())
            a.save()

            #--인기도 1 증가
            t=lecture_list
            t.popularity+=1
            t.save()

            #--유저 검색횟수 1 증가
            user.search_number+=1
            user.save()
            
            r_s_list=["@"+x.lecture.lecture_name for x in user.recent_search_set.all()]

            response_json={
                "message":{
                    "text": '과목명: '+lecture_list.lecture_name+"\n"+
                        '담당교수: '+lecture_list.professor_name+"\n"+
                        '현재원/총원: '+str(lecture_list.opening)+"/"+str(lecture_list.total_number)+"\n"+
                        'updated_at: '+str((lecture_list.updated_at+timedelta(hours=9)).strftime('%I시 %M분 %S초 %p'))
                },
                "keyboard":{
                    "type": "buttons",
                    "buttons": ["강의 검색"]+r_s_list
                }
            }
            
            if lecture_list.opening < lecture_list.total_number:
                response_json["message"]["message_button"]={"label": "여석 있음!!!", "url": "http://www.hufs.ac.kr"}

            return HttpResponse(json.dumps(response_json,ensure_ascii=False), content_type=u"application/json; charset=utf-8")

        #---강의 이름만으로 검색 했을 때 여러개의 강의가 나온 경우 :로 강의이름 교수 학수번호를 구분해 세부검색 
        elif ":" in content:

            temp=content.split(":")
            lecture_list=lecture.objects.filter(lecture_name=temp[0],professor_name=temp[1],course_date=temp[2][1:])

        #---아예 처음 검색한 경우
        else:

            lecture_list=lecture.objects.filter(lecture_name__icontains=content)


        #---검색 했을 때 결과가 0인 경우
        if lecture_list.count()==0:

            if user.recent_search_set.all().count()==0:

                response_json={
                    "message":{
                        "text": "해당 강의가 없습니다! 강의 이름을 다시 입력해 주세요"
                    },
                    "keyboard":{
                        "type": "text"
                    }
                }

            else:

                r_s_list=["@"+x.lecture.lecture_name for x in user.recent_search_set.all()]

                response_json={
                    "message":{
                        "text": "해당 강의가 없습니다! 최근 검색한 강의 중 선택하거나\n강의 검색을 눌러주세요"
                    },
                    "keyboard":{
                        "type": "buttons",
                        "buttons":["강의 검색"]+r_s_list
                    }
                }

        #---검색 했을 때 결과가 여러개 나온 경우 -> :를 포함한 세부 검색 결과로 진행
        elif lecture_list.count()>1:

            lecture_list=[lecture.lecture_name+":"+lecture.professor_name+":\n"+lecture.course_date for lecture in lecture_list]

            response_json={
                "message":{
                    "text": "여러개의 강의가 있습니다 선택하세요"
                },
                "keyboard":{
                    "type": "buttons",
                    "buttons": lecture_list
                }
            }

        #---검색 했을 때 결과가 한 개인 경우(검색에 성공한 경우)
        else:

            #---최근 검색 강의에 먼저 저장
            if user.recent_search_set.all().count()>4: user.recent_search_set.all()[0].delete()
            
            if user.recent_search_set.filter(lecture__course_number=lecture_list[0].course_number).count()==0:
                recent_search(kakao_user=user,
                        lecture=lecture_list[0]).save()
                        
            if lecture_list[0].brand_new()==False:
                a=parsing_class()
                a.parsing_major_name(lecture_list[0].major.major_name)
                lecture_list=lecture.objects.filter(course_number=lecture_list[0].course_number)


            #--학과 검색시간 갱신
            a=major_list.objects.get(major_name=lecture_list[0].major.major_name)
            a.recent_datetime=timezone.localtime(timezone.now())
            a.save()

            #--인기도 1 증가
            t=lecture_list[0]
            t.popularity+=1
            t.save()

            #--유저 검색횟수 1 증가
            user.search_number+=1
            user.save()

            r_s_list=["@"+x.lecture.lecture_name for x in user.recent_search_set.all()]

            response_json={
                "message":{
                    "text": '과목명: '+lecture_list[0].lecture_name+"\n"+
                        '담당교수: '+lecture_list[0].professor_name+"\n"+
                        '현재원/총원: '+str(lecture_list[0].opening)+"/"+str(lecture_list[0].total_number)+"\n"+
                        'updated_at: '+str((lecture_list[0].updated_at+timedelta(hours=9)).strftime('%I시 %M분 %S초 %p'))
                },
                "keyboard":{
                    "type": "buttons",
                    "buttons": ["강의 검색"]+r_s_list
                }
            }

            if lecture_list[0].opening < lecture_list[0].total_number:
                response_json["message"]["message_button"]={"label": "여석 있음!!!", "url": "http://www.hufs.ac.kr"}

    return HttpResponse(json.dumps(response_json,ensure_ascii=False), content_type=u"application/json; charset=utf-8")

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
    # try: 
    #     del_user=kakao_user.objects.get(user_key=user_key)
    #     del_user.delete()
    # finally:
    return HttpResponse("")


@csrf_exempt
def room(request,user_key):
    #채팅방 나감
    
    return HttpResponse("")

@login_required
def task_form(request):
    if request.user.is_superuser:
        
        
        # try:
        if request.GET.get('method')=='list':
            parsing_class().major_list_parsing()
            word="리스트 가져오기 성공"
            
        elif request.GET.get('method')=='start':
            periodic_task()
            word="start 성공"
            
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