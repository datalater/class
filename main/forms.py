from django import forms


class task_check_form(forms.Form):
    TASK_CHOICES = (
        (1, '파싱 시작'),
        (2, '파싱 중지'),
        (3, '파싱 재시작'),
        (4, '시간 조절'),
    )
    task_choice = forms.IntegerField(
        choices=TASK_CHOICES
    )
    
    interval = forms.IntegerField(label= 'Parsing Interval')