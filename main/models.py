from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from datetime import timedelta

class kakao_user(models.Model):

    user_key=models.CharField(max_length=50)
    search_number=models.IntegerField(default=0)

    def __str__(self):
        return self.user_key


class major_list(models.Model):
    
    #--전공이름
    major_name=models.CharField('전공',max_length=25)
    #--전공(1) OR 교양(0)
    category=models.IntegerField(null=True)
    #--최근 해당 학과 강의 검색 일자
    recent_datetime=models.DateTimeField(null=True)
    #--년도
    year=models.IntegerField(null=True)
    #--학기
    semester=models.IntegerField(null=True)
    #--전공코드
    major_code=models.CharField(max_length=20,null=True)
    #--파싱 on_off
    on_off=models.BooleanField(default=True)
    
    def __str__(self):
        return self.major_name

    #--해당 학과를 지속적으로 파싱해야하는지 판단하는 메소드, 30초 이내 검색이 없었을 경우 더 이상 새로운 정보 받아오지 않음.
    def should_parse(self):

        if (timezone.now()-self.recent_datetime).seconds<=30:
            return True
        else:
            return False


class lecture(models.Model):
    
    major=models.ForeignKey(major_list)
    course_number=models.CharField('학수번호',unique=True,max_length=20)
    course_date=models.CharField('강의일',max_length=30,null=True)
    lecture_name=models.CharField('강의 이름',max_length=30)
    professor_name=models.CharField('교수 이름',max_length=30)
    opening=models.IntegerField('여석')
    total_number=models.IntegerField('자리')
    popularity=models.IntegerField('조회 횟수',default=0)
    updated_at = models.DateTimeField('Updated at',null=True)
    
    def __str__(self):
        return self.lecture_name+" "+self.professor_name

    #--이 강의 정보가 업데이트 되고 있는 정보인지 즉, 5초 이내의 정보인지 검사
    def brand_new(self):
        
        if (timezone.now()-self.updated_at).seconds>22:
            return False
        else:
            return True


class recent_search(models.Model):
    
    kakao_user=models.ForeignKey(kakao_user)
    lecture=models.ForeignKey(lecture,null=True)
    
    def __str__(self):
        return self.lecture.lecture_name