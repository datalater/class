from django.contrib import admin
from .models import kakao_user,lecture,recent_search,major_list

# Register your models here.

admin.site.register(kakao_user)
admin.site.register(lecture)
admin.site.register(recent_search)
admin.site.register(major_list)