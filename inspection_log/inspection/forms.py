from django import forms
from . import models


SORTED_LOG = (
    ('', 'Дате'),
    ('', 'Внесению'),
    )


def all_users():
    '''
    Список всех зарегистрированых пользователей
    '''
    log = models.Inspection_log.objects.all()
    users = [i.user_name_id for i in log]
    log_users = [i for i in set(users)]
    return log_users

def usernames():
    username = [(name, name) for key, name in enumerate(all_users())]
    username.insert(0, ('0', 'Производитель'))
    return username

  
class LogForms(forms.ModelForm):
    class Meta:
        model = models.Inspection_log
        fields = '__all__'
        widgets = {
            'job_type': forms.TextInput(attrs={'placeholder': 'Наименование работы'}),
            'record': forms.Textarea(attrs={'placeholder': 'Описание', 'resize': 'none'}),
            'substation_name': forms.TextInput(attrs={'placeholder': 'Подстанция/ТП'}),
        }

    date_record = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'Дата', 'class': 'datepicker', 'readonly': "readonly"}, ),
        input_formats=('%d-%m-%Y',),
    )


class InspectionLogForm(forms.Form):
    substation_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Подстанция/ТП'}), required=False)
    date_time_start = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'Дата начала', 'class': 'datepicker', 'readonly': 'readonly'}), input_formats=('%d-%m-%Y',), required=False)
    date_time_last = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'Дата окончания', 'class': 'datepicker2', 'readonly': 'readonly'}), input_formats=('%d-%m-%Y',), required=False)
    developer = forms.ChoiceField(choices=usernames(), widget=forms.Select(attrs={'data-display': '1'},), required=False)