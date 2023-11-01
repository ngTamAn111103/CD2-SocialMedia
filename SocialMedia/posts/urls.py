from django.urls import path, re_path
from .views import post_comment_create_listview, like_unlike_post
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.models import User


app_name = 'post'

urlpatterns =[
    path('', views.post_comment_create_listview, name='main_post_view'),
    path('liked/', views.like_unlike_post, name='like_post_view'),
]