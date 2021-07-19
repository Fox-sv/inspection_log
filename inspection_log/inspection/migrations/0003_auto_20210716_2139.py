# Generated by Django 3.2.5 on 2021-07-16 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0002_auto_20210716_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Substation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('substation_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='inspection_log',
            name='substation_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='log_to_substation', to='inspection.substation', verbose_name='substation'),
        ),
    ]
