from django.contrib import admin
from .models import kakao_user,lecture,recent_search

# Register your models here.

admin.site.register(kakao_user)
admin.site.register(lecture)
admin.site.register(recent_search)