from __future__ import unicode_literals
from django.db import models


class kakao_user(models.Model):
    
    user_key=models.CharField(max_length=50)
    search_number=models.IntegerField(default=0)
    recent_search=models.CharField(max_length=100,default="")

    def __str__(self):
        return self.user_key


class lecture(models.Model):
    
    course_number=models.CharField('학수번호',unique=True,max_length=20)
    major=models.CharField('전공',max_length=30)
    lecture_name=models.CharField('강의 이름',max_length=30)
    professor_name=models.CharField('교수 이름',max_length=30)
    opening=models.IntegerField('여석')
    total_number=models.IntegerField('자리')
    popularity=models.IntegerField('조회 횟수',default=0)
    updated_at = models.DateTimeField('Updated at',auto_now=True)
    
    def __str__(self):
        return self.lecture_name+" "+self.professor_name