from django.contrib import admin
from django.urls import path
from authentication.models import Event
from custom_admin_dashboard.views import upload_event_file
# Register your models here.

class EventAdmin(admin.ModelAdmin):
    change_list_template = 'admin/events_change_list.html'

    # Override get_urls() method to include custom view
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload/', self.admin_site.admin_view(upload_event_file), name='upload_event_file'),
        ]
        return custom_urls + urls


admin.site.register(Event, EventAdmin)