from django import forms
from . import models
import datetime


class LogForms(forms.ModelForm):
    class Meta:
        model = models.Inspection_log
        fields = '__all__'
        widgets = {
            'job_type': forms.TextInput(attrs={'placeholder': 'Наименование работы'}),
            'record': forms.Textarea(attrs={'placeholder': 'Описание', 'resize': 'none'}),
            'substation_name': forms.Select(attrs={'placeholder': 'Подстанция/ТП'}),
           # 'substation_img': forms.ImageField(widget=forms.)


        }
    date_record = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'Дата', 'class': 'datepicker'}, ),
        input_formats=('%d-%m-%Y',),

    )
