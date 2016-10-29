from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^keyboard$', views.keyboard),
    url(r'^message$',views.message),
    url(r'^friend$',views.reg_friend),
    url(r'^friend/(?P<user_key>.+)$',views.del_friend),
    url(r'^chat_room/(?P<user_key>.+)$',views.room)
]