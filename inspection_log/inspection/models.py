from msilib.schema import File

from django.db import models
from django.contrib.auth.models import User
import datetime


class Substation(models.Model):
    substation_name = models.CharField(max_length=100)

    def __str__(self):
        return self.substation_name


class Inspection_log(models.Model):
    date_record = models.DateField(verbose_name='Date of Record')
    job_type = models.CharField(max_length=100)
    record = models.TextField(max_length=200, verbose_name='Record', blank=True)
    user_name_id = models.ForeignKey(User, verbose_name='Name', related_name='log_to_user', null=True, blank=True, on_delete=models.SET_NULL)
    substation_name = models.ForeignKey(Substation, verbose_name='substation', related_name='log_to_substation', null=True, on_delete=models.SET_NULL)
    note = models.BooleanField(default=False)
    substation_img = models.FileField(upload_to='%Y%m%d/', null=True, blank=True)

    def add_photo(self, photo_file):
        with open(photo_file) as f:
            my_file = File(f)
            filename = "filename.jpg"
            self.substation_img.save(filename, my_file)

    def __str__(self):
        return f'{self.date_record}, {self.substation_name} - {self.job_type}. {self.user_name_id}'


