from django.contrib import admin
from django.urls import path
from . import views, api_utils
from django.urls import path, include


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='sign-up'),
    path('signin/', views.signin, name='sign-in'),
    path('signout/', views.signout, name='signout'),
    path('agenda/', views.agenda, name='agenda'),
    path('download/', views.download, name='download'),
    path('proceedings/download', api_utils.download_proceedings,
         name='download_proceedings'),
    path('program/download', api_utils.download_program,
         name='download_program'),
]
