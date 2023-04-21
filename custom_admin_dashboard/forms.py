# custom_admin_dashboard/forms.py
from django import forms

class AdminEventFileUploadForm(forms.Form):
    event_file = forms.FileField()
