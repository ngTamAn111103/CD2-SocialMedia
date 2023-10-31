from django.urls import path, re_path
from .views import post_comment_create_listview
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.models import User


app_name = 'post'

urlpatterns =[
    path('', views.post_comment_create_listview, name='main_post_view'),
]