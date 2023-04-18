from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.home_dashboard, name='home_dashboard'),
]
