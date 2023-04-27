from django.contrib import admin
from django.urls import path
from authentication.models import Event, UserProfile, Paper
from custom_admin_dashboard.views import upload_event_file, upload_userprofiles_file, upload_paper_file
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

class UserProfileAdmin(admin.ModelAdmin):
    change_list_template = 'admin/userprofiles_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload/', self.admin_site.admin_view(upload_userprofiles_file), name='upload_userprofiles_file'),
        ]
        return custom_urls + urls
    
admin.site.register(UserProfile, UserProfileAdmin)


class PaperAdmin(admin.ModelAdmin):
    change_list_template = 'admin/papers_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload/', self.admin_site.admin_view(upload_paper_file), name='upload_paper_file'),
        ]
        return custom_urls + urls

admin.site.register(Paper, PaperAdmin)