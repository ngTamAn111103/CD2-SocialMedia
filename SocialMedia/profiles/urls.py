from django.urls import path, re_path
from .views import my_profile_view
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.models import User


app_name = 'profiles'

urlpatterns =[
    path('myprofile/', views.my_profile_view, name='my_profile_view'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]