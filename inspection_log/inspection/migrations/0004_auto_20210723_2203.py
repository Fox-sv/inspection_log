# Generated by Django 3.2.5 on 2021-07-23 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inspection', '0003_auto_20210716_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection_log',
            name='date_record',
            field=models.DateField(verbose_name='Date of Record'),
        ),
        migrations.AlterField(
            model_name='inspection_log',
            name='substation_img',
            field=models.FileField(blank=True, null=True, upload_to='%Y%m%d/'),
        ),
        migrations.AlterField(
            model_name='inspection_log',
            name='substation_name',
            field=models.CharField(default=1, max_length=100, verbose_name='substation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inspection_log',
            name='user_name_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='log_to_user', to=settings.AUTH_USER_MODEL, verbose_name='Name'),
        ),
    ]
