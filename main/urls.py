from django.urls import path
from main import views
app_name = 'work'
urlpatterns = [
    path('job_celery',views.creat_job_celery,name='cel_job'),
    path('jobb',views.creat_job,name='no_job'),
    path('resumeh_celery',views.resumeh_celery,name='cel_res'),
    path('resumeh',views.resumeh,name='no_res'),


    path('',views.main,name="main"),
    path('job',views.job,name='job'),
    path('res',views.res,name='res')
]