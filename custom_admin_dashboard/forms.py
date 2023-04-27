# custom_admin_dashboard/forms.py
from django import forms

class AdminEventFileUploadForm(forms.Form):
    event_file = forms.FileField()

class AdminUserProfileFileUploadForm(forms.Form):
    user_profiles_file = forms.FileField(label="Upload Excel file")

class AdminPaperFileUploadForm(forms.Form):
    paper_file = forms.FileField(label="Upload Excel file")