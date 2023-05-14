from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.home_dashboard, name='home_dashboard'),
    path("process_ticket/", views.process_ticket, name="process_ticket"),
    path('scanner/', views.scanner, name='scanner'),
]
