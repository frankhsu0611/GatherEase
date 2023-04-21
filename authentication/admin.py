from django.contrib import admin

from .models import UserProfile, Conference, Event
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Conference)
#admin.site.register(Event)