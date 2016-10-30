from .models import lecture,kakao_user

def function():
    new=kakao_user(user_key="000")
    new.save()