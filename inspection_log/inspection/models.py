from django.db import models
from django.contrib.auth.models import User


class Inspection_log(models.Model):
    date_record = models.DateField(verbose_name='Date of Record', auto_now_add=True)
    record = models.TextField(max_length=200, verbose_name='Record', blank=True)
    user_name_id = models.ForeignKey(User, verbose_name='Name', related_name='log_to_user', null=True, on_delete=models.SET_NULL)
    substation_name = models.CharField(max_length=100)
    note = models.BooleanField(default=False)
    substation_img = models.ImageField(upload_to='/images')

    def __str__(self):
        return f'{self.user_name_id} сделал запись объека {self.substation_name}'