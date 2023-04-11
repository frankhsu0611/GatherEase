from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='sign-up'),
    path('signin/', views.signin, name='sign-in'),
    path('signout/', views.signout, name='signout'),
    path('agenda/', views.agenda, name='agenda'),
    path('download/', views.download, name='download'),
    ]

