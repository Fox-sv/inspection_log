from django import forms
from . import models
import datetime

def all_users():
    '''
    Список всех зарегистрированых пользователей
    '''
    log = models.Inspection_log.objects.all()
    users = [i.user_name_id for i in log]
    log_users = [i for i in set(users)]
    return log_users

ALL_USERS = [(name, name) for key, name in enumerate(all_users())]
ALL_USERS.insert(0, ('0', 'Производитель'))
SORTED_LOG = (
    ('', 'Дате'),
    ('', 'Внесению'),
    )
  
class LogForms(forms.ModelForm):
    class Meta:
        model = models.Inspection_log
        fields = '__all__'
        # exclude = ['substation_img']
        widgets = {
            'job_type': forms.TextInput(attrs={'placeholder': 'Наименование работы'}),
            'record': forms.Textarea(attrs={'placeholder': 'Описание', 'resize': 'none'}),
            'substation_name': forms.TextInput(attrs={'placeholder': 'Подстанция/ТП'}),

        }

    date_record = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'Дата', 'class': 'datepicker', 'readonly': "readonly"}, ),
        input_formats=('%d-%m-%Y',),

    )
    name_of_substation = forms.CharField(max_length=50)

class InspectionLogForm(forms.Form):
    substation_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Подстанция/ТП'}), required=False)
    date_time_start = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'Дата начала', 'class': 'datepicker', 'readonly': 'readonly'}), input_formats=('%d-%m-%Y',), required=False)
    date_time_last = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'Дата окончания', 'class': 'datepicker2', 'readonly': 'readonly'}), input_formats=('%d-%m-%Y',), required=False)
    developer = forms.ChoiceField(choices=ALL_USERS, widget=forms.Select(attrs={'data-display': '1'},), required=False)
    # sorted_log = forms.ChoiceField()