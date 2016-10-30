from .models import lecture,kakao_user

def function():
    print("Rock and Roll!")
    new=kakao_user(user_key="000")
    new.save()