from django.urls import path
from . import api_utiles
from . import views

urlpatterns = [
    path('dashboard/', views.home_dashboard, name='home_dashboard'),
    path('scanner/', views.scanner, name='scanner'),
    path("process_ticket/", api_utiles.process_ticket, name="process_ticket"),
    path('download_userprofiles_template/', api_utiles.download_userprofiles_template, name='download_userprofiles_template'),
    path('download_event_template/', api_utiles.download_event_template, name='download_event_template'),
    path('download_paper_template/', api_utiles.download_paper_template, name='download_paper_template'),
]
