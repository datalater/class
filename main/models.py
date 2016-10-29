from __future__ import unicode_literals
from django.db import models


class kakao_user(models.Model):
    
    user_key=models.CharField(max_length=50)
    search_number=models.IntegerField(default=0)


class lecture(models.Model):
    
    course_number=models.CharField(max_length=20)
    major=models.CharField(max_length=30)
    lecture_name=models.CharField(max_length=30)
    professor_name=models.CharField(max_length=30)
    opening=models.IntegerField()
    total_number=models.IntegerField()
    popularity=models.IntegerField(default=0)