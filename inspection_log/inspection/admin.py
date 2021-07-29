from django.contrib import admin
from . import models

# admin.site.register(models.Inspection_log)
admin.site.register(models.Substation)


@admin.register(models.Inspection_log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('date_record', 'substation_name', 'job_type', 'user_name_id', 'note')
    list_filter = ('substation_name', 'user_name_id', 'job_type', 'note')
    search_fields = ('substation_name', 'job_type', 'date_record',)
