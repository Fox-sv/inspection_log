from django.urls import path
from . import views


app_name = 'inspection'

urlpatterns = [

    path('', views.home, name='start_page'),
    path('inspection_log/', views.inspection_log, name='inspection_log'),
    path('log_form/', views.log_form, name='log_form'),
    path('log_details/<int:log_id>/', views.log_details, name='log_details'),
    path('update/<int:log_id>/', views.update_log, name='update_log'),
    path('delete/<int:log_id>/', views.delete_log, name='delete_log'),

]