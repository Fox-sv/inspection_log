from django import forms
from . import models


class LogForms(forms.ModelForm):
    class Meta:
        model = models.Inspection_log
        fields = '__all__'
        widgets = {
            'job_type': forms.TextInput(attrs={'placeholder': 'Наименование работы'}),
            'record': forms.TextInput(attrs={'placeholder': 'Описание'}),
            'date_record': forms.DateInput(attrs={'placeholder': 'Дата'}),
            'substation_name': forms.Select(attrs={'placeholder': 'Подстанция/ТП'}),
            #'substation_img': forms.TextInput(attrs={'placeholder': 'Загрузить фото'}),

        }
