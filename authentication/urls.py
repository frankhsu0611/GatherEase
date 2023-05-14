from django.contrib import admin
from django.urls import path
from . import views, api_utils
from django.urls import path, include


urlpatterns = [
    path('', views.home, name='home'),
    path('ticket/<str:ticket_id>/', views.ticket, name='ticket'),
    path('signup/', views.signup, name='sign-up'),
    path('signin/', views.signin, name='sign-in'),
    path('signout/', views.signout, name='signout'),
    path('agenda/<str:ticket_id>/', views.agenda, name='agenda'),
    path('download/<str:ticket_id>/', views.download, name='download'),
    path('proceedings/download/<str:ticket_id>/', api_utils.download_proceedings, name='download_proceedings'),
    path('program/download/<str:ticket_id>/', api_utils.download_program, name='download_program'),
    path('certificate/download/<str:ticket_id>/', api_utils.download_certificate, name='download_certificate'),
    path('password_change/', views.change_password, name='password_change'),
    path('password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    #path('certificate/', views.certificate, name='download_certificate'),
]
